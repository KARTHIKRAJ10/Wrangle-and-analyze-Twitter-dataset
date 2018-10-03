
# coding: utf-8

# # WRANGLE AND ANALYZE 

# # Gathering data for wrangling and analyzing the weratedogs
# * using Twitter archive
# * using programmatically
# * using Twitter API

# # Twitter Archive dataset
# twitter-archive-enhanced.csv is provided by udacity and it is downloaded manually.

# In[422]:


import pandas as pd
import numpy as np
df=pd.read_csv("F:/Data Analysis process/twitter-archive-enhanced.csv")
df.head()


# In[423]:


df.info()


# # Image prediction dataset
# Gathering using programmatically from udacity server

# In[424]:


import requests as rq
import os
folder='image_predictions'
if not os.path.exists(folder):
    os.makedirs(folder)
url='https://d17h27t6h515a5.cloudfront.net/topher/2017/August/599fd2ad_image-predictions/image-predictions.tsv'  
response=rq.get(url)
with open(os.path.join(folder,url.split('/')[-1]),mode='wb') as file:
    file.write(response.content)
os.listdir(folder)


# In[425]:


image=pd.read_table('image_predictions/image-predictions.tsv',sep='\t')
image.head()


# # Twitter Dataset
# Gathering using TWITTER API

# In[426]:


import tweepy
from tweepy import OAuthHandler
import json
import time
import re
import matplotlib.pyplot as plt
import warnings
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
OAUTH_TOKEN = ''
OAUTH_TOKEN_SECRET = ''




auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)





# In[427]:


tweet_data = {}
error_list = []
df_list =[]
for tweet_id in df['tweet_id']:
    try:
        tweet = api.get_status(tweet_id,tweet_mode='extended',
                                      wait_on_rate_limit=True,
                                      wait_on_rate_limit_notify=True)._json
        favorites = tweet['favorite_count'] 
        retweets = tweet['retweet_count'] 
        user_followers = tweet['user']['followers_count'] 
        user_favourites = tweet['user']['favourites_count'] 
        date_time = tweet['created_at']
        
        df_list.append({'tweet_id': int(tweet_id),
                        'favorites': int(favorites),
                        'retweets': int(retweets),
                        'user_followers': int(user_followers),
                        'user_favourites': int(user_favourites),
                        'date_time': pd.to_datetime(date_time)})
        
        
    except:
        print("Error for: " + str(tweet_id))
        error_list.append(tweet_id)


# In[428]:


print("The lengh of the errors", len(error_list))


# In[429]:


json_tweets = pd.DataFrame(df_list, columns = ['tweet_id', 'favorites', 'retweets',
                                               'user_followers', 'user_favourites', 'date_time'])
json_tweets.to_csv('tweet_json.txt', encoding = 'utf-8', index=False)


# In[430]:


tweet_data = pd.read_csv('tweet_json.txt', encoding = 'utf-8')


# In[431]:


tweet_data.info()


# In[432]:


tweet_data.head()


# # ACCESSING THE DATASET

# In[433]:


df.info()


# In[434]:


image.info()


# In[328]:


tweet_data.info()


# In[435]:


df.sample(20)


# In[436]:


image.sample(20)


# In[438]:


tweet_data.sample(20)


# In[439]:


df['rating_denominator'].value_counts()


# In[440]:


df['rating_numerator'].value_counts()


# # QUALITY ISSUES

# # Twitter Archive table
# * Timestamp data type should be converted to datatime.
# * Removing the retweets from the dataset.
# * Removing the incorrected words of name such as a,an,the,etc..
# * Rating denominator and rating numerator have incorrect words.
# * To replace the incorrect dog stage.

# # Image table
# * Tweet_id data type should be converted to string.
# * p1,p2,p3 column is not consistent.
# * Remove _ in p1 p2 p3 columns in between the columns to make consistent.

# # Tweet data
# * Tweet_id datatype conversion from int to string.

# # TIDINESS ISSUE

# * Combine dog stage into single column and remove the separate columns.
# * Convert data_time into separate column like data and time.
# * oin all three dataset.
# * Most dog stage are so it should be removed.
# * Many unwanted column should be removed.
# * To drop the separate dog stages.

# # CLEANING

# In[496]:


# To make the copy of all dataframe
df_copy=df.copy()
image_copy=image.copy()
tweet_data_copy=tweet_data.copy()


# # Define 
# Remove all retweets and to get original tweets

# from the df.info() method it is known that there are 181 retweets in the dataset.

# # code

# In[497]:


df_copy.drop(df_copy[df_copy['retweeted_status_id'].notnull()].index,inplace=True)


# # Test

# In[498]:


df_copy.info()


# # Define
# Timestamp datetype should be converted to datetime type in twitter archive dataset

# # Code

# In[499]:


df_copy['timestamp']=pd.to_datetime(df_copy['timestamp'])


# # test

# In[500]:


df_copy.info()


# # Define
# date_time datatype should be converted to datetime in twitter data

# # Code

# In[503]:


tweet_data_copy['date_time']=pd.to_datetime(tweet_data_copy['date_time'])


# # Test

# In[504]:


tweet_data_copy.info()


# # Define 
# Remove '_' in p1 p2 p3 columns in between the columns to make consistent

# # Code

# In[505]:


image_copy['p1']=image_copy['p1'].str.replace('_',' ')
image_copy['p2']=image_copy['p1'].str.replace('_',' ')
image_copy['p3']=image_copy['p1'].str.replace('_',' ')


# # Test

# In[506]:


image_copy.sample(5)


# # Define 
# To make p1 p2 p3 columns as title

# # Code

# In[507]:


image_copy['p1']=image_copy['p1'].str.title()
image_copy['p2']=image_copy['p2'].str.title()
image_copy['p3']=image_copy['p3'].str.title()


# # Test

# In[508]:


image_copy.sample(5)


# # Define
# tweet_id datatype conversion int from str

# # code

# In[510]:


image_copy.tweet_id=image_copy.tweet_id.astype(str)
df_copy.tweet_id=df_copy.tweet_id.astype(str)
tweet_data_copy.tweet_id=tweet_data_copy.tweet_id.astype(str)


# # Test

# In[511]:


image_copy.info()


# In[512]:


df_copy.info()


# In[513]:


tweet_data_copy.info()


# # Define
# combine dog stage into a single column 

# # code

# In[514]:


df_copy['stage'] = df[['doggo', 'floofer','pupper','puppo']].apply(lambda x: ''.join(x), axis=1)

df_copy['stage'].replace("NoneNoneNoneNone","None ", inplace=True)
df_copy['stage'].replace("doggoNoneNoneNone","doggo", inplace=True)
df_copy['stage'].replace("NoneflooferNoneNone","floofer", inplace=True)
df_copy['stage'].replace("NoneNonepupperNone","pupper", inplace=True)
df_copy['stage'].replace("NoneNoneNonepuppo","puppo", inplace=True)


# # Test

# In[515]:


df_copy.sample(2)


# # Define 
# To drop the seperate dog stage column

# # Code

# In[516]:


df_copy=df_copy.drop(columns=['doggo', 'floofer','pupper','puppo'])


# # Test

# In[517]:


df_copy.info()


# # Define
# Replace the incorrect dog stage

# # Code

# In[518]:


df_copy['stage']=df_copy['stage'].replace('doggoNonepupperNone','pupper')
df_copy['stage']=df_copy['stage'].replace('doggoNoneNonepuppo','puppo')
df_copy['stage']=df_copy['stage'].replace('doggoflooferNoneNone','floofer')


# # Test

# In[ ]:


df_copy['stage'].value_counts()


# # Define
# Seperate datetime to data and time
# remove timestamp column

# # code

# In[519]:


df_copy['date'] = df_copy['timestamp'].apply(lambda time: time.strftime('%m-%d-%Y'))
df_copy['time'] = df_copy['timestamp'].apply(lambda time: time.strftime('%H:%M'))
df_copy=df_copy.drop(columns=['timestamp'])


# # test

# In[520]:


df_copy.sample(3)


# In[521]:


df_copy.info()


# # Define
# changing datatype of the data from object to datetime

# # code

# In[522]:


df_copy['date']=pd.to_datetime(df_copy['date'])


# # Test

# In[523]:


df_copy.info()


# # Define
# Rating in the numerator are incorrect

# # Code

# In[525]:


df_copy['rating_numerator']=df_copy['rating_numerator'].replace(420,42)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(165,16)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(144,14)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(182,18)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(143,14)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(660,66)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(960,96)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(1776,17)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(121,12)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(204,20)
df_copy['rating_numerator']=df_copy['rating_numerator'].replace(666,66)


# # Test

# In[526]:


df_copy['rating_numerator'].value_counts()


# # Define 
# To merge all the 3 dataset to single dataset called "twitter_dataset"

# # Code

# In[527]:


twitter_dataset=pd.merge(tweet_data_copy,image_copy,on='tweet_id',how='inner')
twitter_dataset=pd.merge(twitter_dataset,df_copy,on='tweet_id',how='inner')


# # Test

# In[528]:


twitter_dataset.info()


# # Define 
# To remove the unwanted column in twitter_dataset

# # code

# In[529]:


twitter_dataset=twitter_dataset.drop(columns=['date_time','img_num','user_followers','user_favourites','in_reply_to_status_id','in_reply_to_user_id','source','retweeted_status_id','retweeted_status_user_id','retweeted_status_timestamp','expanded_urls'])


# # Test

# In[530]:


twitter_dataset.info()


# In[531]:


twitter_dataset


# # Define
# Replacing the incorrect dog names using Dog

# # Code

# In[532]:


twitter_dataset['name']=twitter_dataset['name'].replace('a','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('an','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('the','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('this','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('such','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('quite','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('None','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('one','Dog')
twitter_dataset['name']=twitter_dataset['name'].replace('unacceptable','Dog')


# # Test

# In[533]:


twitter_dataset['name'].sample(50)


# # Define
# Most of the dog stage are none so it should be removed.

# # Code

# In[575]:


twitter_dataset=twitter_dataset.drop(columns=['stage'])


# # Test

# In[576]:


twitter_dataset.info()


# # Storing the Dataset

# In[577]:


twitter_dataset.to_csv('Twitter_archive_master.csv')
image_copy.to_csv('Image_master.csv')
tweet_data_copy.to_csv('Twitter_api.csv')
df_copy.to_csv('Twitter_archive.csv')


# # Analyzing the Dataset

# In[578]:


analyze_set=pd.read_csv('Twitter_archive_master.csv')


# In[579]:


analyze_set.info()


# In[580]:


analyze_set.sample(5)


# In[582]:


analyze_set.describe()


# # Most Favorite Dog

# In[583]:


analyze_set.loc[analyze_set['favorites']==162332]


# In[592]:


analyze_set[analyze_set['tweet_id']==744234799360020481].jpg_url


# # Least Favorite Dog

# In[584]:


analyze_set.loc[analyze_set['favorites']==80]


# In[591]:


analyze_set[analyze_set['tweet_id']==666102155909144576].jpg_url


# In[585]:


from collections import Counter

x = analyze_set['name']

count = Counter(x)
count.most_common(5)


# Oliver ,Cooper ,Charlie, Lucy are dogs with common name.

# Pupper is the most common age of dog.

# In[599]:


y = analyze_set['date']

count = Counter(y)
count.most_common(1)


# 29 November 2015 is the date where the many dogs are posted in twitter.

# In[605]:


analyze_set['date']=pd.to_datetime(analyze_set['date'])
analyze_set['year']=analyze_set['date'].dt.year
analyze_set['year'].value_counts()


# In[606]:


analyze_set['date']=pd.to_datetime(analyze_set['date'])
analyze_set['month']=analyze_set['date'].dt.month
analyze_set['month'].value_counts()


# In[607]:


analyze_set['rating_numerator'].value_counts()


# In[593]:


analyze_set.plot(kind='scatter',x='favorites',y='retweets', alpha = 0.4)
plt.xlabel('Favorites')
plt.ylabel('Retweets')
plt.title('Retweets and Favorites')
plt.savefig('a.png')


# In[608]:


analyze_set['retweets'].corr(analyze_set['favorites'])


# The correlation between the favorites and retweets is 0.9275
