# ShieldB - Data Masking

### Overview

ShieldB is a powerful data masking and file deletion tool designed to enhance data privacy and ensure compliance with various data protection regulations. This tool allows you to protect sensitive information in your database and selectively delete files from a specified directory, providing a comprehensive solution for managing and securing your data.


### Installation

To use ShieldB, you need to install it as a Python package from the Python Package Index (PyPI). Open your terminal and run the following command:


pip install shieldb

### Configuration

After installing the package, you need to set the SQLALCHEMY_DATABASE_URI environment variable. This variable should contain the URI for your PostgreSQL database where ShieldB will perform its operations.

export SQLALCHEMY_DATABASE_URI="your_postgresql_uri_here" (MAC or Linux)

$env:SQLALCHEMY_DATABASE_URI = 'your_postgresql_uri_here' (Windows)

### USAGE

#### Data Masking

Data Masking with ShieldB

1-) To start, type shieldb in the terminal.<br>
2-) From the options displayed, select the mask action.<br>
3-) Enter the name of the table you wish to work with accurately.<br>
4-) Input the columns you want to mask. Multiple columns can be entered.<br>
5-) Choose the type of masking (e.g., shuffle, regex, reverse).

#### Data Deletion

Data Deletion with ShieldB

1-) To start, type shieldb in the terminal.<br>
2-) From the options displayed, select the delete action.<br>
3-) Enter the name of the table you wish to work with accurately.<br>
4-) Enter the percentage of data to be deleted (an integer between 0 and 100).

### DEPENDENCIES


SQLAlchemy~=2.0.23<br>
psycopg2-binary~=2.9.1<br>
inquirerpy~=0.3.4<br>
nltk~=3.8.1<br>
setuptools~=60.2.0
