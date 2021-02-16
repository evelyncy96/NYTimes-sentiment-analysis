#!/usr/bin/env python
# coding: utf-8

# In[1]:


# part0: Download libraries and packages
from bs4 import BeautifulSoup
import selenium
from selenium import webdriver
import numpy as np
import nltk
nltk.download('vader_lexicon')
from nltk.tokenize import RegexpTokenizer
from nltk.sentiment.vader import SentimentIntensityAnalyzer as SIA
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS 
import requests
import pandas as pd
from datetime import datetime
import re
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
import seaborn as sns
get_ipython().run_line_magic('config', "InlineBackend. figure_format = 'retina' #improve the quality of image")
import time
import csv


# In[2]:


# part1: Create chromedriver
# For more Info refers to NYTimes archive, please visit:https://help.nytimes.com/hc/en-us/articles/115014772767-Archives 
#User chromedriver path!
startDate = input("Please input the start-date (Ex:20201020):") #input the start date of articles you want to collect 
endDate = input("Please input the end-date (Ex:20201102):") #input the end date of articles you want to collect 
driver = webdriver.Chrome('/Users/evelyn.cy/Python329/SideProject/chromedriver') 
driver.get(f'https://www.nytimes.com/search?dropmab=true&endDate={endDate}&query=&sort=best&startDate={startDate}')
time.sleep(2)


# In[3]:


# part2: Choose specific section & type

def click_button(xpath):
    item = driver.find_element_by_xpath(xpath).click()
    time.sleep(0.5)
    
click_button("//*[@id=\"site-content\"]/div/div[1]/div[2]/div/div/div[2]/div/div/button/label/span[2]")
click_button("//*[@id=\"site-content\"]/div/div[1]/div[2]/div/div/div[2]/div/div/div/ul/li[1]/button")
click_button("//*[@id=\"site-content\"]/div/div[1]/div[2]/div/div/div[3]/div/div/button")
click_Num = int(int(driver.find_element_by_class_name("css-1280esi").text)/10)
click_button("//*[@id=\"site-content\"]/div/div[1]/div[2]/div/div/div[3]/div/div/div/ul/li[1]/button")


# In[6]:


# part3: Click show-more button to automacially extend the full info

for i in range(click_Num):
    click_button("//*[@id=\"site-content\"]/div/div[2]/div[2]/div/button")
    time.sleep(2)


# In[7]:


# part4: Collect the articles' website link

soup = BeautifulSoup(driver.page_source, 'html.parser')
articlelink = []
for i in soup.find_all(class_ = 'css-1l4w6pd'):
    link = "https://www.nytimes.com/"+ str(i.find(class_ = 'css-e1lvw9').a['href'])
    articlelink.append(link)
    


# In[14]:


# part5: Collect the full content, title, publish time of all articles and lower the content text
article = []
title = []
publish_time = []
for url in articlelink:
    res = requests.get(url) 
    soup = BeautifulSoup(res.text,'html.parser') 
    title.append(soup.find('h1').text.lower())
    publish_time.append(str(soup.head.meta['content']).split("T")[0])
    time.sleep(1)
    articleContent = [j.text for i in soup.find_all(class_ = 'css-1fanzo5 StoryBodyCompanionColumn') for j in i.find_all(class_ = 'css-axufdj evys1bk0')]
    
    bigstring = ''        
    for i in articleContent:
        bigstring += i
    article.append(bigstring)
    
article = [i.lower() for i in article]


# In[15]:


# part6: Tokenize each article content

tokenizer = RegexpTokenizer(r'[a-zA-Z]+')
tok_article = [tokenizer.tokenize(i) for i in article]


# In[16]:


# part7:Import emotional wordbags using Loughran and McDonald positive and negative dictionaries
# To know more about LM emotional dictionaries,please visit: https://sraf.nd.edu/textual-analysis/resources/
posWord = []
negWord = []
with open("LM_positive.csv","r",encoding = "utf-8-sig") as fIn:
    csvIn = csv.reader(fIn)
    for row in csvIn:
        posWord.append(row[0])
        
with open("LM_negative.csv","r",encoding = "utf-8-sig") as fIn:
    csvIn = csv.reader(fIn)
    for row in csvIn:
        negWord.append(row[0])
        
posWord = [word.lower() for word in posWord]
negWord = [word.lower() for word in negWord]


# In[17]:


# part8: Cleanup the useless article token if the token is in stopwords
i = 1
for content in tok_article:
    for text in content:
        if text in stopwords.words('english') or len(text) == 1:
            content.remove(text)
    i += 1
    
article_length = [len(tok_article[i]) for i in range(len(tok_article))] #


# In[18]:


# part9: Calculate the amount of times "trump" and "biden" appear in articles to find the volume
trump_freq = []
biden_freq = []
category = [] 
"""
If the amount of time "Trump" mentioned in an article surpass that of "Biden", the article will be marked
as "Trump" amd stored in category list. If the amount of time two candidates mentioned in an article is the
same then the article will be marked as "Both"
"""
for i in range(len(tok_article)):
    j = 0
    k = 0
    for word in tok_article[i]:
        if word == "trump":
            j += 1
        elif word == "biden":
            k += 1
    trump_freq.append(j)
    biden_freq.append(k)
    
    if j > k:
        category.append("trump")
    elif j == k:
        category.append("both")
    else:
        category.append("biden")


# In[19]:


# part10-1: Sentiment analysis using neg & pos wordbag from LM emotional dictionary, range [-1, 1]

"""
sent_article collect sentiment density for each candidates, and the formula is presented below:
(# of positive token - # of negative token) / (# of positive token - # of negative token)
"""

sent_article = []
for i in range(len(tok_article)):
    pos_token = [content for content in tok_article[i] if content in posWord]
    neg_token = [content for content in tok_article[i] if content in negWord]
    try:
        sent_article.append(round((len(pos_token)-len(neg_token))/(len(pos_token)+len(neg_token)),2))
    except ZeroDivisionError:
        sent_article.append(0)
        


# In[140]:


# part10-2: Sentiment analysis using Nltk SentimentIntensityAnalyzer

sia = SIA()
sia_sentiment = [sia.polarity_scores(content) for content in article]
sia_compound = [i['compound'] for i in sia_sentiment]
sia_pos = [i['pos'] for i in sia_sentiment]
sia_neg = [i['neg'] for i in sia_sentiment]
sia_neu = [i['neu'] for i in sia_sentiment]


# In[141]:


#part 11: Create dataframe
df = pd.DataFrame({
    "Title":title,
    "Date":publish_time,
    "#article token":article_length,  #effective article tokens filtered by stopwords
    "trump frequency":trump_freq,     #the amount of time "Trump" mentioned in each article 
    "biden frequency":biden_freq,     #the amount of time "Biden" mentioned in each article
    "sentiment_density":sent_article, #sentiment analysis score using LM emotional dictionaries
    "positive":sia_pos,   #Nltk positive scores
    "negative":sia_neg,   #Nltk negative scores
    "neutral":sia_neu,    #Nltk neutral scores
    "compound":sia_compound,   #Nltk compound scores
    "Topic":category                  #article mark
})
pd.set_option('max_colwidth',100) #modify dataframe width 


# In[196]:


# Image 1 : plot

date = list(sorted(set(publish_time)))
shortdate = [f'{i.split("-")[1]}/{i.split("-")[2]}' for i in date]

def volume(candidate):  #pull out dataset from DataFrame column
    return(df.loc[df['Topic'] == candidate,['Date','Topic']].groupby('Date').count().iloc[:, 0].tolist())

def show_data_on_img(x_data,y_data,position): #show numbers on the plot
    for x,y in zip(x_data,y_data):
        plt.text(x,y+position,y,ha='center', va='bottom', fontsize=10)

plt.plot(shortdate,volume('trump'),'o-',color='red',label='Trump',markersize=5) # add data for "Trump" bar
plt.plot(shortdate,volume('biden'),'o-',color='blue',label='Biden',markersize=5) # add data for "Biden" bar
plt.plot(shortdate,volume('both'),'o-',color='green',label='Both',markersize=5) 

plt.title("The Number Of Article Stressed On Different Candidates (Year:2020)",fontsize = 15,y=1.05)
plt.rcParams["figure.figsize"] = (12, 9) 
plt.xticks(rotation = 45,fontsize=10) 
plt.xlabel("Two weeks before election day",fontsize = 15,labelpad = 15) 
plt.ylabel("Article Number",fontsize = 15,labelpad = 15) 
plt.legend(bbox_to_anchor=(1.05, 1)) 

show_data_on_img(shortdate,volume('trump'),0.5)
show_data_on_img(shortdate,volume('biden'),0.5)
show_data_on_img(shortdate,volume('both'),0.5)


# In[195]:


# image 2 : plot

def frequency(candidate):
    df1 = df[["Date","trump frequency","biden frequency"]].groupby("Date").sum()
    return(df1[f'{candidate} frequency'].tolist())

plt.plot(shortdate,frequency('trump'),'o-',color='red',label='Trump',markersize=5) 
plt.plot(shortdate,frequency('biden'),'o-',color='blue',label='Biden',markersize=5) 

plt.title("The Frequency Both Candidates Mentioned In Articles (Year:2020)",fontsize = 15,y=1.05)
plt.xlabel("Two weeks before election day",fontsize = 15,labelpad = 15) 
plt.ylabel("Frequency",fontsize = 15,labelpad = 15) 
plt.xticks(rotation = 45,fontsize=11) 
plt.rcParams["figure.figsize"] = (8, 6) 
plt.legend(prop = {'size':18}) 

show_data_on_img(shortdate,frequency('trump'),3)
show_data_on_img(shortdate,frequency('biden'),3)


# In[194]:


# image 3 : Heatmap 

shortdate = [f'{i.split("-")[1]}/{i.split("-")[2]}' for i in date]

"""
Negative Sentiment Density is calculated on daily-basis, and the formula presented below: 
sum(daily sentiment density of candidate) / count(daily number of articles marked with candidate)
"""

def day_sentiment(candidate,column):
    df1 = df.loc[df['Topic'] == candidate,['Date',column]].groupby('Date')
    day_sent = df1.sum().iloc[:, 0].tolist()
    day_count = df1.count().iloc[:, 0].tolist()
    avg_day_sent = [round(day_sent[i]/day_count[i],2) for i in range(len(day_sent))]
    return(avg_day_sent)


plt.figure(figsize=(11, 6))
ax = sns.heatmap([day_sentiment('trump','sentiment_density')],square = True,annot=True,annot_kws={'size':15,'weight':'bold'},linewidths = .1,                 vmin=-.9,vmax=0.,cmap='hot',yticklabels=['Sentiment'],xticklabels=shortdate,                 cbar_kws={'orientation': 'horizontal',"shrink": 0.3})
ax.tick_params(labelsize=12) 
ax.set(title= "Average Negative Sentiment Density of Daily Articles Stress On Candidate Donald Trump")


plt.figure(figsize=(11, 6))
ax1 = sns.heatmap([day_sentiment('biden','sentiment_density')],square = True,annot=True,annot_kws={'size':15,'weight':'bold'},linewidths = .1,                  vmin=-.9,vmax=0.,cmap='hot',yticklabels=['Sentiment'],xticklabels=shortdate,                  cbar_kws={'orientation': 'horizontal',"shrink": 0.3})
ax1.tick_params(labelsize=12) 
ax1.set(title= "Average Negative Sentiment Density of Daily Articles Stress On Candidate Joe Biden")


# In[192]:


# image 4 : NLTK compound scores in heatmap

"""
NLTK compound scores is calculated on daily-basis, and the formula presented below: 
sum(daily NLTK compound scores of candidate) / count(daily number of articles marked with candidate)
"""

plt.figure(figsize=(11, 6))
ax = sns.heatmap([day_sentiment('trump','compound')],square = True,annot=True,annot_kws={'size':15,'weight':'bold'},linewidths = .1,                 vmin=-.2,vmax=1.,cmap='hot',yticklabels=['Sentiment'],xticklabels=shortdate,                 cbar_kws={'orientation': 'horizontal',"shrink": 0.3})
ax.tick_params(labelsize=12) 
ax.set(title= "NLTK Compound Scores of Daily Articles Stress On Candidate Donald Trump")


plt.figure(figsize=(11, 6))
ax1 = sns.heatmap([day_sentiment('biden','compound')],square = True,annot=True,annot_kws={'size':15,'weight':'bold'},linewidths = .1,                  vmin=-.2,vmax=1.,cmap='hot',yticklabels=['Sentiment'],xticklabels=shortdate,                  cbar_kws={'orientation': 'horizontal',"shrink": 0.3})
ax1.tick_params(labelsize=12) 
ax1.set(title= "NLTK Compound Scores of Daily Articles Stress On Candidate Joe Biden")


# In[203]:


# image 5 : NLTK compound scores in stacked bar charts
data1 = day_sentiment('trump','compound')
data2 = day_sentiment('biden','compound')
data2.insert(0,0.0)

plt.figure(figsize=(9,7))
plt.bar(shortdate,data2,color="blue",label="biden")
plt.bar(shortdate,data1,color="red",bottom=np.array(data2),label="trump")
plt.title("NLTK Compound Sentiment Score",fontsize = 15,y=1.05)
plt.xlabel("Two weeks before election day",fontsize = 15,labelpad = 15) 
plt.ylabel("Scores",fontsize = 15,labelpad = 15) 

plt.legend(bbox_to_anchor=(1.0,1.0))
plt.show()


# In[65]:


# image 6 : bar + plot

def avg_sentiment(candidate):
    frame = df.loc[df['Topic'] == candidate,'sentiment density']
    return(round(frame.sum()/frame.count(),2))

candidate = ['Trump','Biden']
freq = [sum(trump_freq),sum(biden_freq)]
total_sent = [avg_sentiment('trump'),avg_sentiment('biden')]

plt.figure(figsize=(8, 6))
fig, ax = plt.subplots()
ax1 = ax.twinx()
ax.bar(candidate,freq,width=0.3,color=['red','blue'])
ax1.plot(candidate,total_sent, 'o-',color='black',markersize=10,label='Average Sentiment')

plt.title('Average Sentiment Density and Total Frequency candidates mentioned between Oct.20-Nov,2',fontsize=13)
plt.legend(prop = {'size':13})
ax.set_ylabel('Total Frequency',fontsize=18,labelpad = 15)
ax1.set_ylabel('Average Negative Sentiment',fontsize=18,labelpad = 15)
ax1.set_yticks(np.arange(-0.8,0.1,0.1)) 


# ### 
