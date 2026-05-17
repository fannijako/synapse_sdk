from datetime import datetime, timedelta

import pytest  # type: ignore

from src.generic_utils import Utils


CURATED = 'abfss://curated@dlstiscd001.dfs.core.windows.net'
TEST_FOLDER = f'{CURATED}/test'


@pytest.fixture
def utils():
    return Utils()


class TestUtils:
    def test_get_previous_date(self, utils):
        expected = (datetime.now() - timedelta(days=5)).strftime('%Y-%m-%d')
        assert utils.get_previous_date(5) == expected

    def test_write_non_distributed_json(self, utils):
        utils.write_non_distributed_json({'test': 'test'}, f'{TEST_FOLDER}/test.json')

    def test_deep_ls_finds_test_json_at_depth_1(self, utils):
        deep_list = [file for file in utils.deep_ls(TEST_FOLDER, 1) if file.name == 'test.json']
        assert deep_list[0].path == f'{TEST_FOLDER}/test.json'

    def test_deep_ls_finds_test_json_at_depth_2(self, utils):
        deep_list = [file
                     for file
                     in utils.deep_ls(CURATED, 2)
                     if file.name in ['test.json', 'test']]
        assert deep_list[0].path == f'{TEST_FOLDER}/test.json'

    def test_deep_ls_finds_test_folder_at_depth_1(self, utils):
        deep_list = [file
                     for file
                     in utils.deep_ls(CURATED, 1)
                     if file.name in ['test.json', 'test']]
        assert deep_list[0].path == f'{TEST_FOLDER}'
