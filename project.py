import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from snscrape.modules import twitter
import pymongo

# Set up MongoDB client and database
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_data']
collection = db['tweets']

# Define function to scrape Twitter data
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
def upload_to_mongodb(data, search_query):
    collection.insert_one({
        'Scraped Word': search_query,
        'Scraped Date': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        'Scraped Data': data.to_dict('records')
    })

# Set up Streamlit app
st.title('Twitter Data Scraper')

# Get user input for search query, start date, end date, and tweet count
search_query = st.text_input('Enter a search query:')
start_date = st.date_input('Select a start date:')
end_date = st.date_input('Select an end date:')
tweet_count = st.number_input('Enter the maximum number of tweets to scrape:', min_value=1, max_value=1000, value=100)

# Convert date inputs to string format
start_date_str = start_date.strftime('%Y-%m-%d')
end_date_str = end_date.strftime('%Y-%m-%d')

data = pd.DataFrame()

# Scrape Twitter data and display in table
if st.button('Scrape Data'):
    st.write(f'Scraping Twitter data for "{search_query}" from {start_date_str} to {end_date_str}...')
    data = scrape_twitter_data(search_query, start_date_str, end_date_str, tweet_count)
    st.write(f'{len(data)} tweets scraped:')
    st.dataframe(data)
    # Upload data to MongoDB
    upload_to_mongodb(data, search_query)
    st.write('Data uploaded to MongoDB.')

    # Add buttons to download data in CSV and JSON formats
    try:
        csv = data.to_csv(index=False)
        st.download_button('Download CSV', data=csv, file_name='twitter_data.csv', mime='text/csv')
    except Exception as e:
        st.write('Error downloading CSV file:', e)

    try:
        json = data.to_json(orient='records')
        st.download_button('Download JSON', data=json, file_name='twitter_data.json', mime='application/json')
    except Exception as e:
        st.write('Error downloading JSON file:', e)
