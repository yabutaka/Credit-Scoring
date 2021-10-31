import pandas as pd
import re

df_train = pd.read_csv("raw/train.csv")
df_test = pd.read_csv("raw/test.csv")

df = df_train

df_train.columns = pd.Series(df_train.columns).apply(lambda x: x.lower())

def create_camel_case(myString, seperator):
    lst = myString.split(seperator)
    if len(lst) < 2:
        return myString
    else:
        for i in range(len(lst)):
            if i != 0:
                lst[i] = lst[i][0].upper() + lst[i][1:]
        return ''.join(lst)

df.columns = pd.Series(df.columns).apply(create_camel_case, 
                              seperator = '_').apply(create_camel_case,
                              seperator = '.')

df.columns

df.columns = ['uniqueId', 'disbursedAmount', 'assetCost', 'itv', 'branchId',
'supplierId', 'manufacturerId', 'currentPincodeId', 'dateOfBirth',
'employmentType', 'disbursaldate', 'stateId', 'employeeCodeId',
'mobilenoAvlFlag', 'aadharFlag', 'panFlag', 'voteridFlag',
'drivingFlag', 'passportFlag', 'performCnsScore',
'performCnsScoreDescription', 'priNoOfAccts', 'priActiveAccts',
'priOverdueAccts', 'priCurrentBalance', 'priSanctionedAmount',
'priDisbursedAmount', 'secNoOfAccts', 'secActiveAccts',
'secOverdueAccts', 'secCurrentBalance', 'secSanctionedAmount',
'secDisbursedAmount', 'primaryInstalAmt', 'secInstalAmt',
'newAcctsInLastSixMonths', 'delinquentAcctsInLastSixMonths',
'averageAcctAge', 'creditHistoryLength', 'noOfInquiries',
'loanDefault']

df.isna().sum()

df.employmentType.value_counts()        

df.employmentType = df.employmentType.fillna("Unknown")

df.iloc[0]

df.averageAcctAge = df.averageAcctAge.apply(lambda x: float(str(re.search(r'\d+', x.split(" ")[0]).group()) + 
                        '.' + str(re.search(r'\d+', x.split(" ")[1]).group())))

df.creditHistoryLength = df.creditHistoryLength.apply(lambda x: float(str(re.search(r'\d+', x.split(" ")[0]).group()) + 
                        '.' + str(re.search(r'\d+', x.split(" ")[1]).group())))

df

temp = df.loanDefault
df = df.drop("loanDefault", axis = 1)
df.insert(0, 'loanDefault', temp)

df

df.to_csv("vehicle_loan_data.csv", index = False)

df_col = pd.read_csv("raw/data_dictionary.csv")

df_col = df_col.drop("Unnamed: 0", axis = 1)

df_col.insert(0, 'colName', ['uniqueId', 'loanDefault', 'disbursedAmount', 'assetCost', 'itv',
       'branchId', 'supplierId', 'manufacturerId', 'currentPincodeId',
       'dateOfBirth', 'employmentType', 'disbursaldate', 'stateId',
       'employeeCodeId', 'mobilenoAvlFlag', 'aadharFlag', 'panFlag',
       'voteridFlag', 'drivingFlag', 'passportFlag', 'performCnsScore',
       'performCnsScoreDescription', 'priNoOfAccts', 'priActiveAccts',
       'priOverdueAccts', 'priCurrentBalance', 'priSanctionedAmount',
       'priDisbursedAmount', 'secNoOfAccts', 'secActiveAccts',
       'secOverdueAccts', 'secCurrentBalance', 'secSanctionedAmount',
       'secDisbursedAmount', 'primaryInstalAmt', 'secInstalAmt',
       'newAcctsInLastSixMonths', 'delinquentAcctsInLastSixMonths',
       'averageAcctAge', 'creditHistoryLength', 'noOfInquiries'])

df_col = df_col.drop(["Variable Name", "Unnamed: 2"], axis = 1)

df_col.columns = 'colName', 'description'

df_col = df_col.reindex([1, 0] + list(range(2, 41))).reset_index(drop = True)

df_col['min'] = df.min().values
df_col['max'] = df.max().values

df_col

df_col.to_csv("vehicle_loan_info.csv", index = False)

