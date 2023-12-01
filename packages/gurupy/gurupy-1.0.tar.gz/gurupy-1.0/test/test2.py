import pandas as pd
import gurupy as gf
from dotenv import load_dotenv
import os


# Set variables
load_dotenv()
token = os.getenv('gt')
ticker = 'txn'

df_annual = pd.DataFrame()
x_loc = 0

data = gf.stock_financials(token, ticker)
df_a = pd.DataFrame.from_dict(data)
df_b = pd.json_normalize(df_a.loc['annuals'])

for item, values in df_b.items():
    series_expand = pd.Series(values, name=item).explode(ignore_index=True)
    df_series = series_expand.to_frame()
    df_annual = pd.concat([df_annual, df_series], axis=1)
    x_loc += 1

print(df_annual)