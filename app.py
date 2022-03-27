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
    html.H6(id="full-name"),
    html.Div(dcc.Input(id='my-input', value='elonmusk', type='text')),
    
    #profile pic
    html.Img(src="https://pbs.twimg.com/profile_images/1503591435324563456/foUrqiEw_400x400.jpg", id="profile-pic"),
    
    html.H6("Positivity vs Time Graph"),
    dcc.Graph(id='sentiment-graph')
])


@app.callback(
    Output('sentiment-graph', 'figure'),
    Output('full-name', component_property='children'),
    Output('profile-pic', component_property='src'),
    Input(component_id='my-input', component_property='value'))
def update_output(value):
    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=100)

    fig = generate_graph(profileData.tweets)
    fig.update_layout(transition_duration=500)
    name = profileData.name
    profile_image_url = profileData.profile_image_url
    return fig, name, profile_image_url


if __name__ == '__main__':
    app.run_server(debug=True)