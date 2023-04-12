# Twitter-Scraping
Python scripting, Data Collection, MongoDB, Streamlit
Purpose
The purpose of this Python script is to scrape Twitter data based on a user-specified search query, start date, end date, and maximum number of tweets to scrape. The scraped data is then uploaded to a MongoDB Atlas cluster and displayed in a table using the Streamlit library.

Dependencies
Python 3.x
pandas
datetime
snscrape
pymongo
Streamlit
Usage
Clone the repository and navigate to the project directory.
Install the necessary dependencies using pip: pip install -r requirements.txt
In the command line, run streamlit run app.py
In the Streamlit app, enter a search query, start date, end date, and maximum number of tweets to scrape.
Click the "Scrape Data" button to initiate the Twitter data scraping process.
The scraped data will be displayed in a table and uploaded to the MongoDB Atlas cluster.
Use the provided download buttons to download the scraped data in CSV or JSON format.
