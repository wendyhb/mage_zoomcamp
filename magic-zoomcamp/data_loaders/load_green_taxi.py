import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

def load_data_from_api(month, *args, **kwargs):
    url = f'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2020-{month:02d}.csv.gz'

    taxi_dtypes = {
                    'VendorID': pd.Int64Dtype(),
                    'passenger_count': pd.Int64Dtype(),
                    'trip_distance': float,
                    'RatecodeID':pd.Int64Dtype(),
                    'store_and_fwd_flag':str,
                    'PULocationID':pd.Int64Dtype(),
                    'DOLocationID':pd.Int64Dtype(),
                    'payment_type': pd.Int64Dtype(),
                    'fare_amount': float,
                    'extra':float,
                    'mta_tax':float,
                    'tip_amount':float,
                    'tolls_amount':float,
                    'improvement_surcharge':float,
                    'total_amount':float,
                    'congestion_surcharge':float
                }

    # native date parsing 
    parse_dates = ['lpep_pickup_datetime', 'lpep_dropoff_datetime']

    return pd.read_csv(
        url, sep=',', compression='gzip', dtype=taxi_dtypes, parse_dates=parse_dates
        )

@data_loader
def green_taxi_etl():
    # Initialize an empty DataFrame to concatenate data into
    combined_data = pd.DataFrame()

    # Load data for each month in the final quarter of 2020 (October, November, December)
    for month in range(10, 13):
        data_for_month = load_data_from_api(month)
        combined_data = pd.concat([combined_data, data_for_month], ignore_index=True)

    return combined_data



@test
def test_output(output, *args) -> None:
    assert output is not None, 'The output is undefined'



    