from extract import extract
from transform import clean, remove_outliers, transform
from load import load
from eda import eda_raw_data, eda_clean_data, eda_outliers_removed_data, eda_transformed_data
from params import clean_data_table_name, outliers_removed_data_table_name, transformed_data_table_name
from params import clean_staging_file, outliers_staging_file, transformed_staging_file
from utilities import output_folder, staging_folder

def main():
    extract()
    output_folder()
    staging_folder()
    eda_raw_data()
    clean()
    load(clean_staging_file,clean_data_table_name)
    eda_clean_data()
    remove_outliers()
    load(outliers_staging_file,outliers_removed_data_table_name)
    eda_outliers_removed_data()
    transform()
    load(transformed_staging_file,transformed_data_table_name)
    eda_transformed_data()

main()