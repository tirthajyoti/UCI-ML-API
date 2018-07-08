from UCI_ML_Functions import *
import pandas as pd

#local_database=''
#local_table=''

def execute_choice():
	"""
	Main execution function which accepts the user choice and calls appropriate function from the "UCI_ML_Functions.py" module.
	"""
	try:
		user_choice=int(input("\nPlease enter your choice now: "))
	except:
		print("Sorry, could not understand your input.")
		return None

	if user_choice==1:
		filename=str(input("Please enter the full name of the local database i.e. a CSV file including the .csv extension (or you can hit ENTER to accept a default name): "))
		if filename=='':
			print()
			build_local_database('UCI database.csv',msg_flag=True)
			local_database='UCI database.csv'
		else:
			if filename[-3:]!='csv':
				filename=filename+".csv"
			print()
			build_local_database(filename,msg_flag=True)
			local_database=filename
	
	elif user_choice==2:
		filename=str(input("Please enter the full name of the local table i.e. a CSV file including the .csv extension (or you can hit ENTER to accept a default name): "))
		if filename=='':
			print()
			build_local_table('UCI table.csv',msg_flag=True)
			local_table='UCI table.csv'
		else:
			if filename[-3:]!='csv':
				filename=filename+".csv"
			print()
			build_local_table(filename,msg_flag=True)
			local_table=filename
	
	elif user_choice==3:
		name=str(input("Please enter the exact name (matching case) of the dataset you want to download: "))
		local_database=str(input("If you have saved a local database please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
		if local_database=='':
			print()
			download_dataset_name(name,local_database=None)
		else:
			print()
			download_dataset_name(name,local_database=local_database)
	
	elif user_choice==4:
		num_downloads = int(input("Please enter the number of datasets to download: "))
		assert type(num_downloads)==int
		local_database=str(input("If you have saved a local database please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
		if local_database=='':
			print()
			download_datasets(num=num_downloads,local_database=None)
		else:
			print()
			download_datasets(num=num_downloads,local_database=local_database)
	
	elif user_choice==5:
		print()
		print_all_datasets_names()
	
	elif user_choice==6:
		print()
		describe_all_dataset()
	
	elif user_choice==7:
		name=str(input("Please enter the name (or a partial word in the name) of the database you want to search: "))
		local_database=str(input("If you have saved a local database please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
		if local_database=='':
			print()
			return_abstract(name,local_database=None)
		else:
			print()
			return_abstract(name,local_database=local_database)
	
	elif user_choice==8:
		size=str(input("Please choose the size of the datasets to download (Small/Medium/Large/Extra Large): "))
		if size not in ['Small','Medium','Large','Extra Large']:
			print("Choice of size not entered correctly. Please make sure to enter exactly one of the choices shown above.")
			pass
		else:
			local_database=str(input("If you have saved a local database please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
			local_table=str(input("If you have saved a local table please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
			if local_database=='' and local_table!='':
				download_datasets_size(size=size,local_database=None,local_table=local_table,msg_flag=False,download_flag=True)
			elif local_database=='' and local_table=='':
				download_datasets_size(size=size,local_database=None,local_table=None,msg_flag=False,download_flag=True)
			elif local_database!='' and local_table=='':
				download_datasets_size(size=size,local_database=local_database,local_table=None,msg_flag=False,download_flag=True)
			else:
				print(f"OK, downloading all datasets of {size} size. This will take some time...")
				download_datasets_size(size=size,local_database=local_database,local_table=local_table,msg_flag=False,download_flag=True)
			
			print("Finished downloading!")
	
	elif user_choice==9:
		task=str(input("Please choose the machine learning task type (Regression OR Classification OR Clustering OR Recommender Systems OR Other/Unknown): "))
		if task not in ['Regression','Classification', 'Clustering', 'Recommender Systems', 'Other/Unknown']:
			print("Choice of machine learning task type not entered correctly. Please make sure to enter exactly one of the choices shown above.")
			pass
		else:
			local_database=str(input("If you have saved a local database please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
			local_table=str(input("If you have saved a local table please enter the full filename now including the .csv extension (this will make the search much faster) OR hit ENTER if you have not saved one before: "))
			if local_database=='' and local_table!='':
				download_datasets_task(task=task,local_database=None,local_table=local_table,msg_flag=False,download_flag=True)
			elif local_database=='' and local_table=='':
				download_datasets_task(task=task,local_database=None,local_table=None,msg_flag=False,download_flag=True)
			elif local_database!='' and local_table=='':
				download_datasets_task(task=task,local_database=local_database,local_table=None,msg_flag=False,download_flag=True)
			else:
				print(f"OK, downloading all datasets of {size} size. This will take some time...")
				download_datasets_task(task=task,local_database=local_database,local_table=local_table,msg_flag=False,download_flag=True)
			
			print("Finished downloading!")
	
	else:
		print(f"{user_choice} is NOT a valid choice! Please choose a number (option) from the menu shown above.")
