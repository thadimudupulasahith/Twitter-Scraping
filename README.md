# Twitter-Scraping
Python scripting, Data Collection, MongoDB, Streamlit
import streamlit as st                           # Importing Streamlit library for building the app
import pandas as pd                              # Importing pandas library for working with data
from datetime import datetime, timedelta         # Importing datetime and timedelta modules for working with dates and times
from snscrape.modules import twitter             # Importing snscrape library for scraping Twitter data
import pymongo                                   # Importing pymongo library for working with MongoDB

# Set up MongoDB client and database
# Connect to the MongoDB Atlas cluster using the connection string
client = pymongo.MongoClient('mongodb+srv://thadimudupulasahith:sahith@cluster0.cy57gio.mongodb.net/?retryWrites=true&w=majority')
# Access the 'twitter_data' database
db = client['twitter_data']
# Access the 'tweets' collection
collection = db['tweets']

# Define function to scrape Twitter data
# This function takes a search query, start date, end date, and tweet count as inputs
# It uses the snscrape library to scrape tweets that match the search query and fall within the specified date range
# The function returns a pandas DataFrame containing the scraped tweets
def scrape_twitter_data(search_query, start_date, end_date, tweet_count):
    tweets = []
    for tweet in twitter.TwitterSearchScraper(f'{search_query} since:{start_date} until:{end_date}').get_items():
        if len(tweets) >= tweet_count:
            break
        tweets.append({
            'Date': tweet.date.strftime('%Y-%m-%d %H:%M:%S'),
            'ID': tweet.id,
            'URL': tweet.url,
            'Content': tweet.content,
            'User': tweet.user.username,
            'Reply Count': tweet.replyCount,
            'Retweet Count': tweet.retweetCount,
            'Language': tweet.lang,
            'Source': tweet.source,
            'Like Count': tweet.likeCount
        })
    return pd.DataFrame(tweets)

# Define function to upload data to MongoDB
# This function takes a pandas DataFrame and a search query as inputs
# It uploads the DataFrame to the MongoDB Atlas cluster in the 'twitter_data' database and 'tweets' collection
def upload_to_mongodb(data, search_query):
    collection.insert_one({
        'Scraped Word': search_query,
        'Scraped Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Scraped Data': data.to_dict('records')
    })

# Set up Streamlit app
# This line of code initializes a Streamlit app with the title 'Twitter Data Scraper'
st.title('Twitter Data Scraper')

# Get user input for search query, start date, end date, and tweet count
search_query = st.text_input('Enter a search query:')
start_date = st.date_input('Select a start date:')
end_date = st.date_input('Select an end date:')
tweet_count = st.number_input('Enter the maximum number of tweets to scrape:', min_value=1, max_value=1000, value=100)

# Convert date inputs to string format
# These lines of code convert the start date and end date inputs to string format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

data = pd.DataFrame()
