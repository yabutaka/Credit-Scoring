import pandas as pd

# Save data file

raw_data_df = pd.read_csv('raw/cs-training.csv', index_col=0)
raw_data_df = raw_data_df.dropna() # drop missing values
raw_data_df.to_csv('give_me_credit_data.csv', index=False)

# Save metadata file

data_dict = {
    'name': ['SeriousDlqin2yrs', 'RevolvingUtilizationOfUnsecuredLines', 'age',
       'NumberOfTime30-59DaysPastDueNotWorse', 'DebtRatio', 'MonthlyIncome',
       'NumberOfOpenCreditLinesAndLoans', 'NumberOfTimes90DaysLate',
       'NumberRealEstateLoansOrLines', 'NumberOfTime60-89DaysPastDueNotWorse',
       'NumberOfDependents'],
    'description': [
        'Person experienced 90 days past due delinquency or worse',
        'Total balance on credit cards and personal lines of credit except real estate and no installment debt like car loans divided by the sum of credit limits',
        'Age of borrower in years',
        'Number of times borrower has been 30-59 days past due but no worse in the last 2 years.',
        'Monthly debt payments, alimony,living costs divided by monthy gross income',
        'Monthly income',
        'Number of Open loans (installment like car loan or mortgage) and Lines of credit (e.g. credit cards)',
        'Number of times borrower has been 90 days or more past due.',
        'Number of mortgage and real estate loans including home equity lines of credit',
        'Number of times borrower has been 60-89 days past due but no worse in the last 2 years.',
        'Number of dependents in family excluding themselves (spouse, children etc.)'
                   ],
    'upper_bound': [1.0, 50708.0, 103.0, 98.0, 61106.5, 3008750.0, 58.0, 98.0, 54.0, 98.0, 20.0],
    'lower_bound': [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
}

info_df = pd.DataFrame(data_dict)
info_df.to_csv('give_me_credit_info.csv', index=False)