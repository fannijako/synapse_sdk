import json

import pyspark.sql.functions as F # type: ignore

from datetime import datetime, timedelta
from typing import Iterator, Tuple, Union

from delta.tables import DeltaTable # type: ignore
from pyspark.sql import DataFrame # type: ignore


class PositiveNumber:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, int | float) or value <= 0:
            raise ValueError("positive number expected")
        instance.__dict__[self._name] = value


class StringValue:
    def __set_name__(self, owner, name):
        self._name = name

    def __get__(self, instance, owner):
        return instance.__dict__[self._name]

    def __set__(self, instance, value):
        if not isinstance(value, str):
            raise ValueError("string expected")
        instance.__dict__[self._name] = value


class Utils(object):
    _instance = None

    def __new__(cls):
         if not cls._instance:
             cls._instance = super().__new__(cls)
         return cls._instance

    def __str__(cls) -> str:
        return f'Utils class with methods: {cls.__dict__}'

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def deep_ls(self, path: str, max_depth: int = 1) -> Iterator[str]:
        """
        List all files and folders in specified path and
        subfolders within maximum recursion depth.

        Args:
            path (str): path of the listing
            max_depth (str, optional): depth of the listing
                Defaults to 1

        Returns:
            Iterator[str]: returns an iterator with all files until max_depth has been reached
        """

        for file in  mssparkutils.fs.ls(path): # type: ignore
            if file.size != 0:
                yield file
            elif max_depth > 1:
                yield from self.deep_ls(file.path, max_depth - 1)
            else:
                yield file

    def get_previous_date(days_back: int) -> str:
        return (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')

    def write_non_distributed_json(content: dict, target_path: str) -> None:
        """
        Writes a json file to abfss as per one file and not as a distributed json object.

        Args:
            content (dict): content of the file to be written
            target_path (str): abfss:// path to write to
        """

        temp_path = f"/tmp/{target_path.split("/")[-1]}"
        with open(temp_path, 'w') as local_file:
            json.dump(content, local_file)

        mssparkutils.fs.cp('file:' + temp_path, target_path, recurse=False) # type: ignore


class Notebook(Utils):
    exit_values = {}

    def __init__(self):
        self._workspace_name = mssparkutils.env.getWorkspaceName() # type: ignore
        _, self._data_product_name, self._environment, self._data_product_version = self._workspace_name.split('-')
        self._construct_paths()

        self._notebook_name = mssparkutils.runtime.context.get('currentNotebookName') # type: ignore
        
        self._job_id = mssparkutils.env.getJobId() # type: ignore
        self._pipeline_job_id = mssparkutils.runtime.context.get('pipelinejobid') # type: ignore
        self._pool = mssparkutils.env.getPoolName() # type: ignore
        self._cluster = mssparkutils.env.getClusterId() # type: ignore

        self.set_spark_datetime_settings()

    @property
    def workspace_name(self):
        return self._workspace_name

    @workspace_name.setter
    def workspace_name(self, value):
        raise ValueError(f"""Workspace_name can't be changed to {value}. Workspace name is extraced using the mssparkutils library.
                             You can manually change the data_product_name, environment and data_product_version attributes
                             if you would like to work with data from a different data product or environment.
                          """)

    @property
    def data_product_name(self):
        return self._data_product_name

    @data_product_name.setter
    def data_product_name(self, value):
        if not isinstance(value, str):
            raise ValueError("Data_product_name attribute must be a string.")

        if value != self._data_product_name:
            print(f"""Data product name is by default extracted from the workspace name ({self._workspace_name}).
                      Current value is {self._data_product_name}, which you'll overwrite.
                      The path properties will be recalculated by this operation as well.
                      New values will be:
                        data_product_name: {value}
                        environment: {self._environment}
                        data_product_version: {self._data_product_version}
                   """)
            self._data_product_name = value
            self._construct_paths()
        else:
            print("Data_product_name attribute is already set to the same value.")

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, value):
        if value not in ['p', 'd']:
            raise ValueError("Environment attribute must be either p or d.")

        if value == self._environment:
            print("Environment attribute is already set to the same value.")

        if value == 'd':
            print("You can't work with dev data in the prod workspace.")
            return

        print(f"""Environment is by default extracted from the workspace name ({self._workspace_name}).
                  Current value is d, which you'll overwrite to p for prod.
                  You'll be working with prod data in the dev workspace.

                  The path properties will be recalculated by this operation as well.
                  New values will be:
                        data_product_name: {self._data_product_name}
                        environment: {value}
                        data_product_version: {self._data_product_version}
               """)
        self._environment = value
        self._construct_paths()

    @property
    def data_product_version(self):
        return self._data_product_version

    @data_product_version.setter
    def data_product_version(self, value):
        if not isinstance(value, str) or len(value) != 3:
            raise ValueError("data_product_version attribute needs to be a 3 character long string.")

        if value == self._data_product_version:
            print("Data_product_version attribute is already set to the same value.")
            return

        print(f"""Data_product_version is by default extracted from the workspace name ({self._workspace_name}).
                  Current value is {self._data_product_version}, which you'll overwrite.
                  The path properties will be recalculated by this operation as well.
                  New values will be:
                        data_product_name: {self._data_product_name}
                        environment: {self._environment}
                        data_product_version: {value}
               """)
        self._data_product_version = value
        self._construct_paths()

    @property
    def notebook_name(self):
        return self._notebook_name

    @property
    def job_id(self):
        return self._job_id

    @property
    def pipeline_job_id(self):
        return self._pipeline_job_id

    @property
    def pool(self):
        return self._pool

    @property
    def cluster(self):
        return self._cluster

    def _construct_paths(self) -> None:
        self._azure_storage_name = f"dls{self._data_product_name}{self._environment}{self._data_product_version}"
        self._curated_path = f"abfss://curated@{self._azure_storage_name}.dfs.core.windows.net"
        self._standardized_curated_path = f"{self._curated_path}/standardized"
        self._sensitive_standardized_curated_path = f"{self._curated_path}/sensitive-standardized"
        self._trusted_path = f"abfss://trusted@{self._azure_storage_name}.dfs.core.windows.net"

    @property
    def azure_storage_name(self):
        return self._azure_storage_name

    @azure_storage_name.setter
    def azure_storage_name(self, value):
        raise ValueError(f"""Azure_storage_name can't be changed manually to {value}.
                             Set the data_product_name, environment and data_product_version attributes
                             and the storage_account_name attribute will be set accordingly.""")

    @property
    def curated_path(self):
        return self._curated_path

    @curated_path.setter
    def curated_path(self, value):
        raise ValueError(f"""Curated_path can't be changed manually to {value}.
                             Set the data_product_name, environment and data_product_version attributes
                             and the curated_path attribute will be set accordingly.""")

    @property
    def standardized_curated_path(self):
        return self._standardized_curated_path

    @standardized_curated_path.setter
    def standardized_curated_path(self, value):
        raise ValueError(f"""Standardized_curated_path can't be changed manually to {value}.
                             Set the data_product_name, environment and data_product_version attributes
                             and the standardized_curated_path attribute will be set accordingly.""")

    @property
    def sensitive_standardized_curated_path(self):
        return self._sensitive_standardized_curated_path

    @sensitive_standardized_curated_path.setter
    def sensitive_standardized_curated_path(self, value):
        raise ValueError(f"""Sensitive_standardized_curated_path can't be changed manually to {value}.
                             Set the data_product_name, environment and data_product_version attributes
                             and the sensitive_standardized_curated_path attribute will be set accordingly.""")

    @property
    def trusted_path(self):
        return self._trusted_path

    @trusted_path.setter
    def trusted_path(self, value):
        raise ValueError(f"""Trusted_path can't be changed manually to {value}.
                             Set the data_product_name, environment and data_product_version attributes
                             and the trusted_path attribute will be set accordingly.""")

    def __eq__(self, other_notebook) -> bool:

        same_workspace_name = self._workspace_name == other_notebook.workspace_name
        same_job_id = self.job_id == other_notebook.job_id
        same_notebook_name = self.notebook_name and other_notebook.notebook_name
        same_pipeline_job_id = self.pipeline_job_id and other_notebook.pipeline_job_id
        same_pool = self.pool and other_notebook.pool
        same_cluster = self.cluster and other_notebook.cluster

        return same_workspace_name and same_job_id and same_notebook_name and same_pipeline_job_id and same_pool and same_cluster

    def __str__(self) -> str:
        return f'{self.notebook_name} in {self._workspace_name} executed by {self.job_id if self.job_id else self.pipeline_job_id}'

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"

    def set_spark_datetime_settings(self) -> None:
        spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead" , "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead"    , "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite"   , "CORRECTED") # type: ignore

    @classmethod
    def set_exit_value(cls, key: str, value: Union[str, list]) -> None:
        """
        Set or extend the exit values.
        Set:
            - if key did not exist yet
            - if key did exist and was a string
        Extend:
            - if key did exist and was a list and the new one is a list (extend)
            - if key did exist and was a list and the new one is a string (append)
        """

        if not isinstance(value, str | list):
            raise ValueError('value must be of type string or list')

        if key not in cls.exit_values.keys():
            cls.exit_values[key] = value
            return

        previous_value = cls.exit_values.get(key)
        if isinstance(previous_value, str):
            cls.exit_values[key] = value
            return

        if isinstance(previous_value, list):
            previous_value.extend(value)
            cls.exit_values[key] = previous_value
            return

        previous_value.append(value)
        cls.exit_values[key] = previous_value

    def exit(self) -> None:
        """
        Exit the notebook with the previously set exit values
        """
        mssparkutils.notebook.exit(json.dumps(cls.exit_values)) # type: ignore


class DataProduct(Notebook):
    def __init__(self):
        super().__init__()
        self.curated_tables = self.list_tables_in_curated()
        self.trusted_tables = self.list_tables_in_trusted()

    def __eq__(self, other_data_product) -> bool:
        return self.azure_storage_name == other_data_product.azure_storage_name

    def __contains__(self, table: str) -> bool:
            return table in self.curated_tables.keys() or table in self.trusted_tables.keys()

    def __str__(self) -> str:
        return f'{self.data_product_name} data product version {self.data_product_version}'

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
    
    def get_all_deltas(self, path_list: list[str], max_depth: int = 3) -> dict:
        """
        Create a dictionary of the available tables with their path

        Returns: dict
            E.g. {'test_table': 'abfss://curated@dlstiscd002@dfs.windows.core.net/standardized/sap/x04_slt/test_table.delta'}            
        """

        table_list = [
            file.path
            for path in path_list
            for depth in range(max_depth)
            for file in self.deep_ls(path = path, max_depth = depth)
            if file.path.endswith('.delta')
        ]

        return {
            table_path.split('/')[-1].replace('.delta', ''): {'url': table_path}
            for table_path in table_list
        }


    def list_tables_in_curated(self) -> dict:
        return self.get_all_deltas([self._standardized_curated_path, self._sensitive_standardized_curated_path])
    
    def list_tables_in_trusted(self) -> dict:
        return self.get_all_deltas([self._trusted_path], max_depth = 4)

    def optimize_all(self, layer: str = 'curated', partition_filter: str = None):
        """
        If layer is None, optimize curated and trusted, else the specified layer

        Example usage:
            DataProduct().optimize_all()
            Which runs a OPTIMIZE command on all delta tables in the curated layer without a partition filter.
        """

        def execute_layer(table_names: list, layer: str):
            for table_name in table_names:
                table = Table(table_name, layer = layer)
                table.optimize(partition_filter = partition_filter)

        if layer == 'curated' or layer is None:
            execute_layer(self.curated_tables.keys(), 'curated')

        if layer == 'trusted' or layer is None:
            execute_layer(self.trusted_tables.keys(), 'trusted')

    def vacuum_all(self, layer: str = 'curated', hours: int = 168, force: bool = False):
        """
        If layer is None, vacuum curated and trusted, else the specified layer

        Example usage:
            DataProduct().vacuum_all()
            Which runs a VACUUM command with 7 days retention on all delta tables in the curated layer.
        """

        spark.conf.set("spark.databricks.delta.vacuum.parallelDelete.enabled", "true") # type: ignore
        def execute_layer(table_names: list, layer: str):
            for table_name in table_names:
                table = Table(table_name, layer = layer)
                table.vacuum(hours = hours, force = force)

        if layer == 'curated' or layer is None:
            execute_layer(self.curated_tables.keys(), 'curated')

        if layer == 'trusted' or layer is None:
            execute_layer(self.trusted_tables.keys(), 'trusted')


class DataPlaceholder(DataProduct):
    load_type = StringValue()

    def __init__(self, name: str, load_type: str = None, layer: str = 'curated'):

        if not isinstance(name, str):
            raise ValueError('String expected for name.')
        if layer not in ['curated', 'trusted']:
            raise ValueError('Layer must be curated or trusted.')
        if not isinstance(load_type, str | None):
            raise ValueError('String expected for load_type.')

        super().__init__()
        
        self._name = name
        self._layer = layer
        self.load_type = load_type

        self._path = self._find_path()

    @property
    def name(self):
        return self._name

    @property
    def layer(self):
        return self._layer

    @property
    def path(self):
        return self._path

    def _find_path(self) -> Tuple[str, str, str]:
        if self.name in self.curated_tables and self.layer == 'curated':
            return self.curated_tables.get(self._name)

        if self.name in self.trusted_tables and self.layer == 'trusted':
            return self.trusted_path.get(self._name)

        raise ValueError(f'Delta table with name {self.name} does not exist in the {self.layer} layer.')

    def __eq__(self, other_table) -> bool:
        return self.super() == other_table.super() and self._name == other_table.name and self._layer == other_table.layer


class Table(DataPlaceholder):
    table_size = PositiveNumber()
    target_file_size = StringValue()

    def __init__(self, name: str, load_type: str = None, layer: str = 'curated'):
        super().__init__(name = name, load_type = load_type, layer = layer)
        self.calculate_table_properties()

    def calculate_table_properties(self):
        self._DeltaTable = self._get_delta_table()
        self.load_type = self.load_type if self.load_type else self._get_load_type()
        self._dataframe = DataFrame(name = self._name, layer = self._layer, load_type = self._load_type)
        self.table_size = self.get_target_table_size()
        self.target_file_size = self.calculate_target_file_size()

    @property
    def DeltaTable(self):
        return self._DeltaTable

    @property
    def dataframe(self):
        return self._dataframe

    def _get_delta_table(self):
        self._DeltaTable = DeltaTable.forPath(spark, self.path) # type: ignore

    def _get_load_type(self) -> str:
        """
        Get the load type of the table based on the most common operation type of the last 20 versions

        Returns: str
            Full or scd1
        """

        operations = [row.operation
                      for row
                      in self.history(20).select(F.col('operation')).collect()
                      if row.operation in ['MERGE', 'WRITE']]

        return 'scd1' if max(set(operations), key=operations.count) == 'MERGE' else 'full'
    
    def get_target_table_size(self) -> int:
        """
        Get the delta lake table size in bytes, using the DESCRIBE DETAIL command

        Returns:
            int: target table size in bytes
        """

        detail_df = self._DeltaTable.detail()
        table_size = detail_df.select('sizeInBytes').collect()[0][0]
        self.table_size = table_size
        return table_size

    def calculate_target_file_size(self) -> str:
        """
        Generate the target file size for rewrites value based on the followint recommendations:
            - 128 MB - below 10 GB
            - 256 MB - below 3 TB
            - 512 MB - below 10 TB
            - 1 GB - above 10 TB
        Returns value in a format that can be used with the spark configuration settings

        Returns:
            str: target table size in MB
        """

        target_table_size = self.table_size if self.table_size else self.get_target_table_size()
        size_in_gb = target_table_size / 1024 / 1024 / 1024

        if size_in_gb < 10:
            target_file_size = '128mb'
        if size_in_gb < 3072:
            target_file_size = '256mb'
        if size_in_gb < 10240:
            target_file_size = '526mb'
        else:
            target_file_size = '1024mb'

        self._target_file_size = target_file_size
        return target_file_size

    def __str__(self) -> str:
        return f"{self.data_product_name} data product's {self._name} table in {self._layer} layer"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name='{self._name}', load_type={self._load_type}, layer={self._layer})"

    def vacuum(self, hours: int = 168, force: bool = False) -> None:

        if hours < 168 and not force:
            raise ValueError('It is not recommended to VACUUM a delta table with retention lower than 7 days. If you want to continue either way, set the force parameter to True.')

        if hours < 168 and force:
            spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false") # type: ignore

        self._DeltaTable.vacuum(retentionHours = hours)

    def zorder(self, columns: list, partition_filter: str = None) -> None:

        if len(columns) == 0:
            # TODO: recommend columns
            raise ValueError('Columns must be set')

        if not partition_filter:
            self._DeltaTable.optimize().executeZOrderBy(*columns)
        else:
            self._DeltaTable.optimize().where(partition_filter).executeZOrderBy(*columns)

    def optimize(self, partition_filter: str = None) -> None:

        if not partition_filter:
            self._DeltaTable.optimize().executeCompaction()
        else:
            self._DeltaTable.optimize().where(partition_filter).executeCompaction()

    def history(self, limit: int = 10) -> DataFrame:
        return self._DeltaTable.history(limit)
    
    def calculate_enforce_save_target_table_metadata(self) -> None:
        """
        Get the target Delta Lake table size in MB and 
        calculate the target file size, enforce it for rewrites and save the result to a json
        Enforce the target file size for this optimize  and for later writes
        with table property setting delta.targetFileSize
        Enable autoOptimize and autoCompact for setting the data layout for upcoming writes
        """

        # Set the table properties, so that the upcoming writes are using the same target file sizes
        # Effects optimize, zorder, autoopzimite and autocompact
        spark.sql(f"ALTER TABLE delta.`{self._path}` SET TBLPROPERTIES ('delta.targetFileSize'='{self._target_file_size}')") # type: ignore

        # Enable autooptimize, so that the later executions will write new files with target_file_size
        spark.sql(f"ALTER TABLE delta.`{self._path}` SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite'='true')") # type: ignore
   
    def calculate_zorder_and_analyse_columns(self, primary_keys: list[str]) -> tuple[list[str], list[str]]:
        """
        Select column candidates for Z-ORDER BY and ANALYZE from the primary keys
        Specifications for Z-ORDER BY:
            - returns at most 4 columns
            - returns only high cardinality columns
                threshold: 0.01%
                statistic: number of distinct values / number of rows
                threshold: 10 distinct values
        Specification for ANALYZE:
            - primary key
            - not Z-ORDER BY
            - more than 1 distinct values

        Args:
            primary_keys (list[str]): list of primary keys of the table.

        Returns:
            list[str]: list of column names to use in Z-ORDERING.
            list[str]: list of column names to calculate statistics about other than the Z-ORDERING columns.
        """

        nbr_rows = self._dataframe.count()

        zorder_columns = {}
        analyse_columns = []

        for column in primary_keys:
            # Calculate the distinct values in the current column and calculate its ratio over the number of rows
            nbr_distinct = self._dataframe.agg(F.approx_count_distinct(column).alias('count')).collect()[0][0]
            ratio = nbr_distinct / nbr_rows

            # If the ratio is at least 0.01% and has at least 10 distinct values, add it to the possible z-ordering columns
            if ratio >= 0.0001 and nbr_distinct >= 10:
                zorder_columns[column] = ratio

            # If it is not added to the possible z-ordering columns but is not constant, add it to the analyse columns
            elif nbr_distinct > 1:
                analyse_columns.append(column)

        # Sort the possible z-ordering columns based on the ratio
        zorder_columns_sorted = sorted(zorder_columns, key = lambda col: zorder_columns.get(col))
        zorder_columns = zorder_columns_sorted[0:4]

        if len(zorder_columns_sorted) > 4:
            analyse_columns.extend(zorder_columns_sorted[4:])

        self.zorder_columns = zorder_columns
        self.analyse_columns = analyse_columns
        return zorder_columns, analyse_columns
    
    def calculate_statistics(self, primary_keys: list[str], alter_statistics_number: bool = False) -> tuple[str, str, int, int]:
        """
        Calculate the following statistics:
            - z-order columns
            - analyse columns
            - number of columns to calculate statistics on
            - number of columns
        
        Args:
        path (str): path of the delta lake in abfss:// format.
        primary_keys (list[str]): list of primary keys of the table.
        alter_statistics_number (bool, optional): whether to change the table property of delta.dataSkippingNumIndexedCols to the calculated nbr_column_statistics or not. Defaults to False.

        Returns:
        str: column names to use in Z-ORDERING separated by ','. Defaults to ''.
        str: column names to calculate statistics about other than the Z-ORDERING column separated by ','. Defaults to ''.
        int: number of columns to calculate statistics about. Defaults to 32.
        int: number of columns in the table. Defaults to 9999.
        """

        try:
            zorder_columns, analyse_columns = self.calculate_zorder_and_analyse_columns(primary_keys)

            nbr_column_statistics = len(zorder_columns) + len(analyse_columns)
            if alter_statistics_number:
                spark.sql(f"ALTER TABLE delta.`{self._path}` SET TBLPROPERTIES ('delta.dataSkippingNumIndexedCols'='{nbr_column_statistics}')") # type: ignore

            nbr_columns = len(self._dataframe.schema)

            return ','.join(zorder_columns), ','.join(analyse_columns), nbr_column_statistics, nbr_columns

        except Exception:
            return '', '', 32, 9999

    def set_table_properties(self):
        """
        Using the previous methods
        """
        raise NotImplementedError
    
    def get_optimization_recommendations(self):
        """
        E.g. run an optimize, run a vacuum or use the following spark configs while reading
        """
        raise NotImplementedError


class DataFrame(DataProduct):
    file_format = 'delta'
    version = PositiveNumber()
    timestamp = StringValue()

    def __init__(self, name: str, load_type: str = None, layer: str = 'curated', version: int = None, timestamp: str = None):

        if not isinstance(timestamp, str | None):
            raise ValueError('String expected for timestamp.')
        if self.version and self.timestamp:
            raise ValueError("Can't set both version and timestamp")

        super().__init__(name = name, load_type = load_type, layer = layer)

        self.latest_version = self.get_version()
        self.version = version
        self.timestamp = timestamp

        self.load_dataframe()

    def __eq__(self, other_dataframe) -> bool:

        same_super = self.super() == other_dataframe.super()
        same_version = self.version == other_dataframe.version
        same_timestamp = self.timestamp == other_dataframe.timestamp

        return same_super and same_version and same_timestamp

    def __lt__(self, other_dataframe: DataFrame) -> bool:
        if not self.super() == other_dataframe.super():
            raise ValueError('< operator only supported between different versions of the same table')
        return  self.version < other_dataframe.version

    def __le__(self, other_dataframe: DataFrame) -> bool:
        if not self.super() == other_dataframe.super():
            raise ValueError('<= operator only supported between different versions of the same table')
        return  self.version <= other_dataframe.version

    def __gt__(self, other_dataframe: DataFrame) -> bool:
        if not self.super() == other_dataframe.super():
            raise ValueError('> operator only supported between different versions of the same table')
        return  self.version > other_dataframe.version

    def __ge__(self, other_dataframe: DataFrame) -> bool:
        if not self.super() == other_dataframe.super():
            raise ValueError('>= operator only supported between different versions of the same table')
        return  self.version >= other_dataframe.version

    def __add__(self, version_increase: int) -> DataFrame:
        return DataFrame(name = self.name, load_type = self.load_type, layer = self.layer, version = self.version + version_increase)
    
    def __sub__(self, version_decrease: int) -> DataFrame:
        return DataFrame(name = self.name, load_type = self.load_type, layer = self.layer, version = self.version - version_decrease)

    def __str__(self) -> str:
        return f"{self.data_product_name} data product's {self.name} table in {self.layer} layer as a dataframe for version {self.version}"

    def __repr__(self) -> str:
        return f"{type(self).__name__}(name='{self.name}', load_type={self.load_type}, layer={self.layer}, version={self.version}, timestamp={self.timestamp})"

    def load_dataframe(self) -> None:
        if not self.version and not self.timestamp:
            self.dataframe = spark.read.format('delta').load(self.path) # type: ignore
        elif self.version:
            self.dataframe = spark.read.format('delta').option('versionAsOf', self.version).load(self.path) # type: ignore
        elif self.timestamp:
            self.dataframe = spark.read.format('delta').option('timestampAsOf', self.timestamp).load(self.path) # type: ignore

    def get_version(self) -> int:
        return int(self.history(1).select('version').collect()[0][0])

    def load_version_minus_n(self, timetravel: int = 1) -> DataFrame:
        return DataFrame(name = self.name, load_type = self.load_type, layer = self.layer, version = self.version - timetravel)

    def is_changed_since_last_version(self, columns_to_ignore: list = None) -> bool:
        not_existing_columns = [col for col in columns_to_ignore if col not in self.dataframe.columns]
        if len(not_existing_columns) != 0:
            raise ValueError(f'{", ".join(not_existing_columns)} are not present in the dataframe, with columns {self.dataframe.columns}')

        version_minus_one = self.load_version_minus_n(timetravel = 1)

        current_version_count_distinct = self.dataframe.drop(*columns_to_ignore).distinct().count()
        new_version_count_distinct = version_minus_one.dataframe.drop(*columns_to_ignore).distinct().count()

        if current_version_count_distinct != new_version_count_distinct:
            return True

        unioned_df = self.dataframe.drop(*columns_to_ignore).unionByName(version_minus_one.dataframe.drop(*columns_to_ignore))
        unioned_count_distinct = unioned_df.distinct().count()

        return unioned_count_distinct != new_version_count_distinct

    def write_to_database(self,
                          database_name: str,
                          database_schema: str,
                          table_name: str = None,
                          create_table_statement: str = "",
                          mode: str = 'auto'):

        if mode not in ['append', 'overwrite', 'auto']:
            raise ValueError('Mode must be append or overwrite')

        if mode == 'auto':
            mode = 'append' if self.load_type == 'scd1' else 'overwrite'

        asql_database = aSQLDatabase(database_name, database_schema)
        table_name = table_name if table_name else self.name
        connectionProperties, url, dbtable = asql_database.build_connection_properties(database_table = table_name)
        (self.dataframe.write
                       .option("createTableOptions", create_table_statement)
                       .jdbc(url = url,
                             table=dbtable,
                             mode=mode,
                             properties=connectionProperties
                            )
                    )

    def rename_columns(self):
        """
        From generic utils
        """
        raise NotImplementedError

    def add_timestamp_column(self, timestamp_column_name: str = "load_timestamp", timezone: str = None, timestamp_format: str = 'yyyy-MM-dd HH:mm:ss') -> None:
        """
        Adds a timestamp column to a PySpark DataFrame with an optional timezone and custom format.

        Args:
            timestamp_column_name (str, optional): the name for the new timestamp column. Defaults to 'load_timestamp'
            timezone (str, optional): the timezone to which the timestamp will be converted. Defaults to None.
            timestamp_format (str, optional): the format for the timestamp column. Defaults to 'yyyy-MM-dd HH:mm:ss'.

        Raises:
            ValueError: if the provided column name already exists in the DataFrame to prevent value loss.
        """

        if timestamp_column_name in self.dataframe.columns:
            raise ValueError("The provided column name already exists in the DataFrame.")

        # Add the current timestamp column in UTC
        self.dataframe = self.dataframe.withColumn(timestamp_column_name, F.current_timestamp())
        
        # If a timezone is provided, convert the timestamp to the given timezone
        if timezone:
            self.dataframe = self.dataframe.withColumn(
                timestamp_column_name,
                F.from_utc_timestamp(F.col(timestamp_column_name), timezone)
            )
        
        # Apply the specified timestamp format
        self.dataframe = self.dataframe.withColumn(
            timestamp_column_name,
            F.date_format(F.col(timestamp_column_name), timestamp_format)
        )

    def add_hash_column(self, prefix: str = 'dap') -> None:
        """
        Add a hash column to a Spark DataFrame by concatenating all columns and applying SHA-256 hashing.
        The name of the hash column will be based on the provided prefix (e.g., 'dap_hash' for 'dap' prefix).

        This function concatenates all columns of the input DataFrame into a single string for each row,
        applies SHA-256 hashing to these strings, and adds the hash as a new column. The name of this
        new column is constructed using the given prefix followed by '_hash'.

        Parameters:
            prefix (str, optional): The prefix for the hash column name. Defaults to 'dap'.

        Raises:
            ValueError: if the provided column name already exists in the DataFrame to prevent value loss.
        """

        if f"{prefix}_hash" in self.dataframe.columns:
            raise ValueError("The provided column name already exists in the DataFrame.")
        
        concatenated_cols = F.concat(*[self.dataframe[col] for col in self.dataframe.columns])
        self.dataframe = self.dataframe.withColumn(f"{prefix}_hash", F.sha2(concatenated_cols, 256))

    def rename_columns_w_pattern(self, pattern_to_replace: str, replace_to: str = "") -> None:
        """
        Rename the column names based on the given pattern. It removes the pattern by default.

        Args:
            pattern_to_replace (str): The string pattern to replace.
            replace_to (str, optional): The new string.
        """

        for colname in self.dataframe.columns:
            self.dataframe = self.dataframe.withColumnRenamed(colname, colname.replace(pattern_to_replace, replace_to))
    
    def rename_columns_w_mapping(self, column_names: dict) -> None:
        """
        Apply the renaming to each column in the dictionary.
        
        Args:
            column_names (dict): The mapping dictionary. Example:
                df_mapping = {
                    'current_col_name': 'new_col_name',
                    'current_col_name2': 'new_col_name2'
                }
        """

        for column_old_name, column_new_name in column_names.items():
            self.dataframe = self.dataframe.withColumnRenamed(column_old_name, column_new_name)
    
    def cast_data_columns(self, column_types: dict) -> None:
        """
        Apply the casting to each column in the dictionary.
        
        Args:
            column_types (dict): The column types dictionary. Example:
                df_cast = {
                    'col_name': IntegerType(),
                    'col_name2': StringType()
                }
        """

        for column_name, column_type in column_types.items():
            self.dataframe = self.dataframe.withColumn(column_name, F.col(column_name).cast(column_type))
    
    @staticmethod
    def construct_merge_condition(pk: str, separator: str=',') -> str:
        """
        Constructs the merge condition from the given primary keys.

        Args:
            pk (str): The primary keys separated 
            separator (str, optional): The separator between the primary keys. The default value is ','.
        
        Returns:
            str: The merge condition.
        """
        pk_array = pk.split(separator)
        condition = " AND ".join([f"src.{pk.strip()} <=> dst.{pk.strip()}" for pk in pk_array])
        
        return condition
    
    def write_to_excel(self, target_path: str) -> None:
        """
        Write the joined data to the target path in Excel format

        Args:
            target_path (str): abfss:// path to write the result to
        """
    
        temp_path = f"/tmp/{target_path.split('/')[-1]}"

        self.dataframe.pandas_api().to_excel(temp_path, index=False, engine='openpyxl')
        mssparkutils.fs.cp('file:' + temp_path, target_path, recurse=False) # type: ignore


class KeyVault(Notebook):
    key_vault_name = StringValue()

    def __init__(self):
        super().__init__()
        self.key_vault_name = f'kv{self.data_product_name}{self.data_product_version}'

    def __eq__(self, other_keyvault) -> bool:
        return self.key_vault_name == other_keyvault.key_vault_name

    def __str__(self) -> str:
        return f'Key Vault linked service {self.key_vault_name}'

    def __repr__(self) -> str:
        return f"{type(self).__name__}()"
    
    def get_secret(self, secret_name: str) -> str:
        raise NotImplementedError


class aSQLDatabase(Notebook):
    database_name = StringValue()
    database_schema = StringValue()
    database_server = StringValue()
    asql_database_linked_service_name = StringValue()

    def __init__(self, database_name: str, database_schema: str):

        super().__init__()

        self.database_name = database_name
        self.database_schema = database_schema

        self.database_server = f'sql-{self.data_product_name}-we-{"nonprod" if self.environment == "d" else "prod"}.database.windows.net:1433'
        self.asql_database_linked_service_name = f'ls_asql_{self.data_product_name}'

    def __eq__(self, other_database) -> bool:

        same_database_server = self.database_server == other_database.database_server
        same_database_name = self.database_name == other_database.database_name
        same_database_schema = self.database_schema == other_database.database_schema
        same_asql_database_linked_service_name = self.asql_database_linked_service_name == other_database.asql_database_linked_service_name

        return same_database_server and same_database_name and same_database_schema and same_asql_database_linked_service_name

    def __str__(self) -> str:
        return f'Azure SQL database linked service to the {self.database_schema} in {self.database_name} database'

    def __repr__(self) -> str:
        return f"{type(self).__name__}(database_name='{self.database_name}', database_schema={self.database_schema})"
    
    def get_token(self) -> str:
        return TokenLibrary.getConnectionString(self.asql_database_linked_service_name) # type: ignore

    def build_connection_properties(self, database_table: str) -> Tuple[dict, str, str]:

        url = f"jdbc:sqlserver://{self.database_server};databaseName={self.database_name};encrypt=true;trustServerCertificate=false;hostNameInCertificate=*.database.windows.net;loginTimeout=30"
        dbtable = self.database_schema + "." + database_table
        connectionProperties = {
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver",
            "url": url,
            "dbtable": dbtable,
            "accessToken": self.get_token()
            }
        
        return connectionProperties, url, dbtable
