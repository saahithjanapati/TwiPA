from dash import Dash, dcc, html, Input, Output, State
import dash
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tweepy
import dash_bootstrap_components as dbc

from sentiment_analysis import *
from util import *
from clustering import *
from config import consumer_key, consumer_secret, access_token, access_token_secret


app = Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP])
server = app.server

auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
api = tweepy.API(auth)

fig = go.Figure()

global time_to_tweet_dict
global pca_to_tweet_dict

app.layout = html.Div(children=[
                      html.Div(className='row',  # Define the row element
                               children=[
                                  html.Div(className='four columns div-user-controls', 
                                  children = [

                                      html.H1('TwiPA'),

                                      html.P('''Enter a Twitter Username of your choice.'''),

                                      html.Div(className='containerTwo', children = [
                                          html.Div(className = 'textField', children=[dcc.Input(id='my-input', value='elonmusk', type='text')]),
                                          dcc.Loading(id="loading-1", type="default",children=html.Div(id="loading-output-1"))
                                      ]),

                                      html.Br(),

                                      html.P('''Choose number of tweets you want to analyze'''),

                                      dcc.Slider(50, 1000, 100,value=250,id='my-slider'),

                                      html.Br(),
                                      html.Br(),

                                      

                                      html.Div(className = 'image-cropper', 
                                      children = [
                                          html.Img(src="https://pbs.twimg.com/profile_images/1503591435324563456/foUrqiEw_400x400.jpg", id="profile-pic", className = 'rounded')
                                      ]),

                                      html.Div(className = 'container', children = [
                                          html.H6(className = 'parent', id="full-name"),
                                          html.Div(id = "verified", className = 'child',
                                            children = [
                                                html.I(className="bi bi-check-circle-fill")
                                                ], style = {'display': 'block'})

                                      ]),

                                      html.Br(),
                                      html.Br(),

                                      html.H6(id="num-followers"),
                                      html.H6(id="positivity-score", children="Positivity-Score (1 is the most positive):"),
                                      html.H6(id="subjectivity-score", children="Subjectivity-Score (1 is the most subjective):"),

                                      html.Br(),

                                      html.H6(id='hover-data'),

                                      html.A(id='hover-data-link'),
                                      ]
                                  ),  # Define the left element
                                  html.Div(className='eight columns div-for-charts bg-grey', 
                                  children = [
                                    #   dcc.Graph(id='sentiment-graph'), dcc.Graph(id='objectivity-graph'), dcc.Graph(id='cluster-graph')
                                        dcc.Graph(id='sentiment-graph'), dcc.Graph(id='objectivity-graph'), dcc.Graph(id='cluster-graph')

                                      ]) 
                                  ])
                                ])

@app.callback(
    Output('loading-output-1', "children"),
    Output('sentiment-graph', 'figure'),
    Output('objectivity-graph', 'figure'),
    Output('cluster-graph', 'figure'),
    Output('full-name', component_property='children'),
    Output('profile-pic', component_property='src'),
    Output('positivity-score', component_property='children'),
    Output('subjectivity-score', component_property='children'),
    Output('verified', component_property='style'),
    Output('num-followers', component_property='children'),

    Input(component_id='my-input', component_property='value'),
    Input(component_id='my-slider', component_property='value')
    )
def update_output(value, selected_number_tweets):
    # dictionaries used to get tweets for hovering
    global time_to_tweet_dict
    global pca_to_tweet_dict

    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=selected_number_tweets)
    
    time_to_tweet_dict = generate_time_to_tweet_dict(profileData.tweets)

    fig1 = generate_polarity_graph(profileData.tweets)
    fig1.update_layout(transition_duration=500)
    fig2 = generate_objectivity_graph(profileData.tweets)
    fig2.update_layout(transition_duration=500)
    fig3, pca_to_tweet_dict = cluster(profileData.tweets)
    fig3.update_layout(transition_duration=500)

    #sentiment scores
    positivity_string = "Positivity-Score (1 is the most positive): " + (str(get_polarity_score(profileData.tweets))[0:5])
    objectivity_string = "Subjectivity-Score (1 is the most subjective): " + (str(get_objectivity_score(profileData.tweets))[0:5])

    name = profileData.name
    profile_image_url = profileData.profile_image_url

    num_followers = "Number of Followers: " + str(profileData.followers_count)

    if profileData.verified :
        return True, fig1, fig2, fig3, name, profile_image_url, positivity_string, objectivity_string, {'display': 'block'}, num_followers

    return True, fig1.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}), fig2.update_layout({'plot_bgcolor': 'rgba(0, 0, 0, 0)', 'paper_bgcolor': 'rgba(0, 0, 0, 0)'}), fig3, name, profile_image_url, positivity_string, objectivity_string, {'display': 'none'}, num_followers



@app.callback(
    Output('hover-data', 'children'),
    Output('hover-data-link', 'children'),
    Input('sentiment-graph', 'hoverData'),
    Input('objectivity-graph', 'hoverData'),
    Input('cluster-graph', 'hoverData')
    )
def display_hover_data(hoverData1, hoverData2, hoverData3):
    global time_to_tweet_dict 
    global pca_to_tweet_dict
    ctx = dash.callback_context
    if not ctx.triggered:
        return "", ""
    else:
        hoverData = None
        if 'sentiment-graph' in ctx.triggered[0]['prop_id']:
            hoverData = hoverData1
            hoverData = hoverData["points"][0]
            if hoverData["curveNumber"] == 0:
                time = hoverData["x"]
                return "Tweet: " + str(time_to_tweet_dict[time][0]), time_to_tweet_dict[time][2]
        
        elif 'objectivity-graph' in ctx.triggered[0]['prop_id']:
            hoverData = hoverData2
            hoverData = hoverData["points"][0]
            if hoverData["curveNumber"] == 0:
                time = hoverData["x"]
                return "Tweet: " + str(time_to_tweet_dict[time][0]), time_to_tweet_dict[time][2]
       
        elif 'cluster-graph' in ctx.triggered[0]['prop_id']:
            hoverData = hoverData3
            hoverData = hoverData["points"][0]
            print(hoverData)
            # print(pca_to_tweet_dict)
            print(len(pca_to_tweet_dict))
            return "Tweet: " + str(pca_to_tweet_dict[hoverData["x"]][0]), pca_to_tweet_dict[hoverData["x"]][1]


if __name__ == '__main__':
    app.run_server(debug=False)