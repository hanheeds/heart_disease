from sqlalchemy import create_engine
import pandas as pd
import os.path

from params import conn_string

def insert_to_table(data: pd.DataFrame, table_name:str):
    db = create_engine(conn_string)
    conn = db.connect()
    data.to_sql(table_name, conn, if_exists="replace", index=False)
    conn.close()

def output_folder():
    # make a folder for the output if needed
    if not os.path.exists('./output/'):
        os.makedirs('./output/')

def staging_folder():
    # make a folder for the staging_data if needed
    if not os.path.exists('./staging_data/'):
        os.makedirs('./staging_data/')
