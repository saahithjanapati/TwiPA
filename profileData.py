import tweepy 

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
    # data = None
    tweets = []

    def __init__(self, username:str):
        self.name = username
    
    def populate(self, api:tweepy.API):
        """gets data from Twitter API"""
        user = api.get_user(screen_name=self.name)
        self.screen_name = user.screen_name
        self.name = user.name
        self.created_at = user.created_at
        self.description = user.description
        self.location = user.location
        self.profile_image_url = user.profile_image_url
        self.verified = user.verified
        # self.data = user.data
        self.tweets = api.user_timeline(screen_name=self.username, count=2000, include_rts=True, tweet_mode='extended')
        return
    

        
    