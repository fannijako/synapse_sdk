from ..synapse_notebooks.generic_utils import * # pylint: disable=wrong-import-order,unused-wildcard-import,wildcard-import
from test_helper import create_test_delta # pylint: disable=wrong-import-order,unused-wildcard-import

from pyspark.sql.types import * # type: ignore # pylint: disable=wrong-import-order,unused-wildcard-import,wildcard-import

test_curated_location, test_trusted_location = create_test_delta(Notebook())

dataframe = LHTSparkDataFrame(name = 'test_delta_listing_curated', layer = "curated")
dataframe2 = LHTSparkDataFrame(name = 'test_delta_listing_trusted', layer = "trusted")

assert LHTSparkDataFrame.file_format == 'delta', "Class attribute file format is not set"
assert dataframe.file_format == 'delta', "File format attribute is not set"
assert dataframe.name == 'test_delta_listing_curated', 'Name is not set correctly'
assert dataframe.layer == 'curated', "Layer is not set correctly"
assert dataframe.load_type == 'full', "Load type is not set correctly"

assert isinstance(dataframe.delta_table, Table), "Delta Table type is not set correctly"
try:
    dataframe.delta_table = DeltaTable.forPath(spark, test_curated_location) # type: ignore # pylint: disable=undefined-variable
    raise AssertionError("Error was not raised")
except AttributeError:
    pass
except Exception as e:
    raise e

assert dataframe.latest_version is not None, 'Latest version is not set'
assert isinstance(dataframe.latest_version, int), 'Latest version type is not correct'

assert dataframe.version is not None, 'Version was set'
assert dataframe.timestamp is not None, 'timestamp was set'

ERROR_MESSAGE = "Dataframe schema is not correct"
assert isinstance(dataframe.dataframe, DataFrame), "Dataframe type is not correct"
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('salary', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable

assert dataframe != dataframe2, 'Different dataframes equal'
assert dataframe == dataframe, 'Equal dataframes differ' # pylint: disable=comparison-with-itself

dataframe4 = LHTSparkDataFrame(name = 'test_delta_listing_curated',
                               layer = "curated",
                               version = dataframe.latest_version)
assert dataframe4.version == dataframe.latest_version, 'Version is not set correctly'
assert dataframe == dataframe4, 'Dataframes should equal'

try:
    dataframe3 = LHTSparkDataFrame(name = 'test_delta_listing_trusted',
                                   layer = "trusted",
                                   version = 10,
                                   timestamp = '2024-02-19')
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

DATETIME = datetime.today().strftime('%Y-%m-%d') # pylint: disable=no-member
dataframe5 = LHTSparkDataFrame(name = 'test_delta_listing_trusted',
                               layer = "trusted",
                               timestamp = DATETIME)
assert dataframe5.timestamp == DATETIME, 'Timestamp is not set correctly'

dataframe6 = LHTSparkDataFrame(name = 'test_delta_listing_curated',
                               layer = "curated",
                               version = dataframe.latest_version - 1)
assert dataframe6 < dataframe, '< is not defined correctly'
assert not dataframe < dataframe6, '< is not defined correctly' # pylint: disable=unnecessary-negation
assert not dataframe < dataframe, '< is not defined correctly' # pylint: disable=comparison-with-itself,unnecessary-negation

assert dataframe6 <= dataframe, '<= is not defined correctly'
assert not dataframe <= dataframe6, '<= is not defined correctly' # pylint: disable=unnecessary-negation
assert dataframe <= dataframe, '<= is not defined correctly' # pylint: disable=comparison-with-itself

assert not dataframe6 > dataframe, '> is not defined correctly' # pylint: disable=unnecessary-negation
assert dataframe > dataframe6, '> is not defined correctly'
assert not dataframe > dataframe, '> is not defined correctly' # pylint: disable=comparison-with-itself,unnecessary-negation

assert not dataframe6 >= dataframe, '>= is not defined correctly' # pylint: disable=unnecessary-negation
assert dataframe >= dataframe6, '>= is not defined correctly'
assert dataframe >= dataframe, '>= is not defined correctly' # pylint: disable=comparison-with-itself

try:
    dataframe2 < dataframe # pylint: disable=pointless-statement
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

dataframe7 = dataframe6 + 1
assert dataframe7 == dataframe

dataframe8 = dataframe7 - 1
assert dataframe8 == dataframe6

ERROR_MESSAGE = "str is not set correctly"
assert str(dataframe).startswith("tisc data product's test_delta_listing"), ERROR_MESSAGE
assert repr(dataframe).startswith("LHTSparkDataFrame(name='"), "repr is not set correctly"

# Simulate a merge with 0 effected rows
dataframe.delta_table.delta_table.alias("src").merge( # pylint: disable=no-member
    spark.createDataFrame([], dataframe.dataframe.schema).alias("dst"), # type: ignore # pylint: disable=undefined-variable
    dataframe.construct_merge_condition(dataframe.dataframe.columns)
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

assert dataframe.version == dataframe.get_latest_version() - 1

ERROR_MESSAGE = 'Should be false after a merge condition with 0 affected rows'
assert not dataframe.is_changed_since_last_version([]), ERROR_MESSAGE

# Simulate a merge with 1 effected row
dataframe.delta_table.delta_table.alias("src").merge( # pylint: disable=no-member
    spark.createDataFrame([('Alice', 101, 30000, "HR")], dataframe.dataframe.schema).alias("dst"), # type: ignore # pylint: disable=undefined-variable
    dataframe.construct_merge_condition(dataframe.dataframe.columns)
).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()

ERROR_MESSAGE = 'Should be false after a merge condition with 1 affected row'
assert dataframe.is_changed_since_last_version([]), ERROR_MESSAGE

try:
    dataframe.write_to_database(database_name = 'test_database_name',
                                database_schema = 'test_database_schema',
                                mode = 'merge')
    raise AssertionError("Error was not raised")
except ValueError:
    pass
except Exception as e:
    raise e

dataframe.add_timestamp_column()
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('salary', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('load_timestamp', StringType(), False)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable,line-too-long

dataframe.add_hash_column()
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('salary', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('load_timestamp', StringType(), False), # type: ignore # pylint: disable=undefined-variable
                                     StructField('dap_hash', StringType(), True)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable

dataframe.rename_columns_w_pattern(pattern_to_replace='dap', replace_to='lhtdap')
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('salary', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('load_timestamp', StringType(), False), # type: ignore # pylint: disable=undefined-variable
                                     StructField('lhtdap_hash', StringType(), True)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable

dataframe.rename_columns_w_mapping({'load_timestamp': 'load_time', 'salary': 'wage'})
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('wage', LongType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('load_time', StringType(), False), # type: ignore # pylint: disable=undefined-variable
                                     StructField('lhtdap_hash', StringType(), True)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable

dataframe.cast_data_columns({'age': IntegerType(), 'wage': IntegerType()}) # type: ignore # pylint: disable=undefined-variable
assert dataframe.dataframe.schema == StructType([StructField('name', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('age', IntegerType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('wage', IntegerType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('department', StringType(), True), # type: ignore # pylint: disable=undefined-variable
                                     StructField('load_time', StringType(), False), # type: ignore # pylint: disable=undefined-variable
                                     StructField('lhtdap_hash', StringType(), True)]), ERROR_MESSAGE # type: ignore # pylint: disable=undefined-variable

assert dataframe.construct_merge_condition(['name']) == 'src.name <=> dst.name'
EXPECTED = 'src.name <=> dst.name AND src.department <=> dst.department'
assert dataframe.construct_merge_condition(['name', 'department']) == EXPECTED
assert dataframe.construct_merge_condition(['name'],
                                           are_nulls_matched=False) == 'src.name == dst.name'
assert dataframe.construct_merge_condition(['name'],
                                           sink = 'sink',
                                           are_nulls_matched=False) == 'src.name == sink.name'
assert dataframe.construct_merge_condition(['name'],
                                           source = 'source',
                                           sink = 'sink',
                                           are_nulls_matched=False) == 'source.name == sink.name'

PATH = f'{dataframe.standardized_curated_path}/generic_utils/integration_test'
dataframe.write_to_excel(target_path = PATH + '/excel_write_test.xlsx')
assert len([file
            for file
            in dataframe.deep_ls(PATH, max_depth=1)
            if file.name == 'excel_write_test.xlsx']) == 1, 'File was not written'
