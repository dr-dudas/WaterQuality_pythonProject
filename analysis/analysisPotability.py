####
####
####
####

########################################################################################################

### IMPORTS
import data_modelling
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sb
import plotly.graph_objects as gpo
from scipy.stats import ttest_ind

########################################################################################################

### RQ - How can we correlate the Potability of water with the rest of the parameters?

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

def splom_graph(csv_file: str):
    '''
    Docstring for splom_graph
    
    :param csv_file: Description
    :type csv_file: str
    '''

    df = data_modelling.read_clean_general(csv_file)

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

    fig.show()
    

def correlationPot_graph(csv_file: str):
    '''
    Docstring for correlation_graph
    
    :param csv_file: Description
    :type csv_file: str
    '''

    df = data_modelling.read_clean_general(csv_file)

    correlation_matrix = df.corr()

    fig = px.imshow(correlation_matrix,
                    height=600,
                    width=600,
                    text_auto=True, 
                    title="Correlation matrix for water data set",
                    color_continuous_midpoint=0.0,
                    range_color=[-1, 1]
                    )

    fig.show()

def t_tests(csv_file: str):
    '''
    Docstring for t_tests
    
    :param csv_file: Description
    :type csv_file: str
    '''

    #null hyp - the mean of any parameter is the same for potable and non-potable water
    #ha - mean of any parameter is different between potable and non-potable water
    
    df = data_modelling.read_clean_general(csv_file)

    non_potable = df.query("Potability == 0")
    potable = df.query("Potability == 1")


    


def box_plots(csv_file: str):
    '''
    Docstring for violin_plots
    
    :param csv_file: Description
    :type csv_file: str
    '''
    df = data_modelling.read_clean_general(csv_file)

    fig_chloramines = px.box(
        df,
        x='Potability',
        y='Chloramines',
        color='Potability',
        title='Chloramines vs Potability'
    )
    fig_chloramines.update_layout(width=500, height=600)

    # Sulfate vs Potability
    fig_sulfate = px.box(
        df,
        x='Potability',
        y='Sulfate',
        color='Potability',
        title='Sulfate vs Potability'
    )
    fig_sulfate.update_layout(width=500, height=600)

    fig_chloramines.show()
    fig_sulfate.show()



########################################################################################################

#### TESTING ####

#potability_correlations('data\water_potability.csv')
#splom_graph('data\water_potability.csv')
#correlationPot_graph('data\water_potability.csv')
#box_plots('data\water_potability.csv')

#t_tests('data\water_potability.csv')
