import pandas as pd
import numpy as np

nan_filled_cols = []
hmda_csv_name = "hmda_2017_nationwide_all-records_labels.csv"
#Read in HMDA data, about 6GB worth
hmda = pd.read_csv(hmda_csv_name)
#Make outcome column binary, replacing multi-categorical action_taken column
hmda['outcome'] = hmda.action_taken.apply(lambda x: 0 if x > 1 else 1)
#Make outcome column 1
hmda = hmda.set_index('outcome').reset_index()

for col in hmda.columns:
    tot = len(hmda[col])
    nans_tot = hmda[col].isna().sum()
    #Get percentage of each column taht is NaN
    perc = nans_tot / tot 
    #Fill NaNs with 0 for time being
    hmda[col] =  hmda[col].fillna(0)
    #If NaNs are more than 10% of column drop the column 
    if perc >= .1:
        nan_filled_cols.append(col)
hmda = hmda.drop(columns = nan_filled_cols)

types = [str(kind) for kind in hmda.dtypes.to_numpy()]
#di = data_info
di = {"Columns": list(hmda.columns), "Dtypes" : types }
di = pd.DataFrame(di)

hmda.to_csv("src/data/hmda_data.csv", index= False)
di.to_csv("src/data/hmda_info.csv", index = False)
