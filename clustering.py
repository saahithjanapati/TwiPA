from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import plotly.express as px
import pandas as pd
# import plotly.graph_objects as go


# for hovering capability
def generate_score_to_tweet_dict(tweets, tfidfvectorizer, sklearn_pca):
    score_to_tweet_dict = {}
    for tweet in tweets:
        tfidf = tfidfvectorizer.fit_transform([tweet["content"]])
        tf_idf_norm = normalize(tfidf)
        tf_idf_array = tf_idf_norm.toarray()
        print(tf_idf_array)
        Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)
        print(Y_sklearn)
        score = kmeans.predict(Y_sklearn)
        score_to_tweet_dict[score[0]] = tweet["content"]
    return score_to_tweet_dict

""""from https://towardsdatascience.com/k-means-clustering-8e1e64c1561c"""
def cluster(tweets):
    df = pd.DataFrame.from_dict(tweets)
    print(df)
    tweet_texts = df["content"]
    print(tweet_texts)
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    data = [tweet["content"] for tweet in tweets]
    tfidf = tfidfvectorizer.fit_transform(tweet_texts)
    tf_idf_norm = normalize(tfidf)
    tf_idf_array = tf_idf_norm.toarray()

    sklearn_pca = PCA(n_components = 3)
    Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)
    print(Y_sklearn)
    df["X"] = [row[0] for row in Y_sklearn]
    df["Y"] = [row[1] for row in Y_sklearn]
    df["Z"] = [row[2] for row in Y_sklearn]
    print(df)

    kmeans = KMeans(n_clusters=4, max_iter=600, algorithm = 'auto')
    fitted = kmeans.fit(Y_sklearn)
    predictions = kmeans.predict(Y_sklearn)
    df["pred"] = predictions
    graph_data = df[["X", "Y", "Z"]]
    print(graph_data)
    print(px.data.iris())

    fig = px.scatter_3d(graph_data, x='X', y='Y', z='Z', title="PCA and K-Means Clustering", color=predictions, color_continuous_scale='viridis', template='plotly_dark')
    
    fig.update_traces(marker=dict(size=10))
    # fig = go.Figure(data=[go.Scatter3d(x=Y_sklearn[0], y=Y_sklearn[1], z=Y_sklearn[2],mode='markers'), color=predictions])
    

    # generate_score_to_tweet_dict(tweets, tfidfvectorizer, sklearn_pca)
    return fig


def get_top_features_cluster(tf_idf_array, prediction, n_feats):
    labels = np.unique(prediction)
    dfs = []
    for label in labels:
        id_temp = np.where(prediction==label) # indices for each cluster
        x_means = np.mean(tf_idf_array[id_temp], axis = 0) # returns average score across cluster
        sorted_means = np.argsort(x_means)[::-1][:n_feats] # indices with top 20 scores
        features = tf_idf_vectorizor.get_feature_names()
        best_features = [(features[i], x_means[i]) for i in sorted_means]
        df = pd.DataFrame(best_features, columns = ['features', 'score'])
        dfs.append(df)
    return dfs
# dfs = get_top_features_cluster(tf_idf_array, prediction, 15)