from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import tweepy

from sentiment_analysis import *
from config import consumer_key, consumer_secret, access_token, access_token_secret
import dash_bootstrap_components as dbc

app = Dash(__name__, external_stylesheets=[dbc.icons.BOOTSTRAP])

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
                                        html.P('''Choose number of tweets you want to analyze'''),

                                      dcc.Slider(50, 1000, 50,value=50,id='my-slider'),
                                      html.Div(className = 'image-cropper', 
                                      children = [
                                          html.Img(src="https://pbs.twimg.com/profile_images/1503591435324563456/foUrqiEw_400x400.jpg", id="profile-pic", className = 'rounded')
                                      ]),

                                      html.Div(html.H6(className = 'parent', id="full-name")),
                                      html.Div(id = "verified", className = 'child',
                                      children = [
                                          html.I(className="bi bi-check-circle-fill")
                                          ], style = {'display': 'block'}),

                                      html.Br(),
                                      html.Br(),

                                      html.H6(id="num-followers"),
                                      html.H6(id="positivity-score", children="Positivity-Score (1 is the most positive):"),
                                      html.H6(id="subjectivity-score", children="Subjectivity-Score (1 is the most subjective):")

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
    Output('verified', component_property='style'),
    Output('num-followers', component_property='children'),

    Input(component_id='my-input', component_property='value'),
    Input(component_id='my-slider', component_property='value')
    )
def update_output(value, selected_number_tweets):
    from profileData import profileData
    profileData = profileData(value)
    profileData.populate(api=api, num_tweets=selected_number_tweets)

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

    num_followers = "Number of Followers: " + str(profileData.followers_count)

    if profileData.verified :
        return fig1, fig2, name, profile_image_url, positivity_string, objectivity_string, {'display': 'block'}, num_followers

    return fig1, fig2, name, profile_image_url, positivity_string, objectivity_string, {'display': 'none'}, num_followers


if __name__ == '__main__':
    app.run_server(debug=True)