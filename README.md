
![Header](https://raw.githubusercontent.com/tirthajyoti/tirthajyoti.github.io/master/Images/robo_with_ipad.jpg)
# A simple API for working with University of Irvine (UCI) Machine Learning repository
[UCI machine learning dataset repository](https://archive.ics.uci.edu/ml/index.php) is something of a legend in the field of machine learning pedagogy. It is a *'go-to-shop'* for beginners and advanced learners alike. This codebase is an attempt to present **a simple and intuitive API for UCI ML portal**, where users can easily look up a dataset description, search for a particular dataset they are interested, and even download datasets categorized by size or machine learning task.

### About Page of the repository
*The [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php) is a collection of databases, domain theories, and data generators that are used by the machine learning community for the empirical analysis of machine learning algorithms. The archive was created as an ftp archive in 1987 by David Aha and fellow graduate students at UC Irvine. Since that time, it has been widely used by students, educators, and researchers all over the world as a primary source of machine learning data sets. As an indication of the impact of the archive, it has been cited over 1000 times, making it one of the top 100 most cited "papers" in all of computer science. The current version of the web site was designed in 2007 by Arthur Asuncion and David Newman, and this project is in collaboration with Rexa.info at the University of Massachusetts Amherst. Funding support from the National Science Foundation is gratefully acknowledged.*

![UCI ML Logo](https://archive.ics.uci.edu/ml/assets/logo.gif)

### Navigating the portal can be challenging and time consuming
UCI ML portal is a wonderful gift to ML practioners. That said, navigating the portal can be bit frustrating and time consuming as there is no simple intuitive API or download link for the dataset you are interested in. You have to hop around multiple pages to go to the raw dataset page that you are looking for. Also, if you are interested in particular type of ML task (regression or classification for example) and want to download all datasets corresponding to that task, there is no simple command to accomplish such.

### Introducing UCIML Python code base
This is a MIT-licensed Open-source Python 3.6 codebase which offers functions and methods to allow an user play with the UCI ML datasets in an interactive manner. Download/clone/fork the codebase from my **[Github page here](https://github.com/tirthajyoti/UCI-ML-API)**.

### Required packages
Only three widely used Python packages are required to run this code. For easy installation of these supporting packages, setup.bash and setup.bat files are included in my repo. Just execute them in your Linux/Windows shell and you are ready!
* [Pandas](https://pandas.pydata.org/)
* [Beautifulsoup 4](https://www.crummy.com/software/BeautifulSoup/?)
* [Requests](http://docs.python-requests.org/en/master/)

### How to run it?
Just download/clone the Gitgub repo, make sure to have the supporting packages installed and run the following command at your terminal.

**`python Main.py`**

A menu will open up allowing you to perform various tasks. 
Here is a screenshot of the menu,

![Menu](https://raw.githubusercontent.com/tirthajyoti/tirthajyoti.github.io/master/Images/UCI_ML_SC_1.PNG)

### Features and functions currently supported
Following features are currently implemented...
* Building a local database of name, description, and URL of datasets by crawling the entire portal
* Building a local database of name, size, machine learning task of datasets by crawling the entire portal
* Search and download a particular dataset
* Download first few datasets
* Print names of all datasets
* Print short descriptions of all datasets
* Search for one-liner description and webpage link (for more info) of a dataset
* Download datasets based on their size
* Download datasets based on the machine learning task associated with them

#### So, give it a try and put a star to my [Github repo](https://github.com/tirthajyoti/UCI-ML-API) if you like it.

Feedbacks and suggestions for improvements are most welcome at [tirthajyoti@gmail.com](mailto:tirthajyoti@gmail.com)

