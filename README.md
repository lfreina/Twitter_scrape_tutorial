# Twitter_scrape_tutorial
Scrape Twitter for a search word and get 5 similar words and the 5 most frequent words around the search word.
Built in Python3.x

## Setup
To install modules, you need the python package manager pip (sudo apt-get install pip).

### Required files
You will need the files from The Swedish Word Vectors from 10M blog posts from Mattias Östmar.
You can find the files at: https://osf.io/y37g2/

### Virtual environment
It is recommended to use a virtual environment to install packages in, so they don't get installed globally.
There are many tools for this but the most used low-lever is called virtualenv.

> pip install virtualenv

Create a virtual environment for a project:

> cd my_project_folder && virtualenv env -p python3.6

This creates a copy of Python3.6 in whichever directory you ran the command in, placing it in a folder named 'env'.
To begin using the virtual environment, it needs to be activated:

> source env/bin/activate

This will now show in the terminal prompt. To deactivate the venv, just use the command

> deactivate

In Pycharm, you can also choose the virtualenv to be the standard python interpreter.

### Installation
The easiest way to install the module and the required packages is to use pip.
The following will install the required python packages.
Don't forget to activate your virtual environment first!

>pip install twitterscraper gensim nltk

