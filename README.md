# Twitter Data Scraper

## Purpose
The purpose of this Python script is to scrape Twitter data based on a user-specified search query, start date, end date, and maximum number of tweets to scrape. The scraped data is then uploaded to a MongoDB Atlas cluster and displayed in a table using the Streamlit library.

## Dependencies
* Python 3.x
* pandas
* datetime
* snscrape
* pymongo
* Streamlit

## Usage
1. Clone the repository and navigate to the project directory.
2. Install the necessary dependencies using pip: `pip install -r requirements.txt`
3. In the command line, run `streamlit run app.py`.
4. In the Streamlit app, enter a search query, start date, end date, and maximum number of tweets to scrape.
5. Click the "Scrape Data" button to initiate the Twitter data scraping process.
6. The scraped data will be displayed in a table and uploaded to the MongoDB Atlas cluster.
7. Use the provided download buttons to download the scraped data in CSV or JSON format.

## Output
The output of the code is a pandas DataFrame containing the scraped Twitter data. The DataFrame includes columns for the date, tweet ID, URL, tweet content, user, reply count, retweet count, language, source, and like count. The scraped data is also uploaded to a MongoDB Atlas cluster in the 'twitter_data' database and 'tweets' collection.

## Limitations
This code assumes that the user has a MongoDB Atlas cluster set up and that they have the necessary packages installed. The code also has a limit of 1000 tweets to scrape per search query.

## Acknowledgements
This code was inspired by the following resources:

* snscrape documentation: https://github.com/JustAnotherArchivist/snscrape
* MongoDB Atlas documentation: https://docs.atlas.mongodb.com/
* Streamlit documentation: https://docs.streamlit.io/en/stable/
