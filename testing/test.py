from profileData import profileData
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pickle
from sentiment_analysis import generate_graph
import tweepy



def main():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)


    elonMuskData = profileData("lexfridman")
    elonMuskData.populate(api=api, num_tweets=100)

    # profileData = 

    # print(elonMuskData.tweets)
    # filehandler = open("elonMuskData.pb", 'wb')
    # pickle.dump(elonMuskData, filehandler)
    
    
    # elonMuskData = pickle.load(open("elonMuskData.pb", "rb"))
    generate_graph(elonMuskData.tweets)




if __name__ == "__main__":
    main()
