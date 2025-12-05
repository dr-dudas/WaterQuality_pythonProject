#### GROUP INFO
####
####
####

#### IMPORTS ####

import pandas as pd

########################################################################################################

#### FUNCTIONS ####

def read_and_clean_general(file_path:str) -> pd.DataFrame:
    '''
    Docstring for read_and_clean
    
    :param file_path: Description
    :type file_path: str
    :return: Description
    :rtype: DataFrame
    '''
    df = pd.read_csv(file_path)
    
    df = df.drop_duplicates()

    df['ph'] = df['ph'].fillna(df['ph'].mean())
    df['Hardness'] = df['Hardness'].fillna(df['Hardness'].mean())
    df['Solids'] = df['Solids'].fillna(df['Solids'].mean())
    df['Chloramines'] = df['Chloramines'].fillna(df['Chloramines'].mean())
    df['Sulfate'] = df['Sulfate'].fillna(df['Sulfate'].mean())
    df['Conductivity'] = df['Conductivity'].fillna(df['Conductivity'].mean())
    df['Organic_carbon'] = df['Organic_carbon'].fillna(df['Organic_carbon'].mean())
    df['Trihalomethanes'] = df['Trihalomethanes'].fillna(df['Trihalomethanes'].mean())
    df['Turbidity'] = df['Turbidity'].fillna(df['Turbidity'].mean())
    df['Potability'] = df['Potability'].fillna(df['Potability'].mean())

    #print(df.columns)
    #print(df.isna().sum())
    return df


########################################################################################################

#### TESTING ####