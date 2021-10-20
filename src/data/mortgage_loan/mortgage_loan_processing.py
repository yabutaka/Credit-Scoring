import pandas as pd

df_value = pd.read_csv("raw/train_values.csv")

df_label = pd.read_csv("raw/train_labels.csv")

df_test = pd.read_csv("https://www.dropbox.com/s/2heyrfbq3cxvsdb/test_values.csv?raw=1")

df_test

def create_camel_case(myString, seperator):
    lst = myString.split(seperator)
    if len(lst) < 2:
        return myString
    else:
        for i in range(len(lst)):
            if i != 0:
                lst[i] = lst[i][0].upper() + lst[i][1:]
        return ''.join(lst)

df_value.columns = pd.Series(df_value.columns).apply(create_camel_case, 
                              seperator = '_').apply(create_camel_case,
                              seperator = '-')

df_value.insert(0, 'accepted', df_label.accepted)

df_value = df_value.drop('rowId', axis = 1)

df_value = df_value.dropna()

df_value = df_value.replace(True, 1).replace(False, 0)

df_value.to_csv("mortgage_loan_data.csv", index = False)

feature_dict = { 
 'accepted': 'Indicates whether the mortgage application was accepted (successfully originated) with a value of 1 or denied with a value of 0',
 'loanType': 'Indicates if loan was; conventional, FHA-insured, VA-guaranteed, or FSA/RHS',
 'propertyType': 'Indicates if loan application was for; 1-4 family, manufactured, or multifamily',
 'loanPurpose': 'Indicates if loan application was for; home purchase, home improvement, or refinancing',
 'occupancy': 'Indicates if application property was; owner-occupied as principal dwelling, not owner-occupied, or not applicable',
 'loanAmount': 'Size of requested loan in thousands of US dollars',
 'preapproval': ' Indicates if; preapproval requested, preapproval not requested, or not applicable',
 'msaMd': 'Metropolitan Statistical Area/ Metropolitan Division (-1 as missing value)',
 'stateCode': 'Indicates the US state (-1 as missing value)',
 'countyCode': 'Indicates the county (-1 as missing value)',
 'applicantEthnicity': 'Ethnicity of applicant indicating; Hispanic or Latino, Not Hispanic or Latino, info not provided, or not applicable',
 'applicantRace': 'Race of applicant indicating; American Indian or Alaska Native, Asian, Black or African American, Native Hawaiian or Other Pacific Islander, White, info not provided, or not applicable',
 'applicantSex': 'Sex of applicant indicating; male, female, info not provided, or not applicable',
 'applicantIncome': 'Size of income in thousands of US dollars',
 'population': 'Total population in tract',
 'minorityPopulationPct': 'Percentage of minority population to total population for tract',
 'ffiecmedianFamilyIncome': 'FFIEC median family income in dollars for MSA/MD in which the tract is located (adjusted annually by FFIEC)',
 'tractToMsaMdIncomePct': 'Percentage of tract median family income compared to MSA/MD median family income',
 'numberOfOwnerOccupiedUnits': 'Number of dwellings, including individual condominiums, that are lived in by the owner',
 'numberOf1To4FamilyUnits': 'Dwellings that are built to house fewer than 5 families',
 'lender': 'The lender that approved or denied the loan',
 'coApplicant': 'Indicates whether there is a co-applicant or not'
}

col_df = pd.DataFrame(pd.Series(feature_dict)).reset_index()
col_df.columns = 'colName', 'description'

col_df['min'] = df_value.min().values
col_df['max'] = df_value.max().values

col_df.to_csv("mortgage_loan_info.csv", index = False)

