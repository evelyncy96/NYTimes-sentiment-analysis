 ## Analyzing the sentiment of NY Times articles related to candidates Donald Trump and Joe Biden from 2020/10/20 to 2020/11/02 (Two weeks before the election day) <br><br>
 
 
 This repository contains the code and [Loughran and McDonald positive and negative dictionaries](https://sraf.nd.edu/textual-analysis/resources/) used to calculate the sentiment scores for each articles. The visualization results were uploaded in 'Visulaization' document. <br><br>



**I divided my code into 12 parts, the description for each parts were presented below:** <br>
* part0: Import libraries and packages
* part1-4: Collect the articles url from [NYTimes archive](https://help.nytimes.com/hc/en-us/articles/115014772767-Archives) using Selenium
* part5: Web-scrape text, title, publish time of all articles and lower the article text
* part6: Tokenize each article text
* part7: Import Loughran and McDonald positive and negative dictionaries
* part8: Remove stopwords from article text
* part9: Calculate the amount of times "trump" and "biden" mentioned in each articles to find the media volume for each candidate
* part10-1: Using neg & pos wordbag from LM emotional dictionary to analyze sentiment for each article, score range from -1 to +1
* part10-2: Using Nltk SentimentIntensityAnalyzer to analyze sentiment for each article
* part11: Create DataFrame <br><br>

## Visualization of results: Introduction and personal insights found from Image1~6 <br>

    Image1: The Number Of Article Stressed On Different Candidates<br>

In part9, we calculated the frequency of word "Trump" and "Biden" mentioned in each articles in order to find the media volume for each candidate. We then divided each article into three categories, including "trump", "biden", and "both". If the amount of times "Trump" mentioned in each articles surpassed that of "biden", the article would be marked as "trump", otherwise it would be marked as "biden". And then If the amount of times "Trump" mentioned in each articles equals to that of "biden", it would be marked as "both". In image1, we presented the number of article with three categories on a daily basis.<br>

![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image1.png)
<br><br>


    Image2: The Frequency Both Candidates Mentioned In Articles<br>

In image2, we presented the sum of total frequency of words "Trump" and "Biden" in every article on a daily basis.<br>

![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image2.png)
<br>
* `Insight`
From Image1&2, we can tell that the media volume of candidate Donald Trump on New York Times is way higher then that of candidate Joe Biden, which means that New York Times articles discussed more about Donald Trump then Joe Biden. Now it is important to apply sentiment analysis on each article text to see whether or not NY Times preferred to present positive or negative emotion on each article marked with certain categories.

<br><br>

#### Image3: Average Negative Sentiment Density of Daily Articles Stressed On Both Candidate<br>

In part8, we removed stopwords from article text. And then in part 10-1, we calculate sentiment density in list 'sent_article', and the formula is presented below:<br>
sentiment density for each article = (# of positive token - # of negative token) / (# of positive token - # of negative token)<br>

In image3, we presented the average negative sentiment density of both candidates on a daily basis.<br>

![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image3.png)
<br><br>

#### Image4: NLTK compound scores in heatmap<br>

In part10-2, we use Nltk SentimentIntensityAnalyzer from `nltk.sentiment.vader` to analyze sentiment for each article
![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image4.png)
<br><br>
#### Image5: NLTK compound scores in stacked bar charts<br>


![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image5.png)
<br><br>
#### Image6: Average Sentiment Density and Total Frequency candidates mentioned between Oct.20-Nov,2<br>


![image](https://github.com/evelyncy96/NYTimes-sentiment-analysis/blob/main/Visualization/image6.png)




