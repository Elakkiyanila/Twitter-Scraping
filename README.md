# Problem Statement:
Today, data is scattered everywhere in the world. Especially in social media, there may be a big quantity of data on Facebook, Instagram, Youtube, Twitter, etc. This consists of pictures and films on Youtube and Instagram as compared to Facebook and Twitter. To get the real facts on Twitter, you want to scrape the data from Twitter. You Need to Scrape the data like (date, id, url, tweet content, user,reply count, retweet count,language, source, like count etc) from twitter.
# Approach:
+ By using the “snscrape” Library, Scrape the twitter data from Twitter
+ Creating a dataframe with date, id, url, tweet content, user,reply count, retweet count,language, source, like count.
+ Storing each collection of data into a document into Mongodb along with the hashtag or key word we use to Scrape from twitter.
+ Creating a GUI using streamlit that should contain the feature to enter the keyword or Hashtag to be searched, select the date range and limit the tweet count need to be scraped. After scraping, the data needs to be displayed in the page and need a button to upload the data into Database and download the data into csv and json format.
# Twitter Scraping
Twitter scraping refers to the process of using automated tools or software to extract data from Twitter, such as tweets, user profiles, hashtags, and other relevant information. This data can then be used for various purposes, such as analyzing user sentiment, tracking brand mentions, or conducting research.
## Step 1
We need to import the necessary libraries/modules for the code to work.
+ snscrape is used to scrape data from Twitter
+ pandas is used for data manipulation
+ pymongo is used to connect to MongoDB
+ streamlit is used to build the web app.

If the libraries already there it is not necessary to install the libraries or other wise user have to install that library by using.
```
Pip install < library name >
```
```
import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
```
## Step 2
These lines connect to MongoDB to store the scraped data and create a database called 'twitter data'.
```
#Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_data']
```
## Step 3
This is a function that takes in the scraped Twitter data as a pandas dataframe and the keyword/hashtag used for scraping, and stores the data in a MongoDB collection with the same name as the keyword/hashtag.
```
def store_mongodb(tweets_df,hashtag_or_keyword):
    if not hashtag_or_keyword:
        st.error('Please enter a valid hashtag_or_keyword')
        return
    col = db[f'{hashtag_or_keyword}']
    data = tweets_df.to_dict('records')
    col.insert_many(data)
```
## Step 4
This is a function that takes in a keyword/hashtag, start and end dates, and a limit for the number of tweets to scrape according to your needs and it will return the pandas dataframe. 
```
def scrape_data(hashtag_or_keyword, start_date, end_date, tweet_limit):
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hashtag_or_keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= tweet_limit:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount,
                             tweet.retweetCount, tweet.lang, tweet.sourceLabel, tweet.likeCount])
    tweets_df = pd.DataFrame(tweets_list, columns=['date', 'id', 'url', 'content', 'user', 'reply_count',
                                                    'retweet_count', 'language', 'source', 'like_count'])
    return tweets_df
```
## Step 5
The app() function defines the Streamlit application. It first defines the input fields for the keyword or hashtag to search, the start and end dates, and the number of tweets to scrape. 
Then, if the user clicks the "Scrape Twitter Data" button, it calls the scrape_data() function to scrape the tweets and display them in a DataFrame using the st.write() function. 
If the user clicks the "Upload" button, it calls the store_mongodb() function to store the scraped data into MongoDB.
Finally, if the user clicks the "download" button, it allows them to download the scraped data as CSV or JSON files using the st.download_button() function.
```
def app():
    hashtag_or_keyword = st.text_input('Enter a keyword or hashtag to search:')
    start_date = st.date_input('Enter start date:')
    end_date = st.date_input('Enter end date:')
    tweet_limit = st.number_input('Enter number of tweets to scrape:',1 , 1000,1)
    # Scrape twitter data
    if st.button('Scrape Twitter Data'):
        tweets_df = scrape_data(hashtag_or_keyword, start_date, end_date, tweet_limit)
        # To show the scraped data
        st.write(tweets_df)
        st.success('scraped Successfully!!!')
        # Store the scraped data into MongoDB
        st.write('To store the scraped data into MongoDB click **upload**')
    if st.button("Upload"):
        tweets_df = scrape_data(hashtag_or_keyword, start_date, end_date, tweet_limit)
        store_mongodb(tweets_df,hashtag_or_keyword)
        st.success('Uploaded Successfully!!!',icon="✅")
        # Download data as CSV or JSON
        st.write("**:blue[click the below buttons to download the data]**")
    if st.button("download"):
        tweets_df = scrape_data(hashtag_or_keyword, start_date, end_date, tweet_limit)
        csv = tweets_df.to_csv().encode('utf-8')
        json = tweets_df.to_json(orient='records')
        st.download_button(
                label="Download data as CSV",
                data=csv,
                file_name=f'{hashtag_or_keyword}.csv',
                mime='text/csv',
            )
        st.download_button(
                label="Download data as JSON",
                data=json,
                file_name=f'{hashtag_or_keyword}.json',
                mime='application/json',
            )
 ```
Then if __name__ == '__main__': calls the app() function to run the Streamlit application.
# Workflow:
To watch the workflow of this project you can click this below link.

