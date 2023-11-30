import os

from dql.lib.webdataset_meta import GenerateMeta, MergeParquetAndNpz
from dql.query import udf
from dql.query.dataset import DatasetQuery
from dql.query.schema import C
from dql.sql.types import String

ds = DatasetQuery("s3://dvcx-datacomp-small")
ds = ds.filter(C.name.glob("0020*"))


# NOTE, this script does not work end-to-end due to a missing/not-optimized
# functionality such as binary column support and generator-based group-by.
# However, it's still useful to keep it in the codebase as a requirement.


@udf(
    parameters=(C.name,),
    output=(("basename", String), ("ext", String)),
)
def split_name(name):
    basename, ext = os.path.splitext(name)
    return basename, ext.strip(".")


ds = ds.add_signals(split_name)
ds = ds.add_signals(MergeParquetAndNpz, group_by=C.basename)

ds = ds.generate(GenerateMeta)

print(
    ds.limit(20)
    .select(C.parent, C.name, C.uid, C.clip_b32_similarity_score, C.b32_txt)
    .to_pandas()
)
