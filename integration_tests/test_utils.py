from ..synapse_notebooks.generic_utils import Utils

from datetime import datetime, timedelta # pylint: disable=wrong-import-order

CURATED = 'abfss://curated@dlstiscd001.dfs.core.windows.net'
TEST_FOLDER = f'{CURATED}/test'

utils = Utils()

ERROR_MESSAGE =  "Get previous date is not defined properly"
expected = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
assert utils.get_previous_date(5) == expected, ERROR_MESSAGE

utils.write_non_distributed_json({'test': 'test'}, f'{TEST_FOLDER}/test.json')

deep_list = [file for file in utils.deep_ls(TEST_FOLDER, 1) if file.name == 'test.json']
assert deep_list[0].path == f'{TEST_FOLDER}/test.json', "Test.json is not found"

deep_list = [file for file in utils.deep_ls(CURATED, 2) if file.name in ['test.json', 'test']]
assert deep_list[0].path == f'{TEST_FOLDER}/test.json', "Test.json is not found"

deep_list = [file for file in utils.deep_ls(CURATED, 1) if file.name in ['test.json', 'test']]
assert deep_list[0].path == f'{TEST_FOLDER}', 'Test founder is not found'
