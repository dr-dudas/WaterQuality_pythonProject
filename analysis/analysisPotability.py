####
####
####
####

########################################################################################################

### IMPORTS
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.graph_objects as gpo
from scipy.stats import ttest_ind
#from data_modelling import read_clean_general

########################################################################################################

### RQ - How can we correlate the Potability of water with the rest of the parameters?

# Exploring the relationship between potability and the rest of the variables

def potability_correlations(df: pd.DataFrame):
    '''
    Docstring for potability_relationships
    
    :param df: Description
    :type df: pd.Dataframe
    '''

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
    return plt

def splom_graph(df:pd.DataFrame) -> gpo.Figure:
    '''
    Docstring for splom_graph
    
    :param df: Description
    :type df: pd.Dataframe
    '''

    textPotability = ['Safe to drink' if cl == 1 else 'Unsafe to drink' for cl in df['Potability'] ]

    fig = gpo.Figure(data=gpo.Splom(
            dimensions=[dict(label = 'pH', values = df['ph']),
                        dict(label = 'Hardness', values = df['Hardness']),
                        dict(label = 'Solids', values = df['Solids']),
                        dict(label = 'Chloramines', values = df['Chloramines']),
                        dict(label = 'Sulfate', values = df['Sulfate']),
                        dict(label = 'Conductivity', values = df['Conductivity']),
                        dict(label = 'Organic carbon', values = df['Organic_carbon']),
                        dict(label = 'Trihalomethanes', values = df['Trihalomethanes']),
                        dict(label = 'Turbidity', values = df['Turbidity']),
                        ],
            showupperhalf=False,
            text=textPotability,
            marker = dict(color = df['Potability'],
                            size = 5,
                            colorscale = 'Bluered',
                            showscale = False,
                            line_color = 'white',
                            line_width = 0.5)
        )
    )

    fig.update_layout(
            title=dict(text="Water Data set"),
            hoversubplots="axis",
            width=1300,
            height=1300,
            hovermode="x",
    )

    return fig
    

def correlationPot_graph(df:pd.DataFrame) -> px.imshow:
    '''
    Docstring for correlationPot_graph
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Any
    '''

    correlation_matrix = df.corr()

    fig = px.imshow(correlation_matrix,
                    height=600,
                    width=600,
                    text_auto=True, 
                    title="Correlation matrix for water data set",
                    color_continuous_midpoint=0.0,
                    range_color=[-1, 1]
                    )

    return fig

def boxplot_solids(df: pd.DataFrame) -> px.box:
    '''
    Docstring for boxplot_solids
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Any
    '''

    fig_sulfate = px.box(
        df,
        x='Potability',
        y='Sulfate',
        color='Potability',
        title='Sulfate vs Potability'
    )
    fig_sulfate.update_layout(width=500, height=600)
    
    return fig_sulfate

def boxplot_chloramines(df:pd.DataFrame) -> px.box:
    '''
    Docstring for boxplot_chloramines
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Any
    '''

    fig_chloramines = px.box(
        df,
        x='Potability',
        y='Chloramines',
        color='Potability',
        title='Chloramines vs Potability'
    )
    fig_chloramines.update_layout(width=500, height=600)

    return fig_chloramines

def t_tests(df:pd.DataFrame):
    '''
    Docstring for t_tests
    
    :param df: Description
    :type df: pd.Dataframe
    '''

    #null hyp - the mean of any parameter is the same for potable and non-potable water
    #ha - mean of any parameter is different between potable and non-potable water
    
    non_potable = df.query("Potability == 0")
    potable = df.query("Potability == 1")

########################################################################################################

#### TESTING ####
#df = read_clean_general('data\water_potability.csv')

#potability_correlations(df)
#correlationPot_graph('data\water_potability.csv')
#splom_graph('data\water_potability.csv')


#t_tests('data\water_potability.csv')
