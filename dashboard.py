import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# Load the data
df = pd.read_csv('TSLA_Prices.csv')
df['date'] = pd.to_datetime(df['date'])

# Calculate moving averages
df['MA50'] = df['close'].rolling(window=50).mean()
df['MA200'] = df['close'].rolling(window=200).mean()

# Placeholder sentiment data
np.random.seed(0)
df['sentiment'] = np.random.choice(['Positive', 'Neutral', 'Negative'], size=len(df))

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div(style={
    'backgroundImage': 'linear-gradient(rgba(0, 0, 0, 0.5), rgba(70, 70, 70, 0.5)), url(https://images.unsplash.com/photo-1518770660439-4636190af475?crop=entropy&cs=tinysrgb&fit=max&fm=jpg&ixid=MnwzNjUyOXwwfDF8c2VhcmNofDJ8fGZpbmFuY2V8ZW58MHx8fHwxNjg1MjY0NzYx&ixlib=rb-1.2.1&q=80&w=1080)',
    'backgroundSize': 'cover',
    'backgroundAttachment': 'fixed',  # Keeps the background fixed
    'padding': '20px',
    'color': '#fff',
    'minHeight': '100vh' 
}, children=[
    html.H1("Tesla Stock Data Dashboard", style={'textAlign': 'center', 'color': '#fff', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'padding': '10px', 'borderRadius': '5px'}),
    dcc.DatePickerRange(
        id='date-picker',
        min_date_allowed=df['date'].min(),
        max_date_allowed=df['date'].max(),
        start_date=df['date'].min(),
        end_date=df['date'].max(),
        style={'margin': '10px', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'color': '#fff', 'borderRadius': '5px'}
    ),
    dcc.Dropdown(
        id='chart-type-dropdown',
        options=[
            {'label': 'Line Chart', 'value': 'line'},
            {'label': 'Candlestick Chart', 'value': 'candlestick'}
        ],
        value='line',
        style={'margin': '10px', 'backgroundColor': 'rgba(255, 255, 255, 0.8)', 'color': '#000', 'borderRadius': '5px'}
    ),
    dcc.Graph(id='price-graph', style={'backgroundColor': 'rgba(0, 0, 0, 0.3)', 'borderRadius': '5px', 'height': '500px'}),
    html.Div(id='summary-stats', style={'textAlign': 'center', 'marginTop': 20, 'color': '#fff', 'backgroundColor': 'rgba(0, 0, 0, 0.5)', 'padding': '10px', 'borderRadius': '5px'}),
    dcc.Graph(id='volume-bar-chart', style={'backgroundColor': 'rgba(0, 0, 0, 0.3)', 'borderRadius': '5px', 'height': '400px'}),
    dcc.Graph(id='scatter-plot', style={'backgroundColor': 'rgba(0, 0, 0, 0.3)', 'borderRadius': '5px', 'height': '400px'}),
    dcc.Graph(id='heatmap', style={'backgroundColor': 'rgba(0, 0, 0, 0.3)', 'borderRadius': '5px', 'height': '400px'}),
    dcc.Graph(id='sentiment-bar-chart', style={'backgroundColor': 'rgba(0, 0, 0, 0.3)', 'borderRadius': '5px', 'height': '400px'}),
])

# Define the callback to update the graph
@app.callback(
    [Output('price-graph', 'figure'),
     Output('summary-stats', 'children'),
     Output('volume-bar-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('heatmap', 'figure'),
     Output('sentiment-bar-chart', 'figure')],
    [Input('chart-type-dropdown', 'value'),
     Input('date-picker', 'start_date'),
     Input('date-picker', 'end_date')]
)
def update_graph(chart_type, start_date, end_date):
    filtered_df = df[(df['date'] >= start_date) & (df['date'] <= end_date)]
    
    if filtered_df.empty:
        return go.Figure(), "No data available for the selected date range.", go.Figure(), go.Figure(), go.Figure(), go.Figure()

    if chart_type == 'line':
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['close'], mode='lines', name='Close Price', line=dict(color='#007bff')))
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['MA50'], mode='lines', name='50-Day MA', line=dict(dash='dash', color='orange')))
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['MA200'], mode='lines', name='200-Day MA', line=dict(dash='dash', color='green')))
    else:
        fig = go.Figure(data=[go.Candlestick(
            x=filtered_df['date'],
            open=filtered_df['open'],
            high=filtered_df['high'],
            low=filtered_df['low'],
            close=filtered_df['close'],
            name='Candlestick',
            increasing_line_color='green',
            decreasing_line_color='red',
            increasing_fillcolor='rgba(0, 100, 0, 0.5)',
            decreasing_fillcolor='rgba(255, 0, 0, 0.5)',
            line_width=3
        )])
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['MA50'], mode='lines', name='50-Day MA', line=dict(dash='dash', color='orange')))
        fig.add_trace(go.Scatter(x=filtered_df['date'], y=filtered_df['MA200'], mode='lines', name='200-Day MA', line=dict(dash='dash', color='green')))

    fig.update_layout(
        title='Tesla Stock Prices',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='#fff')
    )

    avg_price = filtered_df['close'].mean()
    max_price = filtered_df['close'].max()
    total_volume = filtered_df['volume'].sum()

    summary = f"Average Close Price: ${avg_price:.2f} | Max Close Price: ${max_price:.2f} | Total Volume: {total_volume:,}"

    # Additional visualizations
    bar_chart = px.bar(filtered_df, x='date', y='volume', title='Volume Over Time', labels={'volume': 'Volume'}, color='sentiment')
    scatter_plot = px.scatter(filtered_df, x='volume', y='close', title='Volume vs Close Price', labels={'volume': 'Volume', 'close': 'Close Price'}, color='sentiment')
    
    # Exclude non-numeric columns for correlation
    numeric_df = filtered_df.select_dtypes(include=[np.number])
    heatmap = px.imshow(numeric_df.corr(), title='Correlation Heatmap', labels={'color': 'Correlation'})

    # Sentiment analysis bar chart
    sentiment_counts = filtered_df['sentiment'].value_counts()
    sentiment_bar_chart = px.bar(x=sentiment_counts.index, y=sentiment_counts.values, title='Sentiment Distribution', labels={'x': 'Sentiment', 'y': 'Count'}, color=sentiment_counts.index)

    return fig, summary, bar_chart, scatter_plot, heatmap, sentiment_bar_chart

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)