# TwiPA
## Twitter Profile Analyzer


TwiPa is a tool that analyzes Twitter profiles. It performs sentiment analysis and clustering of tweets of a specific user and creates interactive graphs with this data.

- Link to Website: https://twipahoohacks.herokuapp.com
- Link to HooHacks DevPost: https://devpost.com/software/twipa
- Link to Video Demo: https://www.youtube.com/watch?v=r8qPUJBqLbk


![Screenshot](https://github.com/saahithjanapati/TwiPA/blob/main/screenshot.png)

## How to Run
Make sure you're running Python 3.8 or higher. Then:
```
pip install -r requirements.txt
```
Create file named config.py and fill it with the following fields for access to the [Twitter API](https://developer.twitter.com/en/docs/twitter-api/getting-started/getting-access-to-the-twitter-api):
```
consumer_key = ""
consumer_secret = ""

access_token = ""
access_token_secret = ""
```
Then start the app with:
```
python app.py
```


Created by Siddharth Lakkoju and Saahith Janapati
