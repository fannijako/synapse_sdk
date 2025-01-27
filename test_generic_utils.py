from pyspark.sql import SparkSession

import generic_utils

@pytest.fixture(scope = "local")
def spark():
    return SparkSession.builder.master("local").appName("test").getOrCreate()


