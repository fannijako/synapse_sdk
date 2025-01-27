from pyspark.sql import SparkSession # type: ignore

import generic_utils

@pytest.fixture(scope = "local") # type: ignore
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()


