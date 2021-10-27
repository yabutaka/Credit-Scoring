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


numerical_features = ['ApplicantIncome', 'CoapplicantIncome',
 'LoanAmount', 'Loan_Amount_Term', 'Credit_History']
categorical_features = ['Gender', 'Married', 'Dependents',
 'Education', 'Self_Employed', 'Property_Area', 'Loan_Status']
drop_features = []


col_vals = x.columns.values[-1:].tolist() +  x.columns.values[:-1].tolist()
x = x[col_vals]
x['Loan_Status'] = x['Loan_Status'].replace({"Y": 1, "N": 0})


#Filling missing values of numerical features with mean
x['LoanAmount'] = x['LoanAmount'].fillna(x['LoanAmount'].mean())
x['Loan_Amount_Term'] = x['Loan_Amount_Term'].fillna(x['Loan_Amount_Term'].mean())
x['Credit_History'] = x['Credit_History'].fillna(x['Credit_History'].mean())

#Filling missing values of categorical features with mode
x['Gender'] = x['Gender'].fillna(x['Gender'].mode()[0])
x['Married'] = x['Married'].fillna(x['Married'].mode()[0])
x['Dependents'] = x['Dependents'].fillna(x['Dependents'].mode()[0])
x['Self_Employed'] = x['Self_Employed'].fillna(x['Self_Employed'].mode()[0])


# new columns
x['Total_Income'] = x['ApplicantIncome'] + x['CoapplicantIncome']

drop_features.append('ApplicantIncome')
drop_features.append('CoapplicantIncome')

x['ApplicantIncomeLog'] = np.log(x['ApplicantIncome'].replace({0:0.1}))
drop_features.append('ApplicantIncome')

x['CoapplicantIncomeLog'] = np.log(x['CoapplicantIncome'].replace({0:0.1}))
drop_features.append('CoapplicantIncome')

x['LoanAmountLog'] = np.log(x['LoanAmount'].replace({0:0.1}))
drop_features.append('LoanAmount')

x['Loan_Amount_Term_log'] = np.log(x['Loan_Amount_Term'].replace({0:0.1}))
drop_features.append('Loan_Amount_Term')

x['Total_Income_Log'] = np.log(x['Total_Income'].replace({0:0.1}))
drop_features.append('Total_Income')


# onehot
x = pd.get_dummies(data=x, columns=categorical_features, drop_first=True)


# camel case
x = x.rename({"Loan_ID": "loanID", 
          "ApplicantIncome": "applicantIncome", 
          "CoapplicantIncome": "coapplicantIncome", 
          "LoanAmount": "loanAmount",
          "Loan_Amount_Term": "loanAmountTerm",
          "Credit_History": "satisfactoryCreditHistory",
          "Total_Income": "totalIncome",
          "ApplicantIncomeLog": "applicantIncomeLog",
          "CoapplicantIncomeLog": "coapplicantIncomeLog",
          "LoanAmountLog": "loanAmountLog",
          "Loan_Amount_Term_log": "loanAmountTermLog",
          "Total_Income_Log": "totalIncomeLog",
          "Gender_Male": "isMale",
          "Married_Yes": "isMarried",
          "Dependents_1": "has1Dependent",
          "Dependents_2": "has2Dependents",
          "Dependents_3+": "has3+Dependents",
          "Education_Not Graduate": "hasNotGraduated",
          "Self_Employed_Yes": "isSelfEmployed",
          "Property_Area_Semiurban": "livesSemiurbal",
          "Property_Area_Urban": "livesUrban",
          "Loan_Status_1": "outcome"}, axis='columns')



x.to_csv('screening_data.csv', index=False)


