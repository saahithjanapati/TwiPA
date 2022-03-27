def generate_time_to_tweet_dict(tweets):
    """"generate dictionary in new format to enable fast lookup for graph hovering"""
    new_dict = {}
    for tweet in tweets:
        new_dict[str(tweet["date"])[0:-6]] = [tweet["content"], tweet["id"], "https://twitter.com/twitter/status/" + str(tweet["id"])]
       
    return new_dict