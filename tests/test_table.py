import builtins  # noqa: C0413

import pytest  # type: ignore
from pyspark.sql.types import (BooleanType, LongType, MapType, StringType,  # type: ignore
                               StructField, StructType, TimestampType)

from src.generic_utils import DataFrame, DeltaTable, Notebook, Table, mssparkutils
from tests.test_helper import create_test_delta

spark = getattr(builtins, 'spark', None)  # pylint: disable=invalid-name


@pytest.fixture(scope='module')
def test_delta_locations():
    return create_test_delta(Notebook())


@pytest.fixture
def table(test_delta_locations):  # pylint: disable=unused-argument
    return Table(name='test_delta_listing_curated', layer='curated')


@pytest.fixture
def table2(test_delta_locations):  # pylint: disable=unused-argument
    return Table(name='test_delta_listing_trusted', layer='trusted')


class TestTableAttributes:
    def test_name(self, table):
        assert table.name == 'test_delta_listing_curated'

    def test_name_is_readonly(self, table):
        with pytest.raises(AttributeError):
            table.name = 'test'

    def test_name_unchanged_after_failed_write(self, table):
        with pytest.raises(AttributeError):
            table.name = 'test'
        assert table.name == 'test_delta_listing_curated'

    def test_layer(self, table):
        assert table.layer == 'curated'

    def test_layer_is_readonly(self, table):
        with pytest.raises(AttributeError):
            table.layer = 'trusted'

    def test_layer_unchanged_after_failed_write(self, table):
        with pytest.raises(AttributeError):
            table.layer = 'trusted'
        assert table.layer == 'curated'

    def test_load_type_default(self, table):
        assert table.load_type == 'full'

    def test_load_type_rejects_list(self, table):
        with pytest.raises(TypeError):
            table.load_type = ['full', 'scd1']

    def test_load_type_unchanged_after_failed_write(self, table):
        with pytest.raises(TypeError):
            table.load_type = ['full', 'scd1']
        assert table.load_type == 'full'

    def test_curated_path(self, table, test_delta_locations):
        test_curated_location, _ = test_delta_locations
        assert table.path == test_curated_location

    def test_trusted_path(self, table2, test_delta_locations):
        _, test_trusted_location = test_delta_locations
        assert table2.path == test_trusted_location


class TestTableConstruction:
    def test_layer_mismatch_raises(self, test_delta_locations):  # pylint: disable=unused-argument
        with pytest.raises(ValueError):
            Table(name='test_delta_listing_curated', layer='trusted')

    def test_int_name_raises(self, test_delta_locations):  # pylint: disable=unused-argument
        with pytest.raises(TypeError):
            Table(name=10, layer='curated')

    def test_unknown_layer_raises(self, test_delta_locations):  # pylint: disable=unused-argument
        with pytest.raises(ValueError):
            Table(name='string', layer='standardized')


class TestTableEquality:
    def test_different_tables_unequal(self, table, table2):
        assert table != table2

    def test_same_args_equal(self, table):
        assert table == Table(name='test_delta_listing_curated', layer='curated')


class TestTableDeltaTableProperty:
    def test_delta_table_type(self, table):
        assert isinstance(table.delta_table, DeltaTable)

    def test_delta_table_has_merge(self, table):
        assert 'merge' in dir(table.delta_table)

    def test_delta_table_has_vacuum(self, table):
        assert 'vacuum' in dir(table.delta_table)

    def test_delta_table_has_history(self, table):
        assert 'history' in dir(table.delta_table)

    def test_delta_table_has_optimize(self, table):
        assert 'optimize' in dir(table.delta_table)

    def test_delta_table_has_detail(self, table):
        assert 'detail' in dir(table.delta_table)

    def test_delta_table_is_readonly(self, table, test_delta_locations):
        test_curated_location, _ = test_delta_locations
        with pytest.raises(AttributeError):
            table.delta_table = DeltaTable.forPath(spark, test_curated_location)  # type: ignore


class TestTableDataframe:
    def test_dataframe_type(self, table):
        assert isinstance(table.dataframe, DataFrame)

    def test_dataframe_schema(self, table):
        assert table.dataframe.schema == StructType([
            StructField('name', StringType(), True),
            StructField('age', LongType(), True),
            StructField('salary', LongType(), True),
            StructField('department', StringType(), True),
        ])

    def test_dataframe_is_readonly(self, table, test_delta_locations):
        test_curated_location, _ = test_delta_locations
        with pytest.raises(AttributeError):
            table.dataframe = spark.read.format('delta').load(test_curated_location)  # type: ignore


class TestTableSize:
    def test_table_size_positive(self, table):
        assert table.table_size > 0

    def test_table_size_under_1mb(self, table):
        assert table.table_size < 1024 * 1024

    def test_target_file_size(self, table):
        assert table.target_file_size == '128mb'


class TestTableRepr:
    def test_str(self, table):
        assert str(table).startswith("tisc data product's test_delta_listing_curated")

    def test_repr(self, table):
        assert repr(table).startswith("Table(name='test_delta_listing_curated'")


class TestTableMaintenance:
    def test_vacuum_without_force_raises(self, table):
        with pytest.raises(UserWarning):
            table.vacuum(hours=0, force=False)

    def test_optimize_then_vacuum_leaves_one_file(self, table, test_delta_locations):
        test_curated_location, _ = test_delta_locations
        create_test_delta(Notebook())
        table.optimize()
        table.vacuum(hours=0, force=True)
        files = [file
                 for file
                 in mssparkutils.fs.ls(f'{test_curated_location}')
                 if file.name != '_delta_log']
        assert len(files) == 1

    def test_retention_check_reset_after_force_vacuum(self, table):
        create_test_delta(Notebook())
        table.optimize()
        table.vacuum(hours=0, force=True)
        actual = spark.conf.get("spark.databricks.delta.retentionDurationCheck.enabled")  # type: ignore
        assert actual == 'true'

    def test_default_vacuum_runs(self, table):
        table.vacuum(hours=168)

    def test_zorder_empty_columns_raises(self, table):
        with pytest.raises(ValueError):
            table.zorder(columns=[])

    def test_zorder_runs(self, table):
        table.zorder(columns=['department'])

    def test_zorder_recorded_in_history(self, table):
        table.zorder(columns=['department'])
        history = table.delta_table.history(1)
        assert history.select('operation').collect()[0][0] == 'OPTIMIZE'

    def test_zorder_columns_recorded(self, table):
        table.zorder(columns=['department'])
        history = table.delta_table.history(1)
        zorder_by = history.select('operationParameters').collect()[0][0].get('zOrderBy', '')
        assert zorder_by == '["department"]'


class TestTableHistory:
    def test_history_returns_dataframe(self, table):
        assert isinstance(table.history(), DataFrame)

    def test_history_schema(self, table):
        expected = StructType([
            StructField('version', LongType(), True),
            StructField('timestamp', TimestampType(), True),
            StructField('userId', StringType(), True),
            StructField('userName', StringType(), True),
            StructField('operation', StringType(), True),
            StructField('operationParameters', MapType(StringType(), StringType(), True), True),
            StructField('job', StructType([
                StructField('jobId', StringType(), True),
                StructField('jobName', StringType(), True),
                StructField('runId', StringType(), True),
                StructField('jobOwnerId', StringType(), True),
                StructField('triggerType', StringType(), True),
            ]), True),
            StructField('notebook', StructType([
                StructField('notebookId', StringType(), True),
            ]), True),
            StructField('clusterId', StringType(), True),
            StructField('readVersion', LongType(), True),
            StructField('isolationLevel', StringType(), True),
            StructField('isBlindAppend', BooleanType(), True),
            StructField('operationMetrics', MapType(StringType(), StringType(), True), True),
            StructField('userMetadata', StringType(), True),
            StructField('engineInfo', StringType(), True),
        ])
        assert table.history().schema == expected

    def test_history_default_count(self, table):
        assert len(table.history().collect()) == 10

    def test_history_with_limit(self, table):
        assert len(table.history(1).collect()) == 1


class TestTableProperties:
    def test_set_optimize_write(self, table):
        table.set_table_properties()
        props = table.delta_table.detail().select('properties').collect()[0][0]
        assert props.get('delta.autoOptimize.optimizeWrite', '') == 'true'

    def test_set_target_file_size(self, table):
        table.set_table_properties()
        props = table.delta_table.detail().select('properties').collect()[0][0]
        assert props.get('delta.targetFileSize', '') == '128mb'

    def test_set_data_skipping_columns(self, table):
        table.set_table_properties()
        props = table.delta_table.detail().select('properties').collect()[0][0]
        assert props.get('delta.dataSkippingNumIndexedCols', '') == '4'

    def test_get_optimization_recommendations(self, table):
        assert table.get_optimization_recommendations() is None
