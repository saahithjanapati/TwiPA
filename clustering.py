from sklearn.decomposition import PCA
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from sklearn.preprocessing import normalize
import plotly.express as px



""""from https://towardsdatascience.com/k-means-clustering-8e1e64c1561c"""
def cluster(tweets):
    tfidfvectorizer = TfidfVectorizer(analyzer='word', stop_words='english')
    data = [tweet["content"] for tweet in tweets]
    tfidf = tfidfvectorizer.fit_transform(data)
    tf_idf_norm = normalize(tfidf)
    tf_idf_array = tf_idf_norm.toarray()

    sklearn_pca = PCA(n_components = 2)
    Y_sklearn = sklearn_pca.fit_transform(tf_idf_array)
    kmeans = KMeans(n_clusters=4, max_iter=600, algorithm = 'auto')
    fitted = kmeans.fit(Y_sklearn)
    predictions = kmeans.predict(Y_sklearn)
    fig = px.scatter(Y_sklearn[:, 0], Y_sklearn[:, 1], color=predictions, color_continuous_scale='viridis', template='plotly_dark')
    fig.update_traces(marker=dict(size=30))
    

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