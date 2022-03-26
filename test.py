from profileData import profileData
from config import consumer_key, consumer_secret, access_token, access_token_secret
import pickle
import tweepy



def main():
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret, access_token, access_token_secret)
    api = tweepy.API(auth)


    elonMuskData = profileData("elonmusk")
    elonMuskData.populate(api)
    filehandler = open("elonMuskData.pb", 'wb')
    pickle.dump(elonMuskData, filehandler)




if __name__ == "__main__":
    main()