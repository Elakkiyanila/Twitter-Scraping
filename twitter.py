import snscrape.modules.twitter as sntwitter
import pandas as pd
import pymongo
import streamlit as st
st.title('**:blue[Welcome to Twitter Scraping]**')
st.write('''This website helps you to scrape the tweets using a keyword or hastag and you can change the date range and number of tweets according to your needs ,
          and you can download the files as csv or json format''')
# Connect to MongoDB
client = pymongo.MongoClient('mongodb://localhost:27017/')
db = client['twitter_data']
def store_mongodb(tweets_df,hashtag_or_keyword):
    if not hashtag_or_keyword:
        st.error('Please enter a valid hashtag_or_keyword')
        return
    col = db[f'{hashtag_or_keyword}']
    data = tweets_df.to_dict('records')
    col.insert_many(data)

# Function to scrape the twitter data
def scrape_data(hashtag_or_keyword, start_date, end_date, tweet_limit):
    tweets_list = []
    for i, tweet in enumerate(sntwitter.TwitterSearchScraper(f'{hashtag_or_keyword} since:{start_date} until:{end_date}').get_items()):
        if i >= tweet_limit:
            break
        tweets_list.append([tweet.date, tweet.id, tweet.url, tweet.content, tweet.user.username, tweet.replyCount,
                             tweet.retweetCount, tweet.lang, tweet.sourceLabel, tweet.likeCount])
    # Create dataframe from the scraped data
    tweets_df = pd.DataFrame(tweets_list, columns=['date', 'id', 'url', 'content', 'user', 'reply_count',
                                                    'retweet_count', 'language', 'source', 'like_count'])
    return tweets_df

# Streamlit app
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
        
if __name__ == '__main__':
    app()