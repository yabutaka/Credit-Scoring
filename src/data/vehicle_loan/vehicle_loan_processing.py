import pandas as pd
import re
import numpy as np

df = pd.read_csv("raw/train.csv")
#df_test = pd.read_csv("raw/test.csv")

df.columns = pd.Series(df.columns).apply(lambda x: x.lower())

## Calculate Age

df['date.of.birth'].max()

df['disbursaldate'].min()

df['age'] = (df['disbursaldate'].apply(lambda x: int("20" + x.split("-")[2])) - 
df['date.of.birth'].apply(lambda x: int("19" + x.split("-")[2])))

df = df.drop(['disbursaldate','date.of.birth'],axis=1)

## Unify column name format

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

df.columns = ['uniqueId', 'disbursedAmount', 'assetCost', 'itv', 'branchId',
'supplierId', 'manufacturerId', 'currentPincodeId',
'employmentType', 'stateId', 'employeeCodeId',
'mobilenoAvlFlag', 'aadharFlag', 'panFlag', 'voteridFlag',
'drivingFlag', 'passportFlag', 'performCnsScore',
'performCnsScoreDescription', 'priNoOfAccts', 'priActiveAccts',
'priOverdueAccts', 'priCurrentBalance', 'priSanctionedAmount',
'priDisbursedAmount', 'secNoOfAccts', 'secActiveAccts',
'secOverdueAccts', 'secCurrentBalance', 'secSanctionedAmount',
'secDisbursedAmount', 'primaryInstalAmt', 'secInstalAmt',
'newAcctsInLastSixMonths', 'delinquentAcctsInLastSixMonths',
'averageAcctAge', 'creditHistoryLength', 'noOfInquiries',
'loanDefault', 'age']

df.isna().sum()[df.isna().sum() != 0]

df.employmentType.value_counts()        

df.employmentType = df.employmentType.fillna("Unknown")

df.iloc[0]

df.averageAcctAge = df.averageAcctAge.apply(lambda x: float(str(re.search(r'\d+', x.split(" ")[0]).group()) + 
                        '.' + str(re.search(r'\d+', x.split(" ")[1]).group())))

df.creditHistoryLength = df.creditHistoryLength.apply(lambda x: float(str(re.search(r'\d+', x.split(" ")[0]).group()) + 
                        '.' + str(re.search(r'\d+', x.split(" ")[1]).group())))

df.iloc[0]

temp = df.loanDefault
df = df.drop("loanDefault", axis = 1)
df.insert(0, 'loanDefault', temp)

df

df.columns

## Select right features to use

selected_feature = [
       'loanDefault', 'age', 'disbursedAmount', 'assetCost', 'itv',
       'employmentType', 'mobilenoAvlFlag', 'aadharFlag', 'panFlag',
       'voteridFlag', 'drivingFlag', 'passportFlag', 'performCnsScore',
       'priNoOfAccts', 'priActiveAccts',
       'priOverdueAccts', 'priCurrentBalance', 'priSanctionedAmount',
       'priDisbursedAmount', 'secNoOfAccts', 'secActiveAccts',
       'secOverdueAccts', 'secCurrentBalance', 'secSanctionedAmount',
       'secDisbursedAmount', 'primaryInstalAmt', 'secInstalAmt',
       'newAcctsInLastSixMonths', 'delinquentAcctsInLastSixMonths',
       'averageAcctAge', 'creditHistoryLength', 'noOfInquiries'
]

df = df[selected_feature]

one_hot = pd.get_dummies(df['employmentType'])
df = df.join(one_hot)
df = df.drop('employmentType',axis = 1)

df.columns = ['loanDefault', 'age', 'disbursedAmount', 'assetCost', 'itv',
       'mobilenoAvlFlag', 'aadharFlag', 'panFlag', 'voteridFlag',
       'drivingFlag', 'passportFlag', 'performCnsScore', 'priNoOfAccts',
       'priActiveAccts', 'priOverdueAccts', 'priCurrentBalance',
       'priSanctionedAmount', 'priDisbursedAmount', 'secNoOfAccts',
       'secActiveAccts', 'secOverdueAccts', 'secCurrentBalance',
       'secSanctionedAmount', 'secDisbursedAmount', 'primaryInstalAmt',
       'secInstalAmt', 'newAcctsInLastSixMonths',
       'delinquentAcctsInLastSixMonths', 'averageAcctAge',
       'creditHistoryLength', 'noOfInquiries', 'salaried', 'selfEmployed',
       'unknownEmploy']

df.iloc[0]

df.to_csv("vehicle_loan_data.csv", index = False)

