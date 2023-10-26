import pandas as pd

from utilities import insert_to_table

from params import raw_data_table_name

def extract():
    # extract from csv to dataframe
    data = pd.read_csv('./data/heart_disease.csv')
    # get rid of bottom rows that are erroneous
    dataframe = data[0:899]
    #insert to sql table
    insert_to_table(dataframe, raw_data_table_name)
