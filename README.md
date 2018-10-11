# Stock and Sentiment Analysis

A level Computer Science NEA

Main File --> "Formal.py"

The program aims to find correlation between tweet sentiment and stock movement of a company. 

Sentiment Analysis:

The sentiment analyser is created without the use of NLTK or TextBlob. The sentiment analyser takes into account the occurence of words and negation. It also parses emojis and classifies them. 

Additional Files are the word files. These are extracted from http://ptrckprry.com/course/ssd/data/positive-words.txt 
http://ptrckprry.com/course/ssd/data/negative-words.txt . These are used for classifying words into positive and negattive. 

For the Stock side:

Quandl Data is extracted via API keys. A candlestick and indicators are created producing a simple stock screener. 
Some indicators created:
- Bollinger Bands
- SMA

For the MAIN GUI:
- Tkinter is used. There is a help page, a main page and tweet and stock sentiment page which currently being developed (11/10/18)
