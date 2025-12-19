####
####
####
####

########################################################################################################

### IMPORTS
import pandas as pd
import plotly.express as px
import plotly.figure_factory as ff
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn import metrics

#from data_modelling import read_clean_general

########################################################################################################

### RQ - How can we correlate the Potability of water with the rest of the parameters?

# Exploring the relationship between potability and the rest of the variables

def densityplot_solids(df: pd.DataFrame) -> ff.create_distplot:
    '''
    Docstring for densityPlots
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Any
    '''

    potable = df[df['Potability'] == 1]['Solids']
    non_potable = df[df['Potability'] == 0]['Solids']

    # Create a figure
    fig = ff.create_distplot(
        hist_data=[non_potable, potable],
        group_labels=['Non Potable', 'Potable'],
        show_hist=False,
        show_rug=False,
        colors=['blue', 'orange']
    )

    # Update layout
    fig.update_layout(
        title='Solids Density by Potability',
        xaxis_title='Solids',
        yaxis_title='Density',
        width=600,
        height=500
    )

    return fig

def densityplot_chloramines(df: pd.DataFrame) -> ff.create_distplot:
    '''
    Docstring for densityPlots
    
    :param df: Description
    :type df: pd.DataFrame
    :return: Description
    :rtype: Any
    '''

    potable = df[df['Potability'] == 1]['Chloramines']
    non_potable = df[df['Potability'] == 0]['Chloramines']

    # Create a figure
    fig = ff.create_distplot(
        hist_data=[non_potable, potable],
        group_labels=['Non Potable', 'Potable'],
        show_hist=False,
        show_rug=False,
        colors=['blue', 'orange']
    )

    # Update layout
    fig.update_layout(
        title='Chloramines Density by Potability',
        xaxis_title='Chloramines',
        yaxis_title='Density',
        width=600,
        height=500
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
        y='Solids',
        color='Potability',
        title='Solids vs Potability'
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
        title='Chloramines vs Potability',
    )
    fig_chloramines.update_layout(width=500, height=600)

    return fig_chloramines

def logRegression(df:pd.DataFrame):

    x = df[['Solids', 'Chloramines']]
    y = df[['Potability']]
  
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

    log_regression = LogisticRegression()
    log_regression.fit(x_train, y_train.values.ravel())
    y_pred = log_regression.predict(x_test)

    conf_matrix = metrics.confusion_matrix(y_test, y_pred)
    accuracy = metrics.accuracy_score(y_test, y_pred)

    z_text = [[str(y) for y in x] for x in conf_matrix]
    
    fig_confMatrix = ff.create_annotated_heatmap(
        z = conf_matrix,
        x = ['Predicted Potable', 'Predicted Non-Potable'],
        y = ['Actual Potable', 'Actual Non-potable'],
        annotation_text=z_text, 
        colorscale='Viridis'
    )

    fig_confMatrix.update_layout(title_text='<i><b>Confusion matrix</b></i>')

    fig_confMatrix.add_annotation(dict(font=dict(color="black",size=14),
                        x=0.5,
                        y=-0.15,
                        showarrow=False,
                        text="Predicted value",
                        xref="paper",
                        yref="paper"))

    # add custom yaxis title
    fig_confMatrix.add_annotation(dict(font=dict(color="black",size=14),
                            x=-0.35,
                            y=0.5,
                            showarrow=False,
                            text="Real value",
                            textangle=-90,
                            xref="paper",
                            yref="paper"))

    # adjust margins to make room for yaxis title
    fig_confMatrix.update_layout(margin=dict(t=50, l=200))


    fig_confMatrix['data'][0]['showscale'] = True

    return fig_confMatrix, accuracy

########################################################################################################

