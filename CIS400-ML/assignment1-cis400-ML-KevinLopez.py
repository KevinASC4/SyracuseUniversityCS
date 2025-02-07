# Generic inputs for most ML tasks
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Ridge
from sklearn.linear_model import Lasso
from sklearn.ensemble import RandomForestRegressor

pd.options.display.float_format = '{:,.2f}'.format

# setup interactive notebook mode
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

from IPython.core.display import display, HTML
import plotly
plotly.offline.init_notebook_mode(connected=True)
from plotly.graph_objs import *
from plotly import tools
import plotly.graph_objects as go
import seaborn as sns
# fetch data 
airline_data = pd.read_csv('C:\\Users\kevMi\Downloads\Invistico_Airline (1).csv')

print(airline_data.dtypes)
totalNan = int(airline_data.isnull().sum().sum())
columnsWNa= airline_data.isna().sum()
totalrows = len(airline_data) - 1
print("Total Nan values are", totalNan)
print("The columns with na are", columnsWNa )
print("The total num of rows are", totalrows)
print("There are 23 columns")
subset_data = airline_data.drop(columns = ['satisfaction', 'Gender', 'Customer Type', 'Type of Travel', 'Class'])
loopForData = subset_data.columns
for i in loopForData:
    currentMean = subset_data[i].mean()
    currentStd = subset_data[i].std()
    currentHist = subset_data[i].hist()
    print("The mean of", i, "is", currentMean)
    print("The Standard deviation of", i, "is", currentStd)
    print("The histogram of", i, "is", currentHist)
    plt.show()
if True:
    y_col = 'Arrival Delay in Minutes'
    x_col = 'Departure Delay in Minutes'

    df = airline_data[[x_col, y_col]].sort_values(by=x_col)
    plot_data = []
    plot_data.append(go.Scatter(x= df[x_col], y= df[y_col] , mode = 'markers'))

    layout = go.Layout(xaxis = dict(title=x_col), yaxis = dict(title= y_col), 
                       title = 'Plot of {} versus {}'.format(y_col, x_col))
    fig = go.Figure(data= plot_data, layout=layout)
    plotly.offline.iplot(fig)
    def visualize_by_features(list_of_features, y_col):
        for x_col in list_of_features:
            plot_data = []
            df = airline_data[[x_col, y_col]].sort_values(by=x_col)
            plot_data.append(go.Scatter(x= df[x_col], y= df[y_col], 
                            name = 'feature = {}'.format(x_col), mode = 'markers' ))

            layout = go.Layout(xaxis = dict(title=x_col), yaxis = dict(title= y_col), 
                            title = 'Data for {}'.format(y_col))
            fig = go.Figure(data= plot_data, layout=layout)
            plotly.offline.iplot(fig)
    airline_data.columns
    visualize_by_features(['Age','Flight Distance', 'Seat comfort', 'Food and drink'], 'Arrival Delay in Minutes')