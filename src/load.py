import pandas as pd

from utilities import insert_to_table

"""
read parquet files in the staging folder and load to database
"""

def load(staging_file_name,table_name) -> pd.DataFrame:
    data = pd.DataFrame()
    data = pd.concat([pd.read_parquet('./staging_data/' + staging_file_name),data])

    insert_to_table(data, table_name)

    return data
