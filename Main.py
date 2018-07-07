from UCI_ML_Functions import *
from Choice import *
import pandas as pd

#=====================================================
# Main UX with simple information about the software
#=====================================================
           
print()
print(" "*15+"UCI Machine Learning Repo API by Dr. Tirthajyoti Sarkar"+" "*15)
print(" "*25+"July 2018, Sunnyvale, CA 94086"+" "*25)
print(" "*10+"Uses the following packages: pandas, BeautifulSoup, requests"+" "*10)
print()

print("Please choose from the following options:\n\
(It is HIGHLY RECOMMENDED to choose first two options to build local databases first.\n\
This significantly enhances later search and download speed)\n\
============================================================================\n\
1. Build a local database of name, description, and URL of datasets\n\
2. Build a local database of name, size, machine learning task of datasets\n\
3. Search and download a particular dataset\n\
4. Download first few datasets\n\
5. Print names of all datasets\n\
6. Print descriptions of all datasets\n\
7. Show one-liner description and webpage link (for more info) of a dataset\n\
8. Download datasets based on their size\n\
9. Download datasets based on the machine learning task associated with them\n")

execute_choice()
