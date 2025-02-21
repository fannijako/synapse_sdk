from ..synapse_notebooks.generic_utils import * # pylint: disable=wrong-import-order,unused-wildcard-import,wildcard-import
from test_helper import create_test_delta # pylint: disable=wrong-import-order,unused-wildcard-import

from pyspark.sql.types import * # type: ignore # pylint: disable=wrong-import-order,unused-wildcard-import,wildcard-import

test_curated_location, test_trusted_location = create_test_delta(Notebook())

table = Table(name = 'test_delta_listing_curated', layer = "curated")
table2 = Table(name = 'test_delta_listing_trusted', layer = "trusted")

assert table.name == 'test_delta_listing_curated', 'table name is not set correctly'

try:
    table.name = 'test'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

assert table.name == 'test_delta_listing_curated', "Table name has changed"

assert table.layer == 'curated', 'layer is not set correctly'

try:
    table.layer = 'trusted'
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

assert  table.layer == 'curated', "Layer had changed"

assert table.load_type == 'full', 'load type is not set correctly'

try:
    table.load_type = ['full', 'scd1']
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

assert table.load_type == 'full', "load type had changed"

assert table.path == test_curated_location, "Find_path does not set correctly"
assert table2.path == test_trusted_location, "Find_path does not set correctly"

try:
    table3 = Table(name = 'test_delta_listing_curated', layer = "trusted")
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

try:
    table3 = Table(name = 10, layer = "curated")
    raise AssertionError("Error was not raised")
except TypeError:
    pass
except Exception as e:
    raise e

try:
    table3 = Table(name = 'string', layer = "standardized")
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

assert table != table2
assert table == Table(name = 'test_delta_listing_curated', layer = "curated")

assert isinstance(table.delta_table, DeltaTable), "delta_table is not type DeltaTable"
assert 'merge' in dir(table.delta_table), "delta_table is not type DeltaTable"
assert 'vacuum' in dir(table.delta_table), "delta_table is not type DeltaTable"
assert 'history' in dir(table.delta_table), "delta_table is not type DeltaTable"
assert 'optimize' in dir(table.delta_table), "delta_table is not type DeltaTable"
assert 'detail' in dir(table.delta_table), "delta_table is not type DeltaTable"

assert isinstance(table.dataframe, DataFrame), "dataframe type is not correct"

assert table.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('salary', LongType(), True),  # type: ignore # pylint: disable=undefined-variable
                                             StructField('department', StringType(), True)]) # type: ignore # pylint: disable=undefined-variable

assert table.table_size > 0, "Table size not calculated correctly"
assert table.table_size < 1024*1024, 'Table size not calculated correctly'
assert table.target_file_size == '128mb', "Target file size not set correctly"

try:
    table.delta_table = DeltaTable.forPath(spark, test_curated_location) # type: ignore # pylint: disable=undefined-variable
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

try:
    table.dataframe = spark.read.format('delta').load(test_curated_location) # type: ignore # pylint: disable=undefined-variable
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

ERROR_MESSAGE = "str representation is not set correctly"
assert str(table).startswith("tisc data product's test_delta_listing_curated"), ERROR_MESSAGE
ERROR_MESSAGE = "repr representation is not set correctly"
assert repr(table).startswith("Table(name='test_delta_listing_curated'"), ERROR_MESSAGE

try:
    table.vacuum(hours = 0, force = False)
    raise AssertionError("Error was not raised")
except UserWarning:
    pass
except Exception as e:
    raise e

test_curated_location, test_trusted_location = create_test_delta(Notebook())
table.optimize()
table.vacuum(hours = 0, force = True)

assert spark.conf.get("spark.databricks.delta.retentionDurationCheck.enabled") == 'true', "retention duration check is not reset" # type: ignore # pylint: disable=undefined-variable,line-too-long
assert len([file
            for file
            in mssparkutils.fs.ls(f'{test_curated_location}')
            if file.name != '_delta_log']) == 1

table.vacuum(hours = 168)

try:
    table.zorder(columns = [])
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

table.zorder(columns = ['department'])

history = table.delta_table.history(1)

ERROR_MESSAGE = 'OPTIMIZE command was not executed'
assert history.select('operation').collect()[0][0] == 'OPTIMIZE', ERROR_MESSAGE
ERROR_MESSAGE = "department is not set as a ZORDER column"
assert (history.select('operationParameters')
               .collect()[0][0].get('zOrderBy', '')) == '["department"]', ERROR_MESSAGE

assert isinstance(table.history(), DataFrame), "History is not returning a dataframe"
assert table.history().schema == StructType([StructField('version', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('timestamp', TimestampType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('userId', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('userName', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('operation', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('operationParameters', MapType(StringType(), StringType(), True), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('job', StructType([StructField('jobId', StringType(), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('jobName', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('runId', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('jobOwnerId', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('triggerType', StringType(), True)]), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('notebook', StructType([StructField('notebookId', StringType(), True)]), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('clusterId', StringType(), True), StructField('readVersion', LongType(), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('isolationLevel', StringType(), True), StructField('isBlindAppend', BooleanType(), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('operationMetrics', MapType(StringType(), StringType(), True), True), # type: ignore # pylint: disable=undefined-variable,line-too-long
                                             StructField('userMetadata', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                             StructField('engineInfo', StringType(), True)]), "Schema is not correct" # type: ignore # pylint: disable=undefined-variable,line-too-long
assert len(table.history().collect()) == 10, 'History does not return 10 items'
assert len(table.history(1).collect()) == 1, 'History(1) does not return 1 items'

table.set_table_properties()
assert (table.delta_table.detail()
             .select('properties')
             .collect()[0][0].get('delta.autoOptimize.optimizeWrite',
                                  '')) == 'true', 'Optimizewrite is not set'
assert (table.delta_table.detail()
             .select('properties')
             .collect()[0][0].get('delta.targetFileSize',
                                  '')) == '128mb', 'Target file size is not set'
assert (table.delta_table.detail()
             .select('properties')
             .collect()[0][0].get('delta.dataSkippingNumIndexedCols',
                                  '')) == '4', "dataSkippingNumIndexedCols are not set"

assert table.get_optimization_recommendations() is None
