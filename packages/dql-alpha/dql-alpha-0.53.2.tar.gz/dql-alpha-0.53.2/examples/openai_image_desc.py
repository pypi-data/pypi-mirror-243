# pip install Pillow

import base64
import io
import os

import requests
from PIL import Image, ImageOps, UnidentifiedImageError

from dql.query import C, DatasetQuery, Object, udf
from dql.sql.types import String

source = "s3://ldb-public/remote/data-lakes/dogs-and-cats/"
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")

headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {OPENAI_API_KEY}",
}


def encode_image(raw):
    try:
        img = Image.open(raw)
    except UnidentifiedImageError:
        return None
    img.load()
    img = ImageOps.fit(img, (500, 500))
    output = io.BytesIO()
    img.save(output, format="JPEG")
    hex_data = output.getvalue()
    return base64.b64encode(hex_data).decode("utf-8")


@udf(
    output=(("description", String),),  # Signals being returned by the UDF.
    parameters=(Object(encode_image),),  # Columns consumed by the UDF.
)
def image_description(base64_image):
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": "What’s in this image?"},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"},
                    },
                ],
            }
        ],
        "max_tokens": 300,
    }

    response = requests.post(
        "https://api.openai.com/v1/chat/completions", headers=headers, json=payload
    )
    json_response = response.json()

    if "error" in json_response:
        openai_description = str(json_response["error"])
    else:
        openai_description = json_response["choices"][0]["message"]["content"]

    return (openai_description,)


if __name__ == "__main__":
    results = (
        DatasetQuery(
            source,
            client_config={"aws_anon": True},
        )
        .filter(C.name.glob("cat.*.jpg"))
        .limit(5)
        .add_signals(image_description, processes=True)
        .select("source", "parent", "name", "description")
        .results()
    )
    print(*results, sep="\n")
