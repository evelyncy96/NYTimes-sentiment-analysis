 ## Analyzing the sentiment of NY Times articles related to candidates Donald Trump and Joe Biden from 2020/10/20 to 2020/11/02 (Two weeks before the election day) <br><br>
 
 
 This repository contains the code and [Loughran and McDonald positive and negative dictionaries](https://sraf.nd.edu/textual-analysis/resources/) used to calculate the sentiment scores for each articles. The visualization results were uploaded in 'Visulaization' document. <br><br>



**I divided my code into 12 parts, the description for each parts were presented below:** <br>
* part0: Import libraries and packages
* part1-4: Collect the articles url using Selenium
* part5: Web-scrape text, title, publish time of all articles and lower the article text
* part6: Tokenize each article text
* part7: Import Loughran and McDonald positive and negative dictionaries
* part8: Remove stopwords from article text
* part9: Calculate the amount of times "trump" and "biden" mentioned in each articles to find the media volume for each candidate
* part10-1: Using neg & pos wordbag from LM emotional dictionary to analyze sentiment for each article, score range from -1 to +1
* part10-2: Using Nltk SentimentIntensityAnalyzer to analyze sentiment for each article
* part11: Create DataFrame <br><br>

**Visualization of results: Introduction and personal insights found from Image1~6** <br>








