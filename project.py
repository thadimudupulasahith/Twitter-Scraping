import streamlit as st
import pandas as pd
from datetime import datetime, timedelta
from snscrape.modules import twitter
import pymongo

# Set up MongoDB client and database
# Connect to the MongoDB Atlas cluster using the connection string
uri = "mongodb+srv://thadimudupulasahith:sahith@cluster0.cy57gio.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(uri)
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
# data.to_dict()is a method call that converts a pandas DataFrame object called data into a list of dictionaries,
#where each dictionary corresponds to a row in the DataFrame.
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
#The next line of code initializes an empty pandas DataFrame to hold the scraped data.
data = pd.DataFrame()

# Scrape Twitter data and display in table
# This line of code creates a button that, when clicked, initiates the Twitter data scraping process
if st.button('Scrape Data'):
    # Display message that the data is being scraped
    st.write(f'Scraping Twitter data for "{search_query}" from {start_date_str} to {end_date_str}...')
    # Scrape the data using the given parameters
    #The next line of code calls the scrape_twitter_data function, passing in the search query, start date, end date,
    #and tweet count as arguments.
    #The returned DataFrame is stored in the data variable.
    data = scrape_twitter_data(search_query, start_date_str, end_date_str, tweet_count)
    # Display the number of tweets that were scraped
    st.write(f'{len(data)} tweets scraped:')
    # Display the scraped data in a table
    st.dataframe(data)
# Upload data to MongoDB
# Add button to upload data to MongoDB
if st.button('Upload to MongoDB'):
    upload_to_mongodb(data, search_query)
    #st.write('Data uploaded to MongoDB.')
    #upload_to_mongodb(data, search_query)
    # Display message that the data has been uploaded
    st.write('Data uploaded to MongoDB.')

    # Add buttons to download data in CSV and JSON formats
    try:
         # Convert the data to CSV format and create a download button for it
        csv = data.to_csv(index=False)
        st.download_button('Download CSV', data=csv, file_name='twitter_data.csv', mime='text/csv')
        # Display an error message if the CSV download button cannot be created
    except Exception as e:
        st.write('Error downloading CSV file:', e)

    try:
         # Convert the data to JSON format and create a download button for it
        json = data.to_json(orient='records')
        st.download_button('Download JSON', data=json, file_name='twitter_data.json', mime='application/json')
         # Display an error message if the JSON download button cannot be created
    except Exception as e:
        st.write('Error downloading JSON file:', e)
