python
import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
df = pd.read_excel('Ownership_Trading_Summary_MAR.xlsx')

# Create the Dash app
app = dash.Dash(__name__)

# App layout
app.layout = html.Div([
    html.H1("Ownership Trading Activities Dashboard"),
    dcc.Dropdown(
        id='group-dropdown',
        options=[{'label': group, 'value': group} for group in df['Group'].unique()],
        placeholder="Select a Trading Group"
    ),
    dcc.Graph(id='trading-graph'),
    dcc.Graph(id='volume-graph')
])

# Callback to update graphs
@app.callback(
    [
        Output('trading-graph', 'figure'),
        Output('volume-graph', 'figure')
    ],
    [Input('group-dropdown', 'value')]
)
def update_graphs(selected_group):
    if selected_group:
        filtered_df = df[df['Group'] == selected_group]
        trading_fig = px.bar(filtered_df, x='Date', y=['Buy Value (AED)', 'Sell Value (AED)'], title="Trading Values")
        volume_fig = px.line(filtered_df, x='Date', y=['Buy Volume', 'Sell Volume'], title="Trading Volumes")
    else:
        trading_fig = px.bar(df, x='Date', y=['Buy Value (AED)', 'Sell Value (AED)'], title="Trading Values")
        volume_fig = px.line(df, x='Date', y=['Buy Volume', 'Sell Volume'], title="Trading Volumes")

    return trading_fig, volume_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
