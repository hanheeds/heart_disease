import pandas as pd
from sqlalchemy import create_engine
import os.path
from matplotlib import pyplot as plt

from params import conn_string, numerical
from params import raw_data_table_name, clean_data_table_name, outliers_removed_data_table_name, transformed_data_table_name

titles=['Age','Cholesterol',
        'Duration of Exercise Test', 'ST Depression Induced by Exercise Relative to Rest',
        'Maximum Heart Rate Achieved','Resting Heart Rate',
        'Peak Exercise Systolic Blood Pressue', 'Peak Exercise Diastolic Blood Pressue',
        'Resting Diastolic Blood Pressure','Resting Diastolic Blood Pressue']

def eda_raw_data():
    # fetch the raw data
    db = create_engine(conn_string)

    df = pd.read_sql_query(f'SELECT * FROM {raw_data_table_name}',con=db)

    df = df.convert_dtypes()
    df['age'] = df['age'].astype('Int64')
    
    with open('./output/statistical_measures.txt', 'w') as f:
        f.write('Statistical measures before imputing missing values\n')
        f.write('                Mean       Std    Median       IQR  Kurtosis  Skewness\n')
        for col in numerical:
            stats=df[col].describe()
            median = df[col].median()
            kurtosis = df[col].kurtosis()
            skew = df[col].skew()
            f.write('{:10}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}\n'.format(col,stats[1],stats[2],median,stats[6]-stats[4],kurtosis,skew))

def eda_clean_data():
    # fetch data
    db = create_engine(conn_string)

    data = pd.read_sql_query(f'SELECT * FROM {clean_data_table_name}',con=db)

    # HISTOGRAMS 
    fig = plt.figure(figsize=(8, 20))

    ranges = [(30,75),(0,600),(0,25),(-3,6),(50,200),(25,150),(75,250),(0,150),(75,200),(40,120)]
    x_labels = ['years','mg/dL',
                'minutes','mm',
                'beats per minute', 'beats per minute',
                'mm Hg', 'mm Hg',
                'mm Hg', 'mm Hg']
    for ii,col in enumerate(numerical):
        ax = plt.subplot(5,2,ii+1)
        # plot
        ax.hist(data[col],range=ranges[ii],bins=15,rwidth=0.8,density=True)
        # add title and labels
        ax.set_title(titles[ii])
        ax.set_ylabel('Density')
        ax.set_xlabel(x_labels[ii])
    fig.tight_layout()
    fig.savefig('./output/histograms.png')
    plt.close()

    # statistical measures 
    with open('./output/statistical_measures.txt', 'a') as f:
        f.write('\nStatistical measures after imputing missing values\n')
        f.write('                Mean       Std    Median       IQR  Kurtosis  Skewness\n')
        for col in numerical:
            stats=data[col].describe()
            median = data[col].median()
            kurtosis = data[col].kurtosis()
            skew = data[col].skew()
            f.write('{:10}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}\n'.format(col,stats[1],stats[2],median,stats[6]-stats[4],kurtosis,skew))

def eda_outliers_removed_data():
    # fetch the data without outliers
    db = create_engine(conn_string)
    outliers_removed = pd.read_sql_query(f'SELECT * FROM {outliers_removed_data_table_name}',con=db)

    with open('./output/statistical_measures.txt', 'a') as f:
        f.write('\nStatistical measures after removing outliers\n')
        f.write('                Mean       Std    Median       IQR  Kurtosis  Skewness\n')
        for col in numerical:
            stats= outliers_removed[col].describe()
            median = outliers_removed[col].median()
            kurtosis = outliers_removed[col].kurtosis()
            skew = outliers_removed[col].skew()
            f.write('{:10}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}{:10.2f}\n'.format(col,stats[1],stats[2],median,stats[6]-stats[4],kurtosis,skew))

    x = outliers_removed['age']
    y = outliers_removed['chol']

    # Create a scatter plot 
    plt.scatter(x,y)

    # Set the x and y axis labels
    plt.xlabel('Age (years)')
    plt.ylabel('Cholesteral Levels (mg/dL)')

    # Save the plot
    plt.savefig('./output/age_vs_chol.png')

def eda_transformed_data():
    # fetch the transformed data
    db = create_engine(conn_string)
    transformed = pd.read_sql_query(f'SELECT * FROM {transformed_data_table_name}',con=db)

    ### BOXPLOTS
    fig = plt.figure(figsize=(10, 10)) 
    ax = plt.subplot(1,1,1)
    ax.boxplot(transformed[numerical],labels=titles)
    plt.xticks(rotation=90)
    fig.tight_layout()
    fig.savefig('./output/boxplots.png')
    plt.close()

