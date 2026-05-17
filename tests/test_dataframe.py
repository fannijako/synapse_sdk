import builtins  # noqa: C0413
from datetime import datetime

import pytest  # type: ignore
from pyspark.sql.types import (IntegerType, LongType, StringType,  # type: ignore
                               StructField, StructType)

from src.generic_utils import DataFrame, LHTSparkDataFrame, Notebook, Table
from tests.test_helper import create_test_delta

spark = getattr(builtins, 'spark', None)  # pylint: disable=invalid-name


@pytest.fixture(scope='module')
def test_delta_locations():
    return create_test_delta(Notebook())


@pytest.fixture
def dataframe(test_delta_locations):  # pylint: disable=unused-argument
    return LHTSparkDataFrame(name='test_delta_listing_curated', layer='curated')


@pytest.fixture
def dataframe2(test_delta_locations):  # pylint: disable=unused-argument
    return LHTSparkDataFrame(name='test_delta_listing_trusted', layer='trusted')


class TestLHTSparkDataFrameAttributes:
    def test_file_format_class_attribute(self):
        assert LHTSparkDataFrame.file_format == 'delta'

    def test_file_format_instance(self, dataframe):
        assert dataframe.file_format == 'delta'

    def test_name(self, dataframe):
        assert dataframe.name == 'test_delta_listing_curated'

    def test_layer(self, dataframe):
        assert dataframe.layer == 'curated'

    def test_load_type_default(self, dataframe):
        assert dataframe.load_type == 'full'


class TestLHTSparkDataFrameDeltaTable:
    def test_delta_table_is_table(self, dataframe):
        assert isinstance(dataframe.delta_table, Table)

    def test_delta_table_is_readonly(self, dataframe, test_delta_locations):
        from src.generic_utils import DeltaTable  # pylint: disable=import-outside-toplevel
        test_curated_location, _ = test_delta_locations
        with pytest.raises(AttributeError):
            dataframe.delta_table = DeltaTable.forPath(spark, test_curated_location)  # type: ignore


class TestLHTSparkDataFrameVersioning:
    def test_latest_version_is_set(self, dataframe):
        assert dataframe.latest_version is not None

    def test_latest_version_is_int(self, dataframe):
        assert isinstance(dataframe.latest_version, int)

    def test_version_default_set(self, dataframe):
        assert dataframe.version is not None

    def test_timestamp_default_set(self, dataframe):
        assert dataframe.timestamp is not None

    def test_explicit_version(self, dataframe, test_delta_locations):  # pylint: disable=unused-argument
        explicit = LHTSparkDataFrame(name='test_delta_listing_curated',
                                     layer='curated',
                                     version=dataframe.latest_version)
        assert explicit.version == dataframe.latest_version

    def test_explicit_version_equal_to_latest(self, dataframe, test_delta_locations):  # pylint: disable=unused-argument
        explicit = LHTSparkDataFrame(name='test_delta_listing_curated',
                                     layer='curated',
                                     version=dataframe.latest_version)
        assert dataframe == explicit

    def test_version_and_timestamp_conflict_raises(self, test_delta_locations):  # pylint: disable=unused-argument
        with pytest.raises(ValueError):
            LHTSparkDataFrame(name='test_delta_listing_trusted',
                              layer='trusted',
                              version=10,
                              timestamp='2024-02-19')

    def test_explicit_timestamp(self, test_delta_locations):  # pylint: disable=unused-argument
        datetime_str = datetime.today().strftime('%Y-%m-%d')
        dataframe5 = LHTSparkDataFrame(name='test_delta_listing_trusted',
                                       layer='trusted',
                                       timestamp=datetime_str)
        assert dataframe5.timestamp == datetime_str


class TestLHTSparkDataFrameSchema:
    def test_dataframe_type(self, dataframe):
        assert isinstance(dataframe.dataframe, DataFrame)

    def test_dataframe_schema(self, dataframe):
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('salary', LongType(), True),
            StructField('department', StringType(), True),
        ])
        assert dataframe.dataframe.schema == expected


class TestLHTSparkDataFrameEquality:
    def test_different_dataframes_unequal(self, dataframe, dataframe2):
        assert dataframe != dataframe2

    def test_equal_to_itself(self, dataframe):
        assert dataframe == dataframe  # pylint: disable=comparison-with-itself


class TestLHTSparkDataFrameOrdering:
    @pytest.fixture
    def older(self, dataframe, test_delta_locations):  # pylint: disable=unused-argument
        return LHTSparkDataFrame(name='test_delta_listing_curated',
                                 layer='curated',
                                 version=dataframe.latest_version - 1)

    def test_lt_true(self, older, dataframe):
        assert older < dataframe

    def test_lt_false_other_direction(self, older, dataframe):
        assert not dataframe < older  # pylint: disable=unnecessary-negation

    def test_lt_false_self(self, dataframe):
        assert not dataframe < dataframe  # pylint: disable=comparison-with-itself,unnecessary-negation

    def test_le_true(self, older, dataframe):
        assert older <= dataframe

    def test_le_false_other_direction(self, older, dataframe):
        assert not dataframe <= older  # pylint: disable=unnecessary-negation

    def test_le_self(self, dataframe):
        assert dataframe <= dataframe  # pylint: disable=comparison-with-itself

    def test_gt_false(self, older, dataframe):
        assert not older > dataframe  # pylint: disable=unnecessary-negation

    def test_gt_true(self, older, dataframe):
        assert dataframe > older

    def test_gt_false_self(self, dataframe):
        assert not dataframe > dataframe  # pylint: disable=comparison-with-itself,unnecessary-negation

    def test_ge_false(self, older, dataframe):
        assert not older >= dataframe  # pylint: disable=unnecessary-negation

    def test_ge_true(self, older, dataframe):
        assert dataframe >= older

    def test_ge_self(self, dataframe):
        assert dataframe >= dataframe  # pylint: disable=comparison-with-itself

    def test_compare_across_layers_raises(self, dataframe, dataframe2):
        with pytest.raises(ValueError):
            dataframe2 < dataframe  # pylint: disable=pointless-statement

    def test_add_version_offset(self, older, dataframe):
        assert older + 1 == dataframe

    def test_sub_version_offset(self, older, dataframe):
        assert dataframe - 1 == older


class TestLHTSparkDataFrameRepr:
    def test_str(self, dataframe):
        assert str(dataframe).startswith("tisc data product's test_delta_listing")

    def test_repr(self, dataframe):
        assert repr(dataframe).startswith("LHTSparkDataFrame(name='")


class TestLHTSparkDataFrameMergeChangeDetection:
    def test_version_incremented_after_empty_merge(self, dataframe):
        before = dataframe.version
        dataframe.delta_table.delta_table.alias("src").merge(  # pylint: disable=no-member
            spark.createDataFrame([], dataframe.dataframe.schema).alias("dst"),  # type: ignore
            dataframe.construct_merge_condition(dataframe.dataframe.columns),
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        assert before == dataframe.get_latest_version() - 1

    def test_is_changed_false_after_empty_merge(self, dataframe):
        dataframe.delta_table.delta_table.alias("src").merge(  # pylint: disable=no-member
            spark.createDataFrame([], dataframe.dataframe.schema).alias("dst"),  # type: ignore
            dataframe.construct_merge_condition(dataframe.dataframe.columns),
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        assert not dataframe.is_changed_since_last_version([])

    def test_is_changed_true_after_non_empty_merge(self, dataframe):
        dataframe.delta_table.delta_table.alias("src").merge(  # pylint: disable=no-member
            spark.createDataFrame(  # type: ignore
                [('Alice', 101, 30000, "HR")], dataframe.dataframe.schema
            ).alias("dst"),
            dataframe.construct_merge_condition(dataframe.dataframe.columns),
        ).whenMatchedUpdateAll().whenNotMatchedInsertAll().execute()
        assert dataframe.is_changed_since_last_version([])


class TestLHTSparkDataFrameWriteToDatabase:
    def test_merge_mode_raises(self, dataframe):
        with pytest.raises(ValueError):
            dataframe.write_to_database(database_name='test_database_name',
                                        database_schema='test_database_schema',
                                        mode='merge')


class TestLHTSparkDataFrameColumnTransforms:
    def test_add_timestamp_column(self, dataframe):
        dataframe.add_timestamp_column()
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('salary', LongType(), True),
            StructField('department', StringType(), True),
            StructField('load_timestamp', StringType(), False),
        ])
        assert dataframe.dataframe.schema == expected

    def test_add_hash_column(self, dataframe):
        dataframe.add_timestamp_column()
        dataframe.add_hash_column()
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('salary', LongType(), True),
            StructField('department', StringType(), True),
            StructField('load_timestamp', StringType(), False),
            StructField('dap_hash', StringType(), True),
        ])
        assert dataframe.dataframe.schema == expected

    def test_rename_columns_with_pattern(self, dataframe):
        dataframe.add_timestamp_column()
        dataframe.add_hash_column()
        dataframe.rename_columns_w_pattern(pattern_to_replace='dap', replace_to='lhtdap')
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('salary', LongType(), True),
            StructField('department', StringType(), True),
            StructField('load_timestamp', StringType(), False),
            StructField('lhtdap_hash', StringType(), True),
        ])
        assert dataframe.dataframe.schema == expected

    def test_rename_columns_with_mapping(self, dataframe):
        dataframe.add_timestamp_column()
        dataframe.add_hash_column()
        dataframe.rename_columns_w_pattern(pattern_to_replace='dap', replace_to='lhtdap')
        dataframe.rename_columns_w_mapping({'load_timestamp': 'load_time', 'salary': 'wage'})
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('wage', LongType(), True),
            StructField('department', StringType(), True),
            StructField('load_time', StringType(), False),
            StructField('lhtdap_hash', StringType(), True),
        ])
        assert dataframe.dataframe.schema == expected

    def test_cast_data_columns(self, dataframe):
        dataframe.add_timestamp_column()
        dataframe.add_hash_column()
        dataframe.rename_columns_w_pattern(pattern_to_replace='dap', replace_to='lhtdap')
        dataframe.rename_columns_w_mapping({'load_timestamp': 'load_time', 'salary': 'wage'})
        dataframe.cast_data_columns({'age': IntegerType(), 'wage': IntegerType()})
        expected = StructType([
            StructField('name', StringType(), True),
            StructField('age', IntegerType(), True),
            StructField('wage', IntegerType(), True),
            StructField('department', StringType(), True),
            StructField('load_time', StringType(), False),
            StructField('lhtdap_hash', StringType(), True),
        ])
        assert dataframe.dataframe.schema == expected


class TestLHTSparkDataFrameMergeCondition:
    def test_single_column(self, dataframe):
        assert dataframe.construct_merge_condition(['name']) == 'src.name <=> dst.name'

    def test_multiple_columns(self, dataframe):
        expected = 'src.name <=> dst.name AND src.department <=> dst.department'
        assert dataframe.construct_merge_condition(['name', 'department']) == expected

    def test_nulls_not_matched(self, dataframe):
        actual = dataframe.construct_merge_condition(['name'], are_nulls_matched=False)
        assert actual == 'src.name == dst.name'

    def test_custom_sink(self, dataframe):
        actual = dataframe.construct_merge_condition(['name'],
                                                     sink='sink',
                                                     are_nulls_matched=False)
        assert actual == 'src.name == sink.name'

    def test_custom_source_and_sink(self, dataframe):
        actual = dataframe.construct_merge_condition(['name'],
                                                     source='source',
                                                     sink='sink',
                                                     are_nulls_matched=False)
        assert actual == 'source.name == sink.name'


class TestLHTSparkDataFrameExcelWrite:
    def test_write_to_excel_creates_file(self, dataframe):
        path = f'{dataframe.standardized_curated_path}/generic_utils/integration_test'
        target = path + '/excel_write_test.xlsx'
        dataframe.write_to_excel(target_path=target)
        matches = [file
                   for file
                   in dataframe.deep_ls(path, max_depth=1)
                   if file.name == 'excel_write_test.xlsx']
        assert len(matches) == 1
