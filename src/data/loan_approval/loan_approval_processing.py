import numpy as np
import pandas as pd 
import os.path


data_samp = os.path.join("raw", "Sample_Submission.csv")
data_test = os.path.join("raw", "Test Dataset.csv")
data_train = os.path.join("raw", "Train Dataset.csv")


samp = pd.read_csv(data_samp)
test = pd.read_csv(data_test)
train = pd.read_csv(data_train)
test = pd.DataFrame.merge(test, samp, on = "Loan_ID")
x = pd.concat([train, test])

col_vals = x.columns.values[-1:].tolist() +  x.columns.values[:-1].tolist()
x = x[col_vals]
x['Loan_Status'] = x['Loan_Status'].replace({"Y": 1, "N": 0})


# camel case 
x = x.rename({"Loan_Status": "outcome", 
          "Loan_ID": "loanID", 
          "Gender": "gender", 
          "Married": "married",
          "Dependents": "dependents",
          "Education": "education",
          "Self_Employed": "selfEmployed",
          "ApplicantIncome": "applicantIncome",
          "CoapplicantIncome": "coapplicantIncome",
          "LoanAmount": "loanAmount",
          "Loan_Amount_Term": "loanAmountTerm",
          "Credit_History": "creditHistory",
          "Property_Area": "propertyArea" }, axis='columns')

# drop ID column 
x = x.drop(['loanID'], axis=1)

# drop gender column 
x = x.drop(['gender'], axis=1)

# dropped loanAmount null
x = x.dropna(subset=['loanAmount'], how='all')
x = x.dropna(subset=['loanAmountTerm'], how='all')

# selfEmployed
x["selfEmployed"].fillna( value ='No', inplace = True)
x['selfEmployed'] = x['selfEmployed'].replace({"No": 0, "Yes": 1})

# married to binary
x["married"].fillna( value ='No', inplace = True)
x['married'] = x['married'].replace({"No": 0, "Yes": 1})

# education to binary. (graduate --> 1, not graduated --> 0)
x['education'] = x['education'].replace({"Graduate": 1, "Not Graduate": 0})

# propertyArea --> (rural --> 1, semiurban --> 2, urban --> 3)
x['propertyArea'] = x['propertyArea'].replace({"Rural": 1, "Semiurban": 2, "Urban":3})

# credit history 
x["creditHistory"].fillna(value =0, inplace = True)
x["creditHistory"] = x["creditHistory"].astype(int)

# dependents
temp = x["dependents"].replace("3+", "3")
median_dependents = temp[temp.notnull()].median()
temp.fillna(value = median_dependents, inplace = True)
x["dependents"] = temp.astype(int)

x.to_csv('loan_approval_data.csv', index=False)