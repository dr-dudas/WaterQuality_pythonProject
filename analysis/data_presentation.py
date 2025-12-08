#### GROUP INFO
####
####
####

#### IMPORTS ####

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sb

########################################################################################################

#### FUNCTIONS ####

def read_clean_general(df_file_path:str) -> pd.DataFrame:
    '''
    This functions is given the directory of a .csv file and cleans the data.
    Removes duplicates and normalizes NaN (aka empty values) values.    
    :param df_file_path: dataframe directory/file path
    :type df_file_path: str
    :return: cleaned dataframe
    :rtype: DataFrame
    '''
    df = pd.read_csv(df_file_path)
    
    df = df.drop_duplicates()

    # normalizing the NaNs
    df['ph'] = df['ph'].fillna(df['ph'].mean())
    df['Hardness'] = df['Hardness'].fillna(df['Hardness'].mean())
    df['Solids'] = df['Solids'].fillna(df['Solids'].mean())
    df['Chloramines'] = df['Chloramines'].fillna(df['Chloramines'].mean())
    df['Sulfate'] = df['Sulfate'].fillna(df['Sulfate'].mean())
    df['Conductivity'] = df['Conductivity'].fillna(df['Conductivity'].mean())
    df['Organic_carbon'] = df['Organic_carbon'].fillna(df['Organic_carbon'].mean())
    df['Trihalomethanes'] = df['Trihalomethanes'].fillna(df['Trihalomethanes'].mean())
    df['Turbidity'] = df['Turbidity'].fillna(df['Turbidity'].mean())
    df['Potability'] = df['Potability'].fillna(df['Potability'].median())

    return df


########################################################################################################

def introduction_to_data(df:pd.DataFrame):
    '''
    Calls for various pandas functions and shows the different properties 
    and key characteristics of the dataframe.
    
    :param df: dataframe
    :type df: pd.DataFrame
    '''

    print(df.head())
    print(df.describe())
    print(df.info())

def distribution_visualization(df:pd.DataFrame):
    '''
    Docstring for visualization_ph
    
    :param df_file_path: Description
    :type df_file_path: str
    '''

    df.hist(figsize=(12,10), bins=20)
    plt.suptitle('Distributions')
    plt.show()

def  correlation_heatmap(df:pd.DataFrame):
    '''
    Docstring for heatmap
    
    :param df: Description
    :type df: pd.DataFrame
    '''

    sb.heatmap(df.corr(), annot=True, cmap='coolwarm')
    plt.title('Correlation heatmap')
    plt.show()

# df = read_clean_general('water_potability.csv')
# introduction_to_data(df)
# distribution_visualization(df)
# correlation_heatmap(df)
########################################################################################################

#### TESTING ####