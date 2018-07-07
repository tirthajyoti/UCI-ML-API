from UCI_ML_Functions import *
import pandas as pd


df_table = read_dataset_table()
df_clean=clean_dataset_table(df_table)
df_clean.to_csv('UCI table.csv')
print("="*100)
print()

describe_all_dataset()
print("="*100)
print()

print_all_datasets_names()
print("="*100)
print()

df=build_full_dataframe(msg_flag=True)
df.to_csv("UCI database.csv")
print("="*100)
print()


download_dataset_name('Titanic',local_database='UCI database.csv',msg_flag=True)
download_dataset_name('Cancer',local_database='UCI database.csv',msg_flag=True)

download_datasets(num=5,local_database='UCI database.csv')

download_datasets_size('Extra Large',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)
print("="*100)
print()
download_datasets_size('Small',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=True)


download_datasets_task(task='Recommender Systems',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)
print("="*100)
print()
download_datasets_task(task='Other/Unknown',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)
print("="*100)
print()
download_datasets_task(task='Clustering',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)
print("="*100)
print()
download_datasets_task(task='Regression',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)
print("="*100)
print()
download_datasets_task(task='Classification',local_database='UCI database.csv',local_table='UCI table.csv',
                       msg_flag=True,download_flag=False)