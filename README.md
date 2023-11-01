# Heart Disease - Data Engineering

## Overview
This code creates a postgres database and database table schema for a [heart disease data set](https://archive.ics.uci.edu/ml/datasets/heart+disease). We extract the data from the `hearts.csv` file, clean, impute, and transform it, and load it into the database tables. We preform exploratory data analysis to look at the spread, statistical measures, and outliers of numerical features.

## Usage 

### AWS Virtual Machine 
We start an EC2 instance with Amazon Linux 2. Then connect to it using 
```
ssh -i /path/key-pair-name.pem ec2-user@instance-public-dns-name
```
where `/path/key-pair-name.pem` is replaced with the path to the key and `instance-public-dns-name` is replaced with the DNS name.

Once on the VM, we install and start docker using the following commands:
```
sudo yum update -y
sudo amazon-linux-extras install docker
sudo service docker start
sudo usermod -a -G docker ec2-user
```
We also install python and pip
```
sudo apt-get install python3.7
curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```
Lastly, we copy files we need from our local computer to the VM using
```
scp -i /path/key-pair-name.pem -r /path/to/local/directory ec2-user@instance-public-dns-name:~./
```
where `/path/key-pair-name.pem` is replaced with the path to the key, `/path/to/local/directory` is the directory containing the files `postgres.sh`, `db_and_tables.sh`, `run.sh`, and `requirements.txt` as well as the directories `data`, `src`, and `scripts`, and `instance-public-dns-name` is replaced with the DNS name.
### Code
To use this code we create a docker container with postgres by using the command
```
bash postgres.sh
```
The scripts folder, which includes scripts to create the database and tables, is mounted, as well as the postgres_data folder. 

Once the container is running we can create the database and tables using 
```
bash db_and_tables.sh
```
Then to test the database and tables we can use the following command to interact in the container 
```
docker exec -it heart-disease-db-postgres /bin/bash
```
Once in the container, we use the postgres password set in the `postgres.sh` script 
```
PGPASSWORD=de300hardpassword
```
and then can go into the database using 
```
psql -U postgres -d heartdisease
```
to confirm the tables were created correctly. 


Then we must install the packages needed, as detailed in `requirements.txt`.


Lastly, we run our ETL and EDA using 
```
bash run.sh
```

## ETL

### Extract 
The `extract.py` script reads the heart_disease.csv to a pandas dataframe, removes the rows at the bottom that are erroneous, and then inserts the data to the sql table 'hearts_data'.

### Transform 
The `transform.py` script gets the data from the 'hearts_data' table, cleans, imputes, and transforms the data, and then writes the data to parquet staging files. 

We clean the data by removing columns with more than 10% of null values. We then impute missing values by using 1 nearest neighbor to get a similar result to the other samples. We remove outliers that are outside of 3 standard deviations from the mean. Lastly, we tranform the data by normalizing all numerical features. 

### Load
The `load.py` script reads a parquet staging file and loads the data into the database. It takes two arguments, the staging file name and the SQL table name. We use this three times: to load the data after cleaning, after removing outliers, and after transformations. The final data we will use for data analysis and machine learning is the transformed data.

## EDA

We compute statistical measures for numerical features in the raw data, imputed data, and data without outliers. We can see the statistical measures do not change by much from the imputed data, which is good because we want to maintain accuracy when filling in missing data. Removing outliers does alter the statistics slightly, as expected from removing samples with outliers. The statistics are written to [statistical_measures.txt](/output/statistical_measures.txt).

We look at the shape of the numerical features by plotting histograms. We can see that all of the numerical features are pretty normally distributed, as shown in [histograms.png](/output/histograms.png).

We decided to investigate age versus cholesteral in a scatter plot because usually as one ages, their health and cholesteral levels tend to get worse. Is that justified / backed up with the data we have currently? It seems based on the [plot](/output/age_vs_chol.png) that cholesteral levels and age have nothing in common, which contradicts our prediction.

We also plot boxplots of the normalized data, and we can again see that the features do have distributions similar to a normal distributed, shown in [boxplots.png](/output/boxplots.png).
