import tweepy
import snscrape.modules.twitter as sntwitter


class profileData:
    
    username = None
    screen_name  = None
    followers_count = None
    description = None
    location = None
    name = None
    user_id = None
    created_at = None
    verified = None
    profile_image_url = None
    tweets = []

    def __init__(self, username:str):
        self.screen_name = username

    def populate(self, num_tweets=1000, api=None):
        """use snscrape to get tweets in bulk, getting past api limit"""
        self.tweets = []
        if api:
            self.populate_with_api(api)

        for i,tweet in enumerate(sntwitter.TwitterSearchScraper('from:'+self.screen_name).get_items()):
            print(i)
            if i>num_tweets: break
            tweet_dict = {"date": tweet.date, "id": tweet.id, "content": tweet.content}
            self.tweets.append(tweet_dict)
    

    def populate_with_api(self, api:tweepy.API):

        """gets data from Twitter API using tweepy"""
        user = api.get_user(screen_name=self.screen_name)
        self.screen_name = user.screen_name
        self.name = user.name
        self.created_at = user.created_at
        self.description = user.description
        self.location = user.location
        self.profile_image_url = user.profile_image_url
        self.verified = user.verified
        return


        
    