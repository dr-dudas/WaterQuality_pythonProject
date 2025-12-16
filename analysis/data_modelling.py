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
    df['Sulfate'] = df['Sulfate'].fillna(df['Sulfate'].mean())
    df['Trihalomethanes'] = df['Trihalomethanes'].fillna(df['Trihalomethanes'].mean())

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

def missing_values_summary(df: pd.DataFrame) -> pd.Series:
    '''
    This function returns a Series with the count of missing values for each column.
    
    :param df: dataframe
    :type df: pd.DataFrame
    :return: Series with count of missing values for each column
    '''
    missing_values = df.isnull().sum()
    return missing_values

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

def add_missing_value_column(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds a column 'missing_value' to the dataframe, containing
    the count of missing values (NaN) in each row.

    param df: Dataframe
    type df: pd.DataFrame
    returns: pd.DataFrame: Dataframe copy with an additional 'missing_value' column,
        with an integer value corresponding to the number of missing values for that row.
    """
    df = df.copy()  # avoid mutating the original dataframe
    df["missing_value"] = df.isnull().sum(axis=1)
    return df

# df = read_clean_general('water_potability.csv')
# introduction_to_data(df)
# distribution_visualization(df)
# correlation_heatmap(df)
########################################################################################################

#### TESTING ####