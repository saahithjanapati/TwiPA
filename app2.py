from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tweepy

from sentiment_analysis import generate_graph
from config import consumer_key, consumer_secret, access_token, access_token_secret

import dash_bootstrap_components as dbc
import dash_html_components as html



import plotly.express as px
import plotly.graph_objects as go


app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

alert = dbc.Alert(
            [
                html.I(className="bi bi-info-circle-fill me-2"),
                "An example info alert with an icon",
            ],
            color="info",
            className="d-flex align-items-center",
        )

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

fig = go.Figure()

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls', 
                                  children = [
                                      html.H2('TwIPA - Sentiment Analysis'),
                                      html.P('''Visualising time series with Plotly - Dash'''),
                                      html.P('''Enter a Twitter Username of your choice.'''),
                                      html.Div(dcc.Input(id='my-input', value='elonmusk', type='text')),
                                      html.Div(id = "verified", 
                                          children = [
                                              html.H6('verified'),
                                              dbc.Container(alert)
                                          ], style = {'display': 'block'}),
                                      html.H6(id="full-name"),
                                      html.Img(src="https://pbs.twimg.com/profile_images/1503591435324563456/foUrqiEw_400x400.jpg", id="profile-pic"),
                                      
                                      ]
                                  ),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey', 
                                  children = [
                                      dcc.Graph(id='sentiment-graph')
                                  ])  # Define the right element
                                  ])
                                ])


@app.callback(
    Output('sentiment-graph', 'figure'),
    Output('full-name', component_property='children'),
    Output('profile-pic', component_property='src'),
    Output('verified', component_property='style'),
    Input(component_id='my-input', component_property='value'))
def update_output(value):
    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=100)

    fig = generate_graph(profileData.tweets)
    fig.update_layout(transition_duration=500)
    name = profileData.name
    profile_image_url = profileData.profile_image_url
    verifiedVar = profileData.verified
    if profileData.verified :
        return fig, name, profile_image_url, {'display': 'block'}


    return fig, name, profile_image_url, {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=True)