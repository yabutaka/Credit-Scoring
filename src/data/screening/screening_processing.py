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
          "Education": "hasGraduated",
          "Self_Employed": "selfEmployed",
          "ApplicantIncome": "applicantIncome",
          "CoapplicantIncome": "coapplicantIncome",
          "LoanAmount": "loanAmount",
          "Loan_Amount_Term": "loanAmountTerm",
          "Credit_History": "satisfactoryCreditHistory",
          "Property_Area": "propertyAreaPopulation" }, axis='columns')


# missing values of numerical columns with mean 
x['loanAmount'] = x['loanAmount'].fillna(x['loanAmount'].mean())
x['loanAmountTerm'] = x['loanAmountTerm'].fillna(x['loanAmountTerm'].mean())
x['satisfactoryCreditHistory'] = x['satisfactoryCreditHistory'].fillna(x['satisfactoryCreditHistory'].mean())

# missing values of categorical columns with mode
x['gender'] = x['gender'].fillna(x['gender'].mode()[0])
x['married'] = x['married'].fillna(x['married'].mode()[0])
x['dependents'] = x['dependents'].fillna(x['dependents'].mode()[0])
x['selfEmployed'] = x['selfEmployed'].fillna(x['selfEmployed'].mode()[0])

# categorical cols to numerical
x['gender'] = x['gender'].replace({"Male": 1, "Female": 0})
x['selfEmployed'] = x['selfEmployed'].replace({"No": 0, "Yes": 1})
x['married'] = x['married'].replace({"No": 0, "Yes": 1})
x['hasGraduated'] = x['hasGraduated'].replace({"Graduate": 1, "Not Graduate": 0})
x['propertyAreaPopulation'] = x['propertyAreaPopulation'].replace(
     {"Rural": 1, "Semiurban": 2, "Urban":3})
x["satisfactoryCreditHistory"] = x["satisfactoryCreditHistory"].astype(int)
temp = x["dependents"].replace("3+", "3")
x["dependents"] = temp.astype(int)

# add columns
# np.seterr(divide = 'ignore') 
x['totalIncome'] = x['applicantIncome'] + x['coapplicantIncome']
x['applicantIncomeLog'] = np.log(x['applicantIncome'].replace({0:0.1}))
x['coapplicantIncomeLog'] = np.log(x['coapplicantIncome'].replace({0:0.1}))
x['loanAmountLog'] = np.log(x['loanAmount'].replace({0:0.1}))
x['loanAmountTermLog'] = np.log(x['loanAmountTerm'])
x['totalIncomeLog'] = np.log(x['totalIncome'].replace({0:0.1}))

x.to_csv('screening_data.csv', index=False)


