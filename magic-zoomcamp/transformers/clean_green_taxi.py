if 'transformer' not in globals():
    from mage_ai.data_preparation.decorators import transformer
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

import io
import pandas as pd
import requests
import re as re

@transformer
def transform(data, *args, **kwargs):
    print("Rows with zero passengers:", data['passenger_count'].isin([0]).sum())

    print("Rows with zero trip distance:", data['trip_distance'].isin([0]).sum())
    # Remove rows where the passenger count is equal to 0 or the trip distance is equal to zero.
    data = data[(data['passenger_count'] > 0) & (data['trip_distance'] > 0)]
    data['lpep_pickup_date'] = data['lpep_pickup_datetime'].dt.date  

    data.columns = (data.columns
                    .str.replace(r'(?<=[a-z])(?=[A-Z])', '_', regex=True)
                    .str.lower()
    )
    return data  
    
@test
def test_output(output, *args) -> None:
    assert output['vendor_id'].isin([1, 2, pd.NA]).all(), 'vendor_id is not 1, 2, or NA (its initial unique values)'
    
    # THIS IS EQUIVALENT TO THE BOTTOM TWO LINES
    assert output['passenger_count'].isin([0]).sum() == 0, 'There are rides with zero passengers'
    assert output['trip_distance'].isin([0]).sum() == 0, 'There are trip distances of zero length'

    ## EQUIVALENT TO
    # assert (output['passenger_count'] > 0).all(), "passenger_count should be greater than 0"
    # assert (output['trip_distance'] > 0).all(), "trip_distance should be greater than 0"


