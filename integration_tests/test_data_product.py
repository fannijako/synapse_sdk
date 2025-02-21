from generic_utils import DataProduct, Notebook
from test_helper import create_test_delta


test_curated_location, test_trusted_location = create_test_delta(Notebook())

dataproduct = DataProduct()

url = dataproduct.curated_tables.get('test_delta_listing_curated').get('url')
assert url == test_curated_location, "Test delta not found"

url = dataproduct.trusted_tables.get('test_delta_listing_trusted').get('url')
assert url == test_trusted_location, "Test delta not found"

assert 'test_delta_listing_curated' in dataproduct, "Contains not defined properly"
assert 'test_delta_listing_trusted' in dataproduct, "Contains not defined properly"
assert repr(dataproduct) == 'DataProduct()', 'Repr not defined properly'
assert str(dataproduct) == 'tisc data product version 001', 'str not defined properly'

other_data_product = DataProduct()
other_data_product.data_product_name = 'coca'

assert dataproduct.data_product_name == 'tisc', "Data product name changed unintentionally"
assert other_data_product != dataproduct, 'Other data product does not differ from data product'
