from dql.lib.webdataset import WebDataset
from dql.query.dataset import DatasetQuery
from dql.query.schema import C

ds = DatasetQuery("s3://dvcx-datacomp-small")

wds = ds.filter(C.name.glob("0000000*.tar")).generate(WebDataset, processes=True)

print(wds.select(C.parent, C.name, C.uid, C.width, C.height).to_pandas())
