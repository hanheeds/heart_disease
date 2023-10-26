import pandas as pd
from sqlalchemy import create_engine
import os.path
from sklearn.impute import KNNImputer
import numpy as np

from params import conn_string, numerical
from params import raw_data_table_name, clean_data_table_name, outliers_removed_data_table_name
from params import staging_data_dir, clean_staging_file, outliers_staging_file, transformed_staging_file

def clean():
    '''
    Gets the raw data, removes columns missing more than 10% of the data, and imputes missing values using 1 nearest neighbor.
    '''
    # fetch the raw data
    db = create_engine(conn_string)

    df = pd.read_sql_query(f'SELECT * FROM {raw_data_table_name}',con=db)

    print(f"Shape of raw data: {df.shape}")

    # Get the counts of null for each column
    null_count = df.isnull().sum()

    # If null counts are higher than 10%, we will drop the column. 
    cols_to_drop = null_count[null_count > int(df.shape[0]*0.1)].index.tolist()

    # Drop the columns 
    df = df.drop(columns=cols_to_drop)

    # fix dtypes
    df = df.convert_dtypes()
    df['age'] = df['age'].astype('Int64')

    columns = df.columns

    # impute mising values using kNN
    imputer = KNNImputer(n_neighbors=1)
    data = imputer.fit_transform(df)
    # back into df
    data = pd.DataFrame(data,columns=columns)
    # fix dtypes
    data = data.convert_dtypes()

    print(f"Shape of clean data: {data.shape}")

    # write to parquet
    data.to_parquet(os.path.join(staging_data_dir, clean_staging_file))

def remove_outliers():
    '''
    Gets the cleaned data, finds outliers, and removes them.
    '''
    # fetch the clean data
    db = create_engine(conn_string)

    data = pd.read_sql_query(f'SELECT * FROM {clean_data_table_name}',con=db)

    outliers_removed = data[data[numerical].apply(lambda x: np.abs(x - x.mean()) / x.std() < 3).all(axis=1)]

    print(f"Shape of data with outliers removed: {outliers_removed.shape}")

    # write to parquet
    outliers_removed.to_parquet(os.path.join(staging_data_dir, outliers_staging_file))

def transform():
    '''
    Gets the data without outliers and preforms normalization to transform the data.
    '''
    # fetch the data without outliers
    db = create_engine(conn_string)

    outliers_removed = pd.read_sql_query(f'SELECT * FROM {outliers_removed_data_table_name}',con=db)

    transformed = outliers_removed.copy()
    # normalize all numerical data
    for col in numerical:
        tmp = outliers_removed[col]
        transformed[col]=(tmp - tmp.mean())/tmp.std()

    # write to parquet
    transformed.to_parquet(os.path.join(staging_data_dir, transformed_staging_file))