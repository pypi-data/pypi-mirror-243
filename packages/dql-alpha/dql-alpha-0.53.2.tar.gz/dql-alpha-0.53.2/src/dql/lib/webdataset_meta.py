import os

import numpy as np

from dql.lib.utils import bin_to_array, row_list_to_pandas
from dql.query import C, DatasetRow, LocalFilename, udf
from dql.sql.types import Array, Float32, Int64, String

try:
    import pandas as pd
except ImportError:
    pd = None


def union_dicts(*dicts):
    """Union dictionaries.
    Equivalent to `d1 | d2 | d3` in Python3.9+ but works in older versions.
    """
    result = None
    for d in dicts:
        if not isinstance(d, dict):
            raise ValueError("All arguments must be dictionaries.")
        if not result:
            result = d.copy()
        else:
            result.update(d)
    return result


group_params = (
    C.ext,
    LocalFilename(),
)
group_schema = {"parquet_data": Array(Int64), "npz_data": Array(Int64)}

group_params_fname = group_params[:-1] + (C.fname,)


# We need to merge parque and npz data first because they need to be
# used together for generating multiple records.
# It won't be a requirement when aggregator will generator based.
@udf(parameters=group_params, output=tuple(group_schema.items()))
class MergeParquetAndNpz:
    def __call__(self, args):
        df = row_list_to_pandas(args, group_params_fname)

        fname_npz = df[df.ext == "npz"].fname.iloc[0]
        fname_pq = df[df.ext == "parquet"].fname.iloc[0]
        npz_data = bin_to_array(open(fname_npz, "rb").read())
        pq_data = bin_to_array(open(fname_pq, "rb").read())

        df["npz_data"] = df.ext.apply(lambda x: npz_data if x == "parquet" else None)
        df["parquet_data"] = df.ext.apply(lambda x: pq_data if x == "parquet" else None)

        df = df.drop(["ext", "fname"], axis=1)
        return tuple(map(tuple, df.values))


pq_schema = {
    "uid": String,
    "url": String,
    "text": String,
    "original_width": Int64,
    "original_height": Int64,
    "clip_b32_similarity_score": Float32,
    "clip_l14_similarity_score": Float32,
    "face_bboxes": Array(Array(Float32)),
    "sha256": String,
}

npz_schema = {
    "b32_img": Array(Float32),
    "b32_txt": Array(Float32),
    "l14_img": Array(Float32),
    "l14_txt": Array(Float32),
    "dedup": Array(Float32),
}

meta_params = DatasetRow.schema + (C.parquet_data, C.npz_data)
meta_schema = {**pq_schema, **npz_schema}


@udf(
    parameters=(C.source, C.parent, C.name, C.etag, C.parquet_data, C.npz_data),
    output=DatasetRow.schema + tuple(meta_schema.items()),
)
class GenerateMeta:
    def __call__(self, source, parent, name, etag, parquet_data, npz_data):
        if parquet_data is None or npz_data is None:
            return DatasetRow.create(name, source=source, parent=parent, etag=etag) + (
                None,
            ) * len(meta_schema)

        # Hack until bin data issues is solved
        pq_fname = f"{parent}/{name}"
        npz_fname = os.path.splitext(pq_fname)[0] + ".npz"

        df = pd.read_parquet(pq_fname)
        npz = np.load(npz_fname)

        for idx, (_, row) in enumerate(df.iterrows()):
            row_basic = DatasetRow.create(
                str(idx),
                source=source,
                parent=f"{parent}/{name}",
                etag=etag,
                vtype="parquet",
            )

            pq_payload = tuple([row[key] for key in pq_schema.keys()])
            npz_payload = tuple([npz[key][idx] for key in npz_schema.keys()])

            yield row_basic + pq_payload + npz_payload
