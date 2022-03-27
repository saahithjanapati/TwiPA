from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tweepy

from sentiment_analysis import generate_graph
from config import consumer_key, consumer_secret, access_token, access_token_secret


app = Dash(__name__)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)



fig = go.Figure()

app.layout = html.Div([
    html.Div(dcc.Input(id='my-input', value='elonmusk', type='text')),
     dcc.Graph(id='sentiment-graph')
])


@app.callback(
    Output('sentiment-graph', 'figure'),
    Input(component_id='my-input', component_property='value'))
def update_output(value):
    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=100)
    fig = generate_graph(profileData.tweets)
    fig.update_layout(transition_duration=500)
    return fig


if __name__ == '__main__':
    app.run_server(debug=True)