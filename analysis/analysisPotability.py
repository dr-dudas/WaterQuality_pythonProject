####
####
####
####

########################################################################################################

### IMPORTS
import data_modelling
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb


########################################################################################################

### RQ - How can we correlate the Potability of water with the rest of the parameters?


# Exploring the potability values
def potability_distribution(csv_file: str):
    '''
    Docstring for potability_distribution
    
    :param csv_file: Description
    :type csv_file: str
    '''

    df = data_modelling.read_clean_general(csv_file)

    plt.figure(figsize=(5, 3)) 
    sb.histplot(df['Potability'], bins=20, kde=True)  
    plt.title('Potability distribution')
    plt.xlabel('Potability')
    plt.ylabel('Frequency')
    plt.grid(True)
    plt.show()

# Exploring the relationship between potability and the rest of the variables

def potability_correlations(csv_file: str):
    '''
    Docstring for potability_relationships
    
    :param csv_file: Description
    :type csv_file: str
    '''
    df = data_modelling.read_clean_general(csv_file)

    non_potable = df.query("Potability == 0")
    potable = df.query("Potability == 1")

    plt.figure(figsize = (9,9))
    for ax, col in enumerate(df.columns[:9]):
        plt.subplot(3,3, ax + 1)
        plt.title(col)
        sb.kdeplot(x = non_potable[col], label = "Non Potable")
        sb.kdeplot(x = potable[col], label = "Potable")
        plt.legend()
    plt.tight_layout()
    plt.show()


########################################################################################################

#### TESTING ####

#potability_distribution('water_potability.csv')
potability_correlations('water_potability.csv')