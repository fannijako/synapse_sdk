import pytest  # type: ignore

from src.generic_utils import DataProduct, Notebook
from tests.test_helper import create_test_delta


@pytest.fixture(scope='module')
def test_delta_locations():
    return create_test_delta(Notebook())


@pytest.fixture
def dataproduct():
    return DataProduct()


class TestDataProduct:
    def test_curated_table_url(self, dataproduct, test_delta_locations):
        test_curated_location, _ = test_delta_locations
        url = dataproduct.curated_tables.get('test_delta_listing_curated').get('url')
        assert url == test_curated_location

    def test_trusted_table_url(self, dataproduct, test_delta_locations):
        _, test_trusted_location = test_delta_locations
        url = dataproduct.trusted_tables.get('test_delta_listing_trusted').get('url')
        assert url == test_trusted_location

    def test_contains_curated_table(self, dataproduct, test_delta_locations):  # pylint: disable=unused-argument
        assert 'test_delta_listing_curated' in dataproduct

    def test_contains_trusted_table(self, dataproduct, test_delta_locations):  # pylint: disable=unused-argument
        assert 'test_delta_listing_trusted' in dataproduct

    def test_repr(self, dataproduct):
        assert repr(dataproduct) == 'DataProduct()'

    def test_str(self, dataproduct):
        assert str(dataproduct) == 'tisc data product version 001'

    def test_data_product_name_default(self, dataproduct):
        assert dataproduct.data_product_name == 'tisc'

    def test_mutation_does_not_affect_other_instance(self, dataproduct):
        other_data_product = DataProduct()
        other_data_product.data_product_name = 'coca'
        assert dataproduct.data_product_name == 'tisc'
        assert other_data_product != dataproduct
