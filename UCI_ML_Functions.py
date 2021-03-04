# Functions to read, analyze, and download from UCI ML portal

# ==========================================
# Function to read UCI ML datasets table
# ==========================================
def read_dataset_table(
    url="https://archive.ics.uci.edu/ml/datasets.php", msg_flag=True
):
    """
    Reads the table of datasets from the url: "https://archive.ics.uci.edu/ml/datasets.html" and process it further to clean and categorize
    """
    import pandas as pd

    try:
        if msg_flag:
            print("Reading the dataset table from UCI ML repo...")
        datasets = pd.read_html(url)
        if msg_flag:
            print("Finished reading the table!")
    except:
        print("Could not read the table from UCI ML portal, Sorry!")

    df = datasets[5]  # Fifth entry of this table is the main datasets information
    # Rows and columns of the dataframe
    nrows = df.shape[0]
    ncols = df.shape[1]

    # Read the pertinent rows (skipping every alternate one) and columns
    df = df.iloc[1:nrows:2][[2, 3, 4, 5, 6, 7, 8]]

    # Assign column names
    df.columns = [
        "Name",
        "Data Types",
        "Default Task",
        "Attribute Types",
        "Number of Instances",
        "Number of Attributes",
        "Year",
    ]

    # Set index from 1
    df.index = [i for i in range(1, int(nrows / 2) + 1)]

    return df


# ==============================================================================================
# Function to remove entries with unknown number of samples and cleanly define task categories
# ==============================================================================================
def clean_dataset_table(df, msg_flag=True):
    """
    Accepts the raw dataset table (a DataFrame object) and returns a cleaned up version removing entries with unknown number of samples and attributes
    Also creates a 'Task' category column indicating the main machine learning task associated with the dataset
    """
    import time
    import pandas as pd

    if msg_flag:
        print("Cleaning up the dataset table", end="")
        for i in range(11):
            time.sleep(0.2)
            print(".", end="")
        print(" ", end="")
        print()
        print("Rationalizing the task categories", end="")
        for i in range(11):
            time.sleep(0.2)
            print(".", end="")
        print(" ", end="")

    pd.set_option("mode.chained_assignment", None)

    df_copy = df.copy()
    df_clean = df_copy.dropna(subset=["Number of Instances"])
    df_clean["Number of Instances"] = df_clean["Number of Instances"].apply(int)

    def size_instances(n):
        if n <= 100:
            return "Small"
        elif n <= 1000:
            return "Medium"
        elif n <= 10000:
            return "Large"
        else:
            return "Extra Large"

    df_clean["Sample size"] = df_clean["Number of Instances"].apply(size_instances)

    def categorize_task(task):
        if len(task) > 1:
            tasks = task.split(", ")
        else:
            tasks = list(task)

        if len(tasks) == 1 and tasks[0] == "Classification":
            return "Classification"
        elif "Clustering" in tasks:
            return "Clustering"
        elif "Regression" in tasks:
            return "Regression"
        elif "Recommender-Systems" in tasks:
            return "Recommender Systems"
        elif "Causal-Discovery" in tasks:
            return "Causal Discovery"
        else:
            return "Other/Unknown"

    df_clean["Default Task"] = df_clean["Default Task"].apply(str)
    df_clean["Default Task"] = df_clean["Default Task"].apply(categorize_task)

    if msg_flag:
        print("\nFinished processing the table!")

    return df_clean


# ======================================================================================================
# Function to build a local table (CSV file) with name, attributes, machine learning tasks, size, etc
# ======================================================================================================
def build_local_table(filename=None, msg_flag=True):
    """
    Reads through the UCI ML portal and builds a local table with information such as: \
    name, size, ML task, data type
    filename: Optional filename that can be chosen by the user
    """
    df_table = read_dataset_table(msg_flag=msg_flag)
    df_clean = clean_dataset_table(df_table, msg_flag=msg_flag)
    try:
        if filename != None:
            df_clean.to_csv(filename)
        else:
            df_clean.to_csv("UCI table.csv")
    except:
        print(
            "Sorry, could not create the CSV table. Please make sure to close an already opened file, \
        or to have sufficient permission to write files in the current directory"
        )


# ==================================================================
# Function to read the main page text and create list of datasets
# ==================================================================
def build_dataset_list(url="https://archive.ics.uci.edu/ml/datasets", msg_flag=True):
    """
    Scrapes through the UCI ML datasets page and builds a list of all datasets.
    """

    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import time

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    # Read the HTML from the URL and pass on to BeautifulSoup
    url = url
    if msg_flag:
        print("Opening the file connection...")
    try:
        uh = urllib.request.urlopen(url, context=ctx)
        # print("HTTP status",uh.getcode())
        html = uh.read()
        # print(f"Reading done. Total {len(html)} characters read.")
    except:
        print("Could not open the UCI ML portal successfully. Sorry!")
        return -1

    soup = BeautifulSoup(html, "html5lib")

    dataset_list = []
    lst = []

    for link in soup.find_all("a"):
        lst.append(link.attrs)

    if msg_flag:
        print()
        print("Adding datasets to the list", end="")

        for i in range(11):
            time.sleep(0.3)
            print(".", end="")
        print(" ", end="")

    for l in lst:
        a = l["href"]
        if a.find("/") != -1:
            x = a.split("/")
            if len(x) == 2:
                dataset_list.append(x[1])

    dataset_list = list(set(dataset_list))
    dataset_list = sorted(dataset_list)

    if msg_flag:
        print("\nFinished adding datasets to the list!")

    return dataset_list


# ======================================================================================
# Function to create dictionary of datasets' name, description, and identifier string
# ======================================================================================
def build_dataset_dictionary(
    url="https://archive.ics.uci.edu/ml/datasets.php?format=&task=&att=&area=&numAtt=&numIns=&type=&sort=nameUp&view=list",
    msg_flag=True,
):
    """
    Scrapes through the UCI ML datasets page and builds a dictionary of all datasets with names and description.
    Also stores the unique identifier corresponding to the dataset.
    This identifier string is needed by the downloader function to download the data file. Generic name won't work.
    """
    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import time
    import re

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    url = url
    if msg_flag:
        print("Opening the file connection...")
    try:
        uh = urllib.request.urlopen(url, context=ctx)
        html = uh.read()
    except:
        print("Could not open the UCI ML portal successfully. Sorry!")
        return -1

    soup = BeautifulSoup(html, "html5lib")

    lst = []
    for tag in soup.find_all("p"):
        lst.append(tag.contents)

    i = 0
    description_dict = {}

    for l in lst:
        if len(l) > 2:
            if str(l[1]).find("datasets/") != -1:
                string = str(l[1])
                s = re.search('">.*</a>', string)
                x, y = s.span()
                name = string[x + 2 : y - 4]
                desc = l[2][2:]
                tmp_list = []
                description_dict[name] = tmp_list
                description_dict[name].append(desc)
                s = re.search('".*"', string)
                x, y = s.span()
                identifier = string[x + 10 : y - 1]
                description_dict[name].append(identifier)
                i += 1
        if msg_flag:
            if i % 10 == 0 and i != 0:
                print(f"Record {i} processed!")

    return description_dict


# ===============================================================
# Function to create a DataFrame with all information together
# ===============================================================
def build_full_dataframe(msg_flag=False):
    """
    Builds a DataFrame with all information together including the url link for downloading the data.
    """
    import pandas as pd
    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import time

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    i = 0
    d = build_dataset_dictionary(msg_flag=False)
    new_d = {}
    dataset_list = build_dataset_list(msg_flag=False)

    for k, v in d.items():
        a = extract_url_dataset(v[1], msg_flag=msg_flag)
        if a != None:
            desc = v[0]
            identifier = v[1]
            v[0] = k
            v[1] = desc
            v.append(identifier)
            v.append(a)
            new_d[k] = v
            i += 1
            if msg_flag:
                print(f"Dataset processed:{k}")
        else:
            desc = v[0]
            identifier = v[1]
            v[0] = k
            v[1] = desc
            v.append(identifier)
            v.append("URL not available")
            new_d[k] = v
            if msg_flag:
                print(f"Dataset processed:{k}")
    if msg_flag:
        print("\nTotal datasets analyzed: ", i)

    df_dataset = pd.DataFrame(data=new_d)
    df_dataset = df_dataset.T
    df_dataset.columns = ["Name", "Abstract", "Identifier string", "Datapage URL"]
    df_dataset.index.set_names(["Dataset"], inplace=True)

    return df_dataset


# ================================================================================================
# Function to build a local database (CSV file) with name and URL (of raw data page) information
# ================================================================================================
def build_local_database(filename=None, msg_flag=True):
    """
    Reads through the UCI ML portal and builds a local table with information such as: \
    name, size, ML task, data type
    filename: Optional filename that can be chosen by the user
    """
    df_local = build_full_dataframe(msg_flag=msg_flag)
    try:
        if filename != None:
            df_local.to_csv(filename)
        else:
            df_local.to_csv("UCI database.csv")
    except:
        print(
            "Sorry, could not create the CSV table. Please make sure to close an already opened file, \
        or to have sufficient permission to write files in the current directory"
        )


# ===============================================================================
# Function to extract abstract/description of a particular dataset by searching
# ===============================================================================
def return_abstract(name, local_database=None, msg_flag=False):
    """
    Returns one-liner description (and webpage link for further information) of a particular dataset by searching the given name.
    local_database: Name of the database (CSV file) stored locally i.e. in the same directory, which contains information about all the datasets on UCI ML repo. 
    msg_flag: Controls verbosity
    """

    import pandas as pd

    if local_database != None:
        local_df_flag = True
        df = pd.read_csv(local_database, index_col="Dataset")
    else:
        local_df_flag = False
        if msg_flag:
            print(
                "Local database not supplied.\nBuilding the master database by crawling the website..."
            )
        df = build_full_dataframe(msg_flag=False)
        if msg_flag:
            print("Done!")

    # Number of rows
    nrows = df.shape[0]
    found = 0
    abstracts = []
    for r in range(nrows):
        if name in df.iloc[r]["Name"]:
            found += 1
            abstracts.append(
                df.iloc[r]["Name"]
                + ": "
                + df.iloc[r]["Abstract"]
                + ". For more info, visit this link: "
                + "https://archive.ics.uci.edu/ml/datasets/"
                + df.iloc[r]["Identifier string"]
            )
    if found == 0:
        print("Could not find your search term.")
        return None
    else:
        print(
            f"Total {found} instances found including partial match of the search term. Here they are...\n"
        )
        for a in abstracts:
            print(a)
            print("=" * 100)


# =============================================
# Function to print all dataset descriptions
# =============================================
def describe_all_dataset(msg_flag=False):
    """
    Calls the build_dictionary function and prints description of all datasets from that.
    """

    dict1 = build_dataset_dictionary(msg_flag=msg_flag)

    for k, v in dict1.items():
        print(f"{k}: {v[0]}")
        print("=" * 100)


# =======================================
# Function to print all dataset names
# =======================================
def print_all_datasets_names(msg_flag=False):
    """
    Calls the build_dictionary function and prints names of all datasets from that.
    """

    dict1 = build_dataset_dictionary(msg_flag=msg_flag)

    for key in dict1.keys():
        print(key)
        print("-" * 100)


# ==========================================
# Function for extracting dataset page url
# ==========================================
def extract_url_dataset(dataset, msg_flag=False):
    """
    Given a dataset identifier this function extracts the URL for the page where the actual raw data resides.
    """
    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import time

    # Ignore SSL certificate errors
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE

    dataset_dict = {}
    baseurl = "https://archive.ics.uci.edu/ml/datasets/"
    url = baseurl + dataset

    try:
        uh = urllib.request.urlopen(url, context=ctx)
        html = uh.read().decode()
        soup = BeautifulSoup(html, "html5lib")
        if soup.text.find("does not appear to exist") != -1:
            if msg_flag:
                print(f"{dataset} not found")
            return None
        else:
            for link in soup.find_all("a"):
                if link.attrs["href"].find("machine-learning-databases") != -1:
                    a = link.attrs["href"]
                    a = a[2:]
                    dataurl = "https://archive.ics.uci.edu/ml/" + str(a)
                    # print(dataurl)
                    return str(dataurl)
                    # dataurls.append(dataurl)

            # After finishing the for-loop with a-tags, the first dataurl is added to the dictionary
            # dataset_dict['dataurl']=dataurls[0]
    except:
        # print("Could not retrieve")
        return None


# ================================
# File download helper function
# ================================
def download_file(url, directory):
    """
    Downloads a file from a given url into the given directory.
    """
    import requests
    import os

    local_filename = directory + "/" + url.split("/")[-1]
    # NOTE the stream=True parameter
    r = requests.get(url, stream=True)
    try:
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=1024):
                if chunk:  # filter out keep-alive new chunks
                    f.write(chunk)
    except:
        print("Sorry could not write this particular file!")
        # f.flush()


# =====================================================
# Function for downloading the data set from a page
# =====================================================
def download_dataset_url(url, directory, msg_flag=False, download_flag=True):
    """
    Download all the files from the links in the given url.
    msg_flag: Controls verbosity.
    download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose).
    """

    import urllib.request, urllib.parse, urllib.error
    from bs4 import BeautifulSoup
    import ssl
    import os

    if url == "URL not available":
        return None

    cwd = os.getcwd()
    directory = directory.replace(":", "-")
    local_directory = cwd + "\\" + str(directory)
    if not os.path.exists(local_directory):
        try:
            os.makedirs(local_directory)
        except:
            print(f"Cannot create directory: {directory}")

    if download_flag:
        # Ignore SSL certificate errors
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        uh = urllib.request.urlopen(url, context=ctx)
        html = uh.read().decode()
        soup = BeautifulSoup(html, "html5lib")

        links = []
        for link in soup.find_all("a"):
            links.append(link.attrs["href"])

        links_to_download = []

        if "Index" in links:
            idx = links.index("Index")
        else:
            idx = len(links) - 2
        for i in range(idx + 1, len(links)):
            links_to_download.append(url + str(links[i]))

        for file_url in links_to_download:
            download_file(file_url, local_directory)

        if msg_flag:
            print(f"Downloaded dataset from {url}")


# =================================================================================================
# User API Function for downloading a given number of datasets and storing in a local directory
# =================================================================================================
def download_datasets(num=10, local_database=None, msg_flag=True, download_flag=True):
    """
    Downloads datasets and puts them in a local directory named after the dataset.
    By default downloads first 10 datasets only. User can choose the number of dataets to be downloaded.
    msg_flag: Controls verbosity.
	download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose).
    """

    import pandas as pd

    if local_database != None:
        local_df_flag = True
        df = pd.read_csv(local_database, index_col="Dataset")
    else:
        local_df_flag = False
        if msg_flag:
            print(
                "Local database not supplied.\nBuilding the master database by crawling the website..."
            )
        df = build_full_dataframe(msg_flag=False)
        if msg_flag:
            print("Done!")

    if num < 1:
        print("Invalid entry for the number of datasets.")
    else:
        for i in range(num):
            if msg_flag:
                print(f"Downloading dataset(s) for: {df['Name'][i]}")
            download_dataset_url(
                df["Datapage URL"][i],
                df["Name"][i],
                msg_flag=False,
                download_flag=download_flag,
            )
        print("\nFinished downloading.")


# ============================================================================
# User API function to download dataset by searching a for particular name
# ============================================================================
def download_dataset_name(name, local_database=None, msg_flag=True, download_flag=True):
    """
    Downloads a particular dataset by searching the given name.
    local_database: Name of the database (CSV file) stored locally i.e. in the same directory, which contains information about all the datasets on UCI ML repo. 
    msg_flag: Controls verbosity
    download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose)
    """
    import pandas as pd

    if local_database != None:
        local_df_flag = True
        df = pd.read_csv(local_database, index_col="Dataset")
    else:
        local_df_flag = False
        if msg_flag:
            print(
                "Local database not supplied.\nBuilding the master database by crawling the website..."
            )
        df = build_full_dataframe(msg_flag=False)
        if msg_flag:
            print("Done!")

    urls_to_download = {}

    for i in df.index.values:
        if name in i:
            urls_to_download[df.loc[i]["Name"]] = df.loc[i]["Datapage URL"]

    if len(urls_to_download) == 0:
        print(f'Serach term "{name}" not found in the database. Nothing downloaded!')
    else:
        if len(urls_to_download) > 1:
            print(
                f"{len(urls_to_download)} instances of search term found including partial match. Downloading datasets for all...\n"
            )

        for u in urls_to_download:
            if msg_flag:
                print(f"Downloading dataset(s) for: {u}")
            download_dataset_url(
                urls_to_download[u],
                directory=u,
                msg_flag=False,
                download_flag=download_flag,
            )

        print("\nFinished downloading.")


# =========================================================
# Function to download all datasets in a given dataframe
# =========================================================
def download_all_from_dataframe(df, msg_flag=False, download_flag=True):
    """
    Downloads all datasets which appear in the given dataframe.
    Assumes that the datapage URL information is in the dataframe.
    msg_flag: Controls verbosity
    download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose)
    """

    nrows = df.shape[0]
    if download_flag == False:
        print("Not downloading anything, just creating empty directories.\n")
    for r in range(nrows):
        if msg_flag:
            print(f"Downloading the dataset: {df.iloc[r]['Name']}")
        download_dataset_url(
            df.iloc[r]["Datapage URL"], df.iloc[r]["Name"], download_flag=download_flag
        )


# =======================================================
# User API Function to download datasets based on size
# =======================================================
def download_datasets_size(
    size="Small",
    local_database=None,
    local_table=None,
    msg_flag=False,
    download_flag=True,
):
    """
    Downloads all datasets which satisfy the 'size' criteria.
    size: Size of the dataset which user wants to download. Could be any of the following: 'Small', 'Medium', 'Large','Extra Large'.
    local_database: Name of the database (CSV file) stored locally i.e. in the same directory, which contains name and URL information about all the datasets on UCI ML repo.
    local_table: Name of the database (CSV file) stored locally i.e. in the same directory, which contains features information about all the datasets on UCI ML repo i.e. number of samples, type of machine learning task to be performed with the dataset. 
    msg_flag: Controls verbosity
    download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose)
    """
    import pandas as pd

    assert type(size) == str
    assert str(size) in ["Small", "Medium", "Large", "Extra Large"]

    if local_database != None:
        local_df_flag = True
        df_local = pd.read_csv(local_database, index_col="Dataset")
        df = df_local
    else:
        local_df_flag = False
        print(
            "Local database not supplied.\nBuilding the master database by crawling the website..."
        )
        df = build_full_dataframe(msg_flag=False)
        print("Master database build done!")

    if local_table != None:
        local_table_flag = True
        table_local = pd.read_csv(local_table)
        df_clean = clean_dataset_table(table_local, msg_flag=msg_flag)
    else:
        local_table_flag = False
        print(
            "Local table not supplied.\nBuilding the master table by reading from the website..."
        )
        df_table = read_dataset_table(msg_flag=msg_flag)
        df_clean = clean_dataset_table(df_table, msg_flag=msg_flag)

    df_merged = df_clean.merge(df, on="Name")
    df_filter = df_merged[df_merged["Sample size"] == str(size)]

    download_all_from_dataframe(
        df_filter, msg_flag=msg_flag, download_flag=download_flag
    )


# ===========================================================================
# User API Function to download datasets based on the machine learning task
# ===========================================================================
def download_datasets_task(
    task="Classification",
    local_database=None,
    local_table=None,
    msg_flag=False,
    download_flag=True,
):
    """
    Downloads all datasets which satisfy the size criteria.
    task: Machine learning task for which user wants to download the datasets. Could be any of the following: 
	    'Classification', 
		'Recommender Systems', 
		'Regression', 
		'Other/Unknown', 
		'Clustering', 
		'Causal Discovery'.
	local_database: Name of the database (CSV file) stored locally i.e. in the same directory, which contains name and URL information about all the datasets on UCI ML repo.
	local_table: Name of the database (CSV file) stored locally i.e. in the same directory, which contains features information about all the datasets on UCI ML repo i.e. number of samples, type of machine learning task to be performed with the dataset. 
	msg_flag: Controls verbosity
    download_flag: Default is True. If set to False, only creates the directories but does not initiate download (for testing purpose).
    """
    import pandas as pd

    if local_database != None:
        local_df_flag = True
        df = pd.read_csv(local_database, index_col="Dataset")
    else:
        local_df_flag = False
        print(
            "Local database not supplied.\nBuilding the master database by crawling the website..."
        )
        df = build_full_dataframe(msg_flag=False)
        print("Master database build done!")

    if local_table != None:
        local_table_flag = True
        df_clean = pd.read_csv(local_table)
    else:
        local_table_flag = False
        print(
            "Local table not supplied.\nBuilding the master table by reading from the website..."
        )
        df_table = read_dataset_table(msg_flag=msg_flag)
        df_clean = clean_dataset_table(df_table, msg_flag=msg_flag)

    df_merged = df_clean.merge(df, on="Name")
    df_filter = df_merged[df_merged["Default Task"] == str(task)]

    download_all_from_dataframe(
        df_filter, msg_flag=msg_flag, download_flag=download_flag
    )
