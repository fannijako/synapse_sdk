import json

import pyspark.sql.functions as F # type: ignore

from datetime import datetime, timedelta
from typing import Iterator, Tuple, Union

from delta.tables import DeltaTable # type: ignore
from pyspark.sql import DataFrame, SparkSession # type: ignore


class Utils():
    def deep_ls(self, path: str, max_depth: int = 1) -> Iterator[str]:
        """
        List all files and folders in specified path and
        subfolders within maximum recursion depth.

        Args:
            path (str): path of the listing.
            max_depth (str, optional): depth of the listing. Defaults to 1.

        Returns:
            Iterator[str]: returns all files until max_depth has been reached.
        """

        folder = mssparkutils.fs.ls(path) # type: ignore

        for file in folder:
            if file.size != 0:
                yield file

        if max_depth > 1:
            for file in folder:
                if file.size != 0:
                    continue
                for directory in self.deep_ls(file.path, max_depth - 1):
                    yield directory

        else:
            for file in folder:
                if file.size == 0:
                    yield file

    def get_previous_date(days_back: int) -> str:
        """
        Calculate and return the date a specified number of days back from the current date.

        Args:
            days_back (int): The number of days to go back from the current date.

        Returns:
            str: The date in 'YYYY-MM-DD' format representing the date calculated days_back from today.
        """
        date_back = datetime.now() - timedelta(days=days_back)
        return date_back.strftime('%Y-%m-%d')

    def write_non_distributed_json(content: dict, target_path: str) -> None:
        """
        Writes a json file to abfss as per one file and not as a distributed json object.

        Args:
            content (dict): content of the file to be written.
            target_path (str): abfss:// path to write to.
        """

        file_name = target_path.split("/")[-1]
        temp_path = f"/tmp/{file_name}"

        with open(temp_path, 'w') as local_file:
            json.dump(content, local_file)

        mssparkutils.fs.cp('file:' + temp_path, target_path, recurse=False) # type: ignore


class Notebook(Utils):
    def __init__(self) -> None:
        self.workspace_name = mssparkutils.env.getWorkspaceName() # type: ignore
        _, self.data_product_name, self.environment, self.data_product_version = self.workspace_name.split('-')
        self.azure_storage_name = f"dls{self.data_product_name}{self.environment}{self.data_product_version}"
        self.curated_path = f"abfss://curated@{self.azure_storage_name}.dfs.core.windows.net"
        self.standardized_curated_path = f"{self.curated_path}/standardized"
        self.sensitive_standardized_curated_path = f"{self.curated_path}/sensitive-standardized"
        self.job_id = mssparkutils.env.getJobId() # type: ignore
        self.pool = mssparkutils.env.getPoolName() # type: ignore
        self.cluster = mssparkutils.env.getClusterId() # type: ignore
        self.notebook_name = mssparkutils.runtime.context.get('currentNotebookName') # type: ignore
        self.pipeline_job_id = mssparkutils.runtime.context.get('pipelinejobid') # type: ignore

        self.set_spark_datetime_settings()
        self.exit_values = {}

    def set_spark_datetime_settings(self) -> None:
        spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInRead" , "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.datetimeRebaseModeInWrite", "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInRead"    , "CORRECTED") # type: ignore
        spark.conf.set("spark.sql.legacy.parquet.int96RebaseModeInWrite"   , "CORRECTED") # type: ignore

    def set_exit_value(self, key: str, value: Union[str, list]) -> None:
        """
        Set or extend the exit values.
        Set:
            - if key did not exist yet
            - if key did exist and was a string
        Extend:
            - if key did exist and was a list and the new one is a list (extend)
            - if key did exist and was a list and the new one is a string (append)
        """

        if type(value) not in [str, list]:
            raise ValueError('value must be of type string or list')

        if key not in self.exit_values.keys():
            self.exit_values[key] = value
            return

        previous_value = self.exit_values.get(key)
        if type(previous_value) == str:
            self.exit_values[key] = value
            return

        if type(value) == list:
            previous_value.extend(value)
            self.exit_values[key] = previous_value
            return

        previous_value.append(value)
        self.exit_values[key] = previous_value

    def exit(self) -> None:
        """
        Exit the notebook with the previously set exit values
        """
        mssparkutils.notebook.exit(json.dumps(self.exit_values)) # type: ignore


class DataProduct(Notebook):
    def __init__(self) -> None:
        super().__init__()
        self.curated_tables = self.list_tables_in_curated()
        self.trusted_tables = {}
    
    def list_tables_in_curated(self) -> dict:
        """
        Create a dictionary of the available tables in curated with their metadata

        Returns: dict
            E.g. {'test_table': {'sensitivity': 'standardized',
                                'source': 'sap',
                                'database': 'x04_slt'}}            
        """

        table_list = [file.path
                      for file
                      in self.deep_ls(path = self.standardized_curated_path,
                                      max_depth = 3)
                      if file.path.endswith('.delta')]

        table_list.extend([file.path
                           for file
                           in self.deep_ls(path = self.sensitive_standardized_curated_path,
                                           max_depth = 3)
                           if file.path.endswith('.delta')])

        curated_dict = {}

        for table_path in table_list:
            _, _, _, sensitivity, source, database, table_name = table_path.split('/')
            table_name = table_name.replace('.delta', '')

            curated_dict.update({table_name: {'sensitivity': sensitivity,
                                              'source': source,
                                              'database': database}})
        
        return curated_dict
    
    def list_tables_in_trusted(self) -> dict:
        raise NotImplementedError

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


class Table(DataProduct):
    def __init__(self, name: str, load_type: str = None, layer: str = 'curated') -> None:
        super().__init__()
        self.name = name
        self.layer = layer
        self.sensitivity, self.source, self.database = self._find_sensitivity_source_database()
        self.path = f'{self.curated_path if layer == "curated" else self.trusted_path}/{self.sensitivity}/{self.source}/{self.database}/{self.name}.delta'
        self.DeltaTable = DeltaTable.forPath(spark, self.path) # type: ignore
        self.load_type = load_type if load_type else self._get_load_type()
        self.table_size = None
        self.target_file_size = None

    def _find_sensitivity_source_database(self) -> Tuple[str, str, str]:
        table = self.curated_tables.get(self.name)
        if not table:
            raise ValueError(f'Delta table with name {self.name} does not exist in the {self.layer} layer.')
        return table.get('sensitivity'), table.get('source'), table.get('database')

    def vacuum(self, hours: int = 168, force: bool = False) -> None:

        if hours < 168 and not force:
            raise ValueError('It is not recommended to VACUUM a delta table with retention lower than 7 days. If you want to continue either way, set the force parameter to True.')

        if hours < 168 and force:
            spark.conf.set("spark.databricks.delta.retentionDurationCheck.enabled", "false") # type: ignore

        self.DeltaTable.vacuum(retentionHours = hours)

    def zorder(self, columns: list, partition_filter: str = None) -> None:

        if len(columns) == 0:
            # TODO: recommend columns
            raise ValueError('Columns must be set')

        if not partition_filter:
            self.DeltaTable.optimize().executeZOrderBy(*columns)
        else:
            self.DeltaTable.optimize().where(partition_filter).executeZOrderBy(*columns)

    def optimize(self, partition_filter: str = None) -> None:

        if not partition_filter:
            self.DeltaTable.optimize().executeCompaction()
        else:
            self.DeltaTable.optimize().where(partition_filter).executeCompaction()

    def history(self, limit: int = 10) -> DataFrame:
        return self.DeltaTable.history(limit)

    def _get_load_type(self) -> str:
        """
        Get the load type of the table based on the most common operation type of the last 20 versions

        Returns: str
            Full or scd1
        """

        operations = [row.operation
                      for row
                      in self.history(20).select(F.col('operation')).collect()
                      if row.operation not in ['OPTIMIZE', 'VACUUM', 'RESTORE']]

        return 'scd1' if max(set(operations), key=operations.count) == 'MERGE' else 'full'
    
    def get_target_table_size(self) -> int:
        """
        Get the delta lake table size in bytes, using the DESCRIBE DETAIL command

        Returns:
            int: target table size in bytes
        """

        detail_df = self.DeltaTable.detail()
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

        self.target_file_size = target_file_size
        return target_file_size
    
    def calculate_enforce_save_target_table_metadata(self, print: bool = False) -> None:
        """
        Get the target Delta Lake table size in MB and 
        calculate the target file size, enforce it for rewrites and save the result to a json
        Enforce the target file size for this optimize  and for later writes
        with table property setting delta.targetFileSize
        Enable autoOptimize and autoCompact for setting the data layout for upcoming writes
        """

        target_file_size = self.target_file_size if self.target_file_size else self.calculate_target_file_size()

        # Set the table properties, so that the upcoming writes are using the same target file sizes
        # Effects optimize, zorder, autoopzimite and autocompact
        spark.sql(f"ALTER TABLE delta.`{self.path}` SET TBLPROPERTIES ('delta.targetFileSize'='{target_file_size}')") # type: ignore

        # Enable autooptimize, so that the later executions will write new files with target_file_size
        spark.sql(f"ALTER TABLE delta.`{self.path}` SET TBLPROPERTIES ('delta.autoOptimize.optimizeWrite'='true')") # type: ignore

        if print:
            details = self.DeltaTable.detail()
            print(f"Table properties for {path}: {details.select('properties').collect()[0][0]}") 
   
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

        nbr_rows = self.dataframe.count()

        zorder_columns = {}
        analyse_columns = []

        for column in primary_keys:
            # Calculate the distinct values in the current column and calculate its ratio over the number of rows
            nbr_distinct = self.dataframe.agg(F.approx_count_distinct(column).alias('count')).collect()[0][0]
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
                spark.sql(f"ALTER TABLE delta.`{self.path}` SET TBLPROPERTIES ('delta.dataSkippingNumIndexedCols'='{nbr_column_statistics}')") # type: ignore

            nbr_columns = len(self.dataframe.schema)

            return ','.join(zorder_columns), ','.join(analyse_columns), nbr_column_statistics, nbr_columns

        except Exception:
            return '', '', 32, 9999

    def set_table_properties(self):
        """
        Using the previous methods
        """
        raise NotImplementedError

    def copy_prod_data_to_dev(self):
        raise NotImplementedError
    
    def get_optimization_recommendations(self):
        """
        E.g. run an optimize, run a vacuum or use the following spark configs while reading
        """
        raise NotImplementedError


class DataFrame(Table):
    def __init__(self, name: str, load_type: str = None, layer: str = 'curated', version: int = None, timestamp: str = None) -> None:
        super().__init__(name = name, load_type = load_type, layer = layer)
        self.version = version
        self.timestamp = timestamp
        self.load_dataframe()
        self.version = self.get_version()

    def load_dataframe(self) -> None:
        if self.version and self.timestamp:
            raise ValueError("Can't set both version and timestamp")
        if not self.version and not self.timestamp:
            self.dataframe = spark.read.format('delta').load(self.path) # type: ignore
        elif self.version:
            self.dataframe = spark.read.format('delta').option('versionAsOf', self.version).load(self.path) # type: ignore
        elif self.timestamp:
            self.dataframe = spark.read.format('delta').option('timestampAsOf', self.timestamp).load(self.path) # type: ignore

    def get_version(self) -> int:
        return self.version if self.version else int(self.history(1).select('version').collect()[0][0])

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
    def __init__(self) -> None:
        super().__init__()
        self.key_vault_name = f'kv{self.data_product_name}{self.data_product_version}'
    
    def get_secret(self, secret_name: str) -> str:
        raise NotImplementedError


class aSQLDatabase(Notebook):
    def __init__(self, database_name: str, database_schema: str) -> None:
        super().__init__()
        self.database_server = f'sql-{self.data_product_name}-we-{"nonprod" if self.environment == "d" else "prod"}.database.windows.net:1433'
        self.database_name = database_name
        self.database_schema = database_schema
        self.asql_database_linked_service_name = f'ls_asql_{self.data_product_name}'
    
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
