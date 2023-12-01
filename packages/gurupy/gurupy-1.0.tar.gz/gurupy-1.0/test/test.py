import pandas as pd
import setuptools
import gurupy
from dotenv import load_dotenv
import os


# Set variables
load_dotenv()
token = os.getenv('gt')
ticker = 'txn'


x = gurupy.dividend_history_exdate_index_df(token, ticker)
print(x)



