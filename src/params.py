conn_string = 'postgresql://postgres:de300hardpassword@localhost:5432/heartdisease'
raw_data_table_name = "raw_hearts_data"
clean_data_table_name = "clean_hearts_data"
outliers_removed_data_table_name = "outliers_removed_hearts_data"
transformed_data_table_name = "transformed_hearts_data"

staging_data_dir = "staging_data"
clean_staging_file = "hearts_clean.parquet"
outliers_staging_file = "hearts_outliers_removed.parquet"
transformed_staging_file = "hearts_transformed.parquet"

numerical = ['age', 'chol','thaldur','oldpeak', 'thalach', 'thalrest', 'tpeakbps', 'tpeakbpd','trestbps', 'trestbpd']