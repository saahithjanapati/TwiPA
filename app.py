from dash import Dash, dcc, html, Input, Output, State
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tweepy
import json

from sentiment_analysis import *
from util import *
from config import consumer_key, consumer_secret, access_token, access_token_secret


app = Dash(__name__)

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

fig = go.Figure()

global time_to_tweet_dict

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls', 
                                  children = [
                                      html.H2('TwIPA - Sentiment Analysis'),
                                      html.P('''Visualising time series with Plotly - Dash'''),
                                      html.P('''Enter a Twitter Username of your choice.'''),
                                      html.Div(dcc.Input(id='my-input', value='elonmusk', type='text')),
                                        html.P('''Choose number of tweets you want to analyze'''),

                                      dcc.Slider(50, 1000, 50,value=50,id='my-slider'),
                                      html.Img(src="https://pbs.twimg.com/profile_images/1503591435324563456/foUrqiEw_400x400.jpg", id="profile-pic"),
                                      html.H6(id="full-name"),
                                      html.Div(id = "verified",
                                      children = [
                                          html.H6('verified'),
                                          html.I(className="bi bi-check-circle-fill")
                                      ], style = {'display': 'block'}),
                                      html.H6(id="positivity-score", children="Positivity-Score (1 is the most positive):"),
                                      html.H6(id="subjectivity-score", children="Subjectivity-Score (1 is the most subjective):"),
                                      html.Pre(id='hover-data')
                                      ]
                                  ),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey', 
                                  children = [
                                      dcc.Graph(id='sentiment-graph'), dcc.Graph(id='objectivity-graph')
                                  ])  # Define the right element
                                  ])
                                ])

@app.callback(
    Output('sentiment-graph', 'figure'),
    Output('objectivity-graph', 'figure'),
    Output('full-name', component_property='children'),
    Output('profile-pic', component_property='src'),
    Output('positivity-score', component_property='children'),
    Output('subjectivity-score', component_property='children'),
    Input(component_id='my-input', component_property='value'),
    Input(component_id='my-slider', component_property='value')
    )

def update_output(value, selected_number_tweets):
    global time_to_tweet_dict
    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=selected_number_tweets)
    
    time_to_tweet_dict = generate_time_to_tweet_dict(profileData.tweets)
    # print(time_to_tweet_dict)
    # graphs
    fig1 = generate_polarity_graph(profileData.tweets)
    fig1.update_layout(transition_duration=500)
    fig2 = generate_objectivity_graph(profileData.tweets)
    fig2.update_layout(transition_duration=500)

    #sentiment scores
    positivity_string = "Positivity-Score (1 is the most positive): " + (str(get_polarity_score(profileData.tweets))[0:5])
    objectivity_string = "Subjectivity-Score (1 is the most subjective): " + (str(get_objectivity_score(profileData.tweets))[0:5])

    name = profileData.name
    profile_image_url = profileData.profile_image_url
    return fig1, fig2, name, profile_image_url, positivity_string, objectivity_string


@app.callback(
    Output('hover-data', 'children'),
    Input('sentiment-graph', 'hoverData'),
    Input('objectivity-graph', 'hoverData'))
def display_hover_data(hoverData1, hoverData2):
    global time_to_tweet_dict 
    ctx = dash.callback_context
    if not ctx.triggered:
        return ""
    else:
        hoverData = None
        if 'sentiment-graph' in ctx.triggered[0]['prop_id']:
            hoverData = hoverData1
        elif 'objectivity-graph' in ctx.triggered[0]['prop_id']:
            hoverData = hoverData2
    hoverData = hoverData["points"][0]
    if hoverData["curveNumber"] == 0:
        time = hoverData["x"]
        return time_to_tweet_dict[time][0]

if __name__ == '__main__':
    app.run_server(debug=True)