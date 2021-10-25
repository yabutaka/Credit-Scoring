import pandas as pd

# Save data file

raw_data_df = pd.read_csv('raw/cs-training.csv', index_col=0)

raw_data_df = raw_data_df[raw_data_df["MonthlyIncome"].notna()]
raw_data_df["Debt"] = raw_data_df["MonthlyIncome"] * raw_data_df["DebtRatio"] # Extract Debt amount
raw_data_df.drop("DebtRatio", axis=1, inplace=True)

raw_data_df.to_csv('give_me_credit_data.csv', index=False)

# Save metadata file

data_dict = {
    'name': ['SeriousDlqin2yrs', 'RevolvingUtilizationOfUnsecuredLines', 'age',
       'NumberOfTime30-59DaysPastDueNotWorse', 'MonthlyIncome',
       'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
       'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse',
       'NumberOfDependents', 'Debt'],
    'description': [
        'Person experienced 90 days past due delinquency or worse',
        'Total balance on credit cards and personal lines of credit except real estate and no installment debt like car loans divided by the sum of credit limits',
        'Age of borrower in years',
        'Number of times borrower has been 30-59 days past due but no worse in the last 2 years.',
        'Monthly income',
        'Number of Open loans (installment like car loan or mortgage) and Lines of credit (e.g. credit cards)',
        'Number of times borrower has been 90 days or more past due.',
        'Number of mortgage and real estate loans including home equity lines of credit',
        'Number of times borrower has been 60-89 days past due but no worse in the last 2 years.',
        'Number of dependents in family excluding themselves (spouse, children etc.)',
        'Monthly debt payments'
                   ],
    'upper_bound': [1.0, 50708.0, 103.0, 98.0, 3008750.0, 58.0, 98.0, 54.0, 98.0, 20.0, 478450.55915999995],
    'lower_bound': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}

info_df = pd.DataFrame(data_dict)
info_df.to_csv('give_me_credit_info.csv', index=False)