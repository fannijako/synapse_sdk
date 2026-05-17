import mssparkutils # type: ignore # pylint: disable=import-error

DAG = { "activities": [{"name": "utils",
                        "path": "test_utils",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "notebook",
                        "path": "test_notebook",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "table",
                        "path": "test_table",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "data_product",
                        "path": "test_data_product",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "dataframe",
                        "path": "test_dataframe",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "keyvault",
                        "path": "test_keyvault",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "asql",
                        "path": "test_asql_database",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "azureml",
                        "path": "test_azureml",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "kusto",
                        "path": "test_kusto",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        },
                        {"name": "synstorage",
                        "path": "test_synstorage",
                        "timeoutPerCellInSeconds": 600, # 10 minutes timeout per cell
                        "retry": 0
                        }
                        ],
        "timeoutInSeconds": 3600, # 60 minutes timeout for the notebook
        "concurrency": 1
      }

mssparkutils.notebook.runMultiple(DAG) # type: ignore

TEST_FOLDER = 'abfss://curated@dlstiscd001.dfs.core.windows.net/generic_utils/'
mssparkutils.fs.rm(TEST_FOLDER, True) # type: ignore
