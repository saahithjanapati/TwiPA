from matplotlib.pyplot import polar
from textblob import TextBlob
import re
import plotly.graph_objects as go
import plotly.express as px

def generate_polarity_graph(tweets, sliding_window_size=5):
    graph_data = {"date":[], "sentiment":[]}
    for tweet in tweets:
        graph_data["date"].append(tweet["date"])
        graph_data["sentiment"].append(get_polarity(tweet["content"]))
    
    fig = go.Figure()
    
    
    fig = px.scatter(x=graph_data["date"], y=graph_data["sentiment"], title="Positivity vs Time", color_continuous_scale='viridis', color = graph_data["sentiment"], template='plotly_dark')
    
    
    smoothed_data = get_moving_average(graph_data["sentiment"], sliding_window_size)
    fig.add_traces(list(px.line(x=graph_data["date"][sliding_window_size:], y=smoothed_data).select_traces()))

    fig.update_layout(title_x=0.5)
    return fig    


def generate_objectivity_graph(tweets, sliding_window_size=5):
    graph_data = {"date":[], "objectivity":[]}
    for tweet in tweets:
        graph_data["date"].append(tweet["date"])
        graph_data["objectivity"].append(get_objectivity(tweet["content"]))
    
    fig = go.Figure()

    fig = px.scatter(x=graph_data["date"], y=graph_data["objectivity"], title="Subjectivity vs Time", color_continuous_scale='viridis', color = graph_data["objectivity"], template='plotly_dark')
    smoothed_data = get_moving_average(graph_data["objectivity"], sliding_window_size)
    fig.add_traces(list(px.line(x=graph_data["date"][sliding_window_size:], y=smoothed_data).select_traces()))
    fig.update_layout(title_x=0.5)
    return fig

def get_polarity(tweet):
    cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    polarity_val = TextBlob(cleaned_tweet).sentiment.polarity
    return polarity_val

def get_objectivity(tweet):
    cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    objectivity_val = TextBlob(cleaned_tweet).sentiment.subjectivity
    return objectivity_val

def get_polarity_score(tweets):
    polarity_sum = 0
    for tweet in tweets:
        polarity_sum += get_polarity(tweet["content"])
    return polarity_sum/len(tweets)

def get_objectivity_score(tweets):
    objectivity_sum = 0
    for tweet in tweets:
        objectivity_sum += get_objectivity(tweet["content"])
    return objectivity_sum/len(tweets)

def get_moving_average(data, window_size=10):
    i = window_size
    moving_averages = []
    while i < len(data):
        window = data[i-window_size:i]
        moving_averages.append(round(sum(window) / window_size, 2))
        i+=1
    return moving_averages

