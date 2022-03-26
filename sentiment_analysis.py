from textblob import TextBlob
import re
import plotly.graph_objects as go
import plotly.express as px

def generate_graph(tweets, sliding_window_size=5):
    graph_data = {"date":[], "sentiment":[]}
    for tweet in tweets:
        graph_data["date"].append(tweet["date"])
        graph_data["sentiment"].append(get_sentiment(tweet["content"]))
    

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=graph_data["date"], y=graph_data["sentiment"], mode='markers', marker_color = graph_data["sentiment"], marker_colorscale=px.colors.sequential.Viridis, name="Sentiment"))

    # fig = px.scatter(x=graph_data["date"], y=graph_data["sentiment"], color=graph_data["sentiment"])
    smoothed_data = get_moving_average(graph_data["sentiment"], sliding_window_size)
    fig.add_trace(go.Scatter(x=graph_data["date"][sliding_window_size:], y=smoothed_data, mode='lines', marker_color="black", name="Running Average"))

    # fig.add_trace(x=graph_data["date"][sliding_window_size:], y=smoothed_data, mode='lines')
    fig.show()


def get_sentiment(tweet):
    cleaned_tweet = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    return TextBlob(cleaned_tweet).sentiment.polarity

def get_moving_average(data, window_size=10):
    i = window_size
    moving_averages = []
    while i < len(data):
        window = data[i-window_size:i]
        moving_averages.append(round(sum(window) / window_size, 2))
        i+=1
    return moving_averages

