#============= Main Program ==================#
"""
MAIN file. Program To be Run from here.
External files include PostiveWords.txt and
Negative words.txt

"""
#========== Imports (Python Modules)==========#

from tweepy import *
import re
import emoji
import statistics
import math
import quandl
from tkinter import *
import pandas as pd
from tkinter.ttk import Progressbar
from scipy.stats import pearsonr
import time as tm
import numpy as np
from collections import Counter
from sklearn.feature_extraction.text import CountVectorizer
import matplotlib
from mpl_finance import candlestick_ohlc
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import *
import datetime

#======== API Keys (Tweepy and Quandl) =========#

consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token_key = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

Quandl_API = "9AK1N1LNy7PzHefyRR9w"

global TotalPosTweets
global TotalNegTweets
global query

global OverallTotalToPlot
OverallTotalToPlot = []

#===== Arrays(For Classification of Emojis) =====#


positiveEmojiList = [
    ':smile:',
    ':simple_smile:',
    ':laughing:',
    ':blush:',
    ':smiley:',
    ':relaxed:',
    ':heart_eyes:',
    ':grin:',
    ':grinning:',
    ':kissing:',
    ':sweat_smile:',
    ':joy:',
    ':satisfied:',
    ':crown:',
    ':face_with_tears_of_joy:',
    ':fire:',
    ':money_bag:',
    ':dollar_banknote:',
    ':glowing_star:',
    ':rolling_on_the_floor_laughing:',
    ':slightly_smiling_face:'
]

negativeEmojiList = [
    ':worried:',
    ':frowning:',
    ':anguished:',
    ':grimacing:',
    ':disappointed_relieved:',
    ':unamused:',
    ':fearful:',
    ':sob:',
    ':cry:',
    ':angry:',
    ':rage:',
    ':frowning:',
    ':man_shrugging:',
    ':face_screaming_in_fear:',
    ':crying_face:',
    ':pouting_face:',
    ':flushed_face:'
]

negation = [
    'no',
    'not',
    "couldn't",
    "wasn't",
    "didn’t",
    "wouldn’t",
    "shouldn’t",
    "weren’t",
    "don’t",
    "doesn't",
    "haven't",
    "hasn't",
    "won't",
    "wont",
    "hadn't",
    "never",
    "none",
    "nobody",
    "nothing",
    "neither",
    "nor",
    "nowhere",
    "isn't",
    "can't",
    "cannot",
    "mustn't",
    "mightn't",
    "shan't",
    "without",
    "needn't"
]

class Twitter(object):

    def __init__(self):
        #=====Access Twitter Database by calling on the API Keys=====#
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.api = API(self.auth)

    def Trends(self):
        global TopTopics
        Trends = self.api.trends_place(
            1)  # Uses the API to get most retweeted tweets in the world(1)
        Trend_Data = Trends[0]
        Trend_Data = Trend_Data['trends']  #Creates a data frame for Trend data
        topicname = [Trend_Data['name'] for Trend_Data in Trend_Data]
        TopTopics = list()
        for i in topicname[0:5]:
            TopTopics.append(i)  #Appends the top 5 retweeted tweets.

        TopTopics = '\n'.join(
            TopTopics)  #creates a line between every Top Topic
        #TopTopics will be displayed in the tkinter page
        print(TopTopics)

    def Remove_URL(self, tweet):
        #Remove URL function
        #Removes URL from parsed_tweet and replaces them with '', (space)

        try:
            noUrl = re.sub(r'http\S+', '', str(tweet.text))
            return noUrl

        except:
            print("Error")

    def IdentifyEmoji(self, CleanTweet):
        #Identify Emojis
        #Calls on Emoji class and convert the image of emojis to description from the no url tweet data

        try:
            noEmoji = emoji.demojize(CleanTweet)
            return noEmoji

        except:
            print("Error in converting emojis")

    def CountSentimentOfEmojis(self, CleanTweetNoEmoji):
        #Count sentiment of Emojis by comparing emojis to the array of positive and negative emojis

        global positiveCounter
        global negativeCounter
        positiveCounter = 0
        negativeCounter = 0

        for word in CleanTweetNoEmoji.split():
            if word in positiveEmojiList:
                positiveCounter += 1

            elif word in negativeEmojiList:
                negativeCounter += 1

            else:
                pass

        return positiveCounter, negativeCounter

    def ClassifyWords(self, CleanTweet):
        global posWordCounter
        global negWordCounter

        posWordCounter = 0
        negWordCounter = 0

        PosFile = open("PositiveWords.txt").read()
        NegFile = open("NegativeWords.txt").read()

        nomarks = CleanTweet.replace('!', '')
        nomarks = nomarks.lower()
        nomarks = nomarks.replace('.', '')
        nomarks = nomarks.replace(':', '')

        word_counter = dict()

        try:
            for words in nomarks.split():
                if words in word_counter:
                    word_counter[words] += 1
                else:
                    word_counter[words] = 1
            for words in nomarks.split():
                if words in PosFile.splitlines():
                    if word_counter[words] > 1:
                        posWordCounter += (word_counter[words] * 1.3)
                        print(word_counter[words], posWordCounter)
                        print(words)
                    else:
                        posWordCounter += 1
                        print(words)
                elif words in NegFile.splitlines():
                    if word_counter[words] > 1:
                        negWordCounter += (word_counter[words] * 1.3)
                        print(word_counter[words], negWordCounter)
                        print(words)
                    else:
                        negWordCounter += 1
                        print(words)

        except:
            print("Error")

        return posWordCounter, negWordCounter

    def FrequencyTables(self, CleanTweet):
        global OverallTotal
        positiveTweets = 0
        negativeTweets = 0

        TotalPos = posWordCounter + positiveCounter
        TotalNeg = negWordCounter + negativeCounter
        OverallTotal = (TotalPos - TotalNeg) / (len(CleanTweet.split()))
        OverallTotalToPlot.append(OverallTotal)

        global negative_tweets
        global positive_tweets
        negative_tweets = dict()
        positive_tweets = dict()

        if OverallTotal > 0:
            print("Positive Tweet", OverallTotal)
            try:
                positive_tweets[CleanTweet] = OverallTotal
                print(positive_tweets)
            except:
                print("error")
        elif OverallTotal < 0:
            print("Negative Tweet", OverallTotal)
            try:
                negative_tweets[CleanTweet] = OverallTotal
                print(negative_tweets)

            except:
                print("error")

        else:
            print("Neutral")

        return positiveTweets, negativeTweets, OverallTotal

    def Main(self):

        search = Cursor(
            self.api.search, q=('#' + str(query)), lang='en', count=10)

        global counterOfTweets
        counterOfTweets = 0
        TotalPosTweets = 0
        TotalNegTweets = 0
        TotalNeuTweets = 0

        try:
            for tweet in search.items(20):

                #if tweet.created_at < endDate and tweet.created_at > startDate

                counterOfTweets += 1
                CleanTweet = self.Remove_URL(tweet)
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)
                CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji)
                classifyWords = self.ClassifyWords(CleanTweet)
                countNumbers = self.FrequencyTables(CleanTweet)

                print("noEmoji:", counterOfTweets, CleanTweet,
                      CleanTweetNoEmoji, CountEmoji, classifyWords,
                      countNumbers)
                if OverallTotal > 0:
                    TotalPosTweets += 1

                elif OverallTotal < 0:
                    TotalNegTweets += 1

                else:
                    TotalNeuTweets += 1

            print(TotalPosTweets, TotalNegTweets)

            global OverallSentiment
            OverallSentiment = ((TotalPosTweets - TotalNegTweets) / (
                TotalPosTweets + TotalNegTweets + TotalNeuTweets))
            print("Overall the Total Sentiment of", str(counterOfTweets),
                  "tweets is:", OverallSentiment)

            if OverallSentiment > 0:
                print("Hence , Positive")
            elif OverallSentiment < 0:
                print("Hence, Negative")
            else:
                print("Hence, Neutral")

        except error.TweepError as e:
            print(e.reason)
            print("error")


class Stock(object):

    def __init__(self):
        quandl.ApiConfig.api_key = Quandl_API
        self.Twitter = Twitter()
        self.StockData()

    def StockData(self):
        """
            Pulls Stock Data via the Quandl API
        """
        try:
            print(stockentry)
            global Data
            #data = quandl.get('WIKI/' + str(stockentry), rows=50)
            data = quandl.get('EOD/' + str(stockentry), rows=7)
            print(data)
            Data = data

            return Data

        except:
            pass


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.Stock = Stock()
        self.Twitter = Twitter()
        self.main_window()

    def main_window(self):
        self.master.title("Main")
        self.master.configure(
            background='snow', highlightbackground='light steel blue')

        self.Twitter.Trends()

        self.canvas = Canvas(self.master, width=670, height=450)
        self.canvas.grid(row=0, column=0, sticky='nsew')

        self.line = self.canvas.create_rectangle(
            329, -10, 332, 450, fill='light blue'
        )  #Seprates the Main window - Left=Stock Right=Twitter Query

        self.rectangle = self.canvas.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        self.rectangle_bottomn = self.canvas.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')

        self.LabelTQ = Label(
            self.master, text='Twitter Query:', font=("Avenir", 14))
        self.EntryTQ = Entry(self.master, borderwidth=2)

        self.ButtonTQ = Button(
            self.master,
            text="Enter",
            font=("Avenir", 14),
            command=self.TwitterQueryEntry)

        self.LabelT = Label(
            self.master, text="Select Company:", font=("Avenir", 14))
        self.var = StringVar(self.master)

        self.Choice = ["AAPL", "AMZN", "MSFT", "NKE"]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master, self.var,
                            *self.Choice)  # Drop Down Menu
        self.ButtonT = Button(
            self.master,
            text="Enter",
            font=("Avenir", 14),
            command=self.CompanyEntry)

        self.LabelT.place(x=360, y=100)
        self.w.place(x=360, y=130)
        self.ButtonT.place(x=360, y=170)

        self.LabelTQ.place(x=30, y=100)
        self.EntryTQ.place(x=30, y=130)
        self.ButtonTQ.place(x=30, y=170)

        self.LabelWP = Label(
            self.master,
            text="Stock and Sentiment Program",
            font=("Avenir", 20),
            foreground='white',
            activebackground='light sky blue',
            background='light sky blue')
        self.LabelGU = Label(
            self.master,
            text="Please Enter the Twitter Query First",
            font=("Avenir", 14))
        self.LabelSH = Label(
            self.master,
            text="Press Help to view Ticker Infromation",
            font=("Avenir", 14))
        self.LabelTT = Label(
            self.master,
            text="Hot Topics In Twitter",
            font=("Avenir", 14),
            foreground='salmon')
        self.LabelTt = Label(
            self.master,
            text=(TopTopics),
            foreground='black',
            font=("Avenir", 14),
            relief='groove')

        self.LabelTt.place(x=40, y=300)
        self.LabelTT.place(x=48, y=270)
        self.LabelSH.place(x=360, y=50)
        self.LabelGU.place(x=30, y=50)
        self.LabelWP.place(x=195, y=10)

        self.ButtonHP = Button(
            self.master,
            text="Help",
            font=("Avenir", 14),
            background='light sky blue',
            activebackground='light sky blue',
            command=self.GoToHelpPage)

        self.ButtonHP.place(x=600, y=10)

    def CompanyEntry(self):
        """Retrives Entry of USER"""
        global stockentry
        try:
            self.ButtonVG = Button(
                self.master, text="View Graph", command=self.GoToStockPage)
            self.ButtonVG.place(x=350, y=350)

            self.LabelCP = Label(
                self.master,
                text="Loading...",
                font=("Avenir", 12),
                foreground='salmon')
            self.LabelCP.place(x=350, y=320)
            stockentry = self.var.get()
            self.Stock.StockData()

        except:
            print("Error")

    def TwitterQueryEntry(self):
        try:
            global query
            query = self.EntryTQ.get()
            print(query)
            self.Twitter.Main()

        except:
            print("Error")

    def GoToHelpPage(self):
        self.helppage = Toplevel(self.master)
        self.app = HelpPage(self.helppage)

    def GoToStockPage(self):
        self.stockpage = Toplevel(self.master)
        self.app = StockPage(self.stockpage)


class HelpPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.masters = master
        self.master.geometry("660x440")
        self.create_Help_Page()

    def create_Help_Page(self):
        self.masters.title("Help Page")
        self.masters.configure(
            background='white', highlightbackground='light steel blue')

        self.canvashp = Canvas(self.masters,width=670,height=480)
        self.canvashp.grid(row=0, column=0, sticky='nsew')

        self.rectangle_top = self.canvashp.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        self.rectangle_bottom = self.canvashp.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')

        self.LabelHp = Label(
            self.master,
            text="Help Page",
            font=("Avenir", 20),
            foreground='white',
            activebackground='light sky blue',
            background='light sky blue')

        self.LabelHp.place(x=280,y=10)

        self.LabelHP = Label(self.masters, text="Select an Option:")
        self.var = StringVar(self.masters)
        self.Choice = [
            "Help With Stock Graph", "Help with Twitter Query", "About"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.masters, self.var,
                            *self.Choice)  # Drop Down Menu
        self.buttonx = Button(
            self.masters, text="Enter",command=self.getEntry)

        self.LabelHP.place(x=39, y=100)
        self.w.place(x=30, y=130)
        self.buttonx.place(x=30, y=170)

    def getEntry(self):
        entry = self.var.get()
        print(entry)
        if entry == "Help With Stock Graph":
            self.HelpStock()
        elif entry == "Help with Twitter Query":
            self.HelpTwitter()
        else:
            self.About()

    def HelpStock(self):
        self.LabelHS = Label(
            self.masters,
            text=
            "Ticker Information \n AAPL = APPLE \n AMZN = AMAZON \n MSFT = MICROSOFT \n NKE = NIKE",
            font=("Avenir", 12),
            foreground='light sky blue',
            relief='groove'
        )

        self.LabelHS.place(x=300, y=150)

    def HelpTwitter(self):

        self.LabelHT = Label(
            self.masters,
            text=
            "Enter your Query and Hit Enter Button \n This query will used to pull Twitter Data from the Database",
            font=("Avenir", 12)
        )
        self.LabelHT.place(x=300, y=100)

    def About(self):
        pass


class StockPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.mastersp = master
        self.master.geometry("660x440")
        self.Twitter = Twitter()
        self.GraphStock()

    def GraphStock(self):

        self.mastersp.title("Tweet and Graph Page")
        s = []
        with open("Parsed_Tweets.txt", 'r') as r:
            s.append(r.read())

        print(OverallTotalToPlot)
        df = pd.DataFrame({'values': OverallTotalToPlot})

        self.canvashp = Canvas(self.mastersp, width=670, height=480)
        self.canvashp.grid(row=0, column=0, sticky='nsew')

        self.rectangle_top = self.canvashp.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        self.rectangle_bottom = self.canvashp.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')

        self.Labelsp = Label(
            self.mastersp,
            text="Twiter Sentiment Page",
            font=("Avenir", 20),
            foreground='white',
            activebackground='light sky blue',
            background='light sky blue')

        self.Labelsp.place(x=240,y=10)

        self.LabelGO = Label(
            self.mastersp,
            text=("Overall Sentiment of Tweets:", OverallSentiment),
            font=("Avenir", 14),
            relief='groove'
        )

        self.LabelWI = Label(
            self.mastersp,
            text=("Information About Indicators/Graph:"),
            font=("Avenir", 14))
        self.varc = StringVar(self.master)
        self.Choices = ["Bollinger Bands", "Moving Average", "Candlestick"]
        self.varc.set(self.Choices[0])
        self.om = OptionMenu(self.mastersp, self.varc,
                             *self.Choices)  # Drop Down Menu
        self.buttonx = Button(
            self.mastersp, text="Enter", command=self.GetEntryIndicator)

        self.LabelWI.place(x=20, y=130)
        self.om.place(x=20, y=160)
        self.buttonx.place(x=20, y=190)

        self.LabelGO.place(x=20, y=100)

        print("YES", positive_tweets)
        print("No,", negative_tweets)

        plt.style.use('ggplot')
        MovingAverage = Data['Close'].rolling(3).mean()

        # Creates A 3-Day Moving Average
        Data['MA50'] = Data['Close'].rolling(2).mean()

        # Calculates Standard Deviation on rolling mean
        StandardDeviation = Data['Close'].rolling(2).std()

        # Bollinger Bands Indicator - Upper Boundary
        Data['UpBB'] = MovingAverage + (2 * StandardDeviation)

        # Bollinger Bands Indicator- Lower Boundary
        Data['LowBB'] = MovingAverage - (2 * StandardDeviation)

        fig = plt.figure(figsize=(9, 9))
        fig.suptitle(stockentry + ' STOCK DATA', fontsize=12)

        ax = plt.subplot2grid((2, 2), (0, 0), colspan=4, rowspan=1)
        Data['Date'] = Data.index.map(mdates.date2num)
        plt.plot(Data['Close'], Label="Close", color="yellow")

        plt.pause(0.05)
        plt.plot(Data['MA50'], label="Moving Average", color="blue")
        plt.pause(0.05)
        plt.plot(Data['UpBB'], Label="Upper Bollinger Band", color="black")
        plt.pause(0.05)
        plt.plot(Data['LowBB'], Label="Lower Bollinger Band", color="grey")
        plt.pause(0.05)
        plt.xlabel("Date")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.legend(loc='best')
        ax.set_ylabel('Value')

        Data['Date'] = Data.index.map(mdates.date2num)
        candlestickData = Data[['Date', 'Open', 'High', 'Low', 'Close']]
        candlestick_ohlc(
            ax,
            candlestickData.values,
            width=.3,
            colorup='green',
            colordown='red')
        plt.xlabel("Date")
        #ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        # ax.get_shared_x_axes().join(ax, ax2)

        ax4 = fig.add_subplot(2, 2, 3)
        Data['Date'] = Data.index.map(mdates.date2num)
        ax4.plot(Data['Close'], label='Close Price')
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d'))
        ax4.set_xlabel('Date')
        ax4.set_ylabel('Value')
        ax4.legend(loc='best')

        ax5 = fig.add_subplot(2, 2, 4)
        ax5.scatter(df, df['values'], label='Sentiment Value', color='blue')
        cofficient = pearsonr((df['values'][0:7]), Data['Close'])
        print("correlaction coefficient: ", str(cofficient))
        ax5.plot(
            cofficient,
            label='Pearson correlation coefficient',
            color='magenta')
        ax5.set_xlabel('Tweet')
        ax5.legend(loc='best')
        plt.show(ax)

    def GetEntryIndicator(self):
        choice_entry = self.varc.get()
        if choice_entry == 'Bollinger Bands':
            self.LabelBB = Label(
                self.mastersp,
                text=
                ("Bollinger Bands: \nWhen the market is volatile, the bands widen.\n When the market is under a less volatile period, the bands contract."
                 ),
                font=("Avenir", 14))
            self.LabelBB.place(x=30, y=200)

        elif choice_entry == 'Moving Average':
            self.LabelMA = Label(
                self.mastersp,
                text=("Moving Average is calculated by..."),
                font=("Avenir", 14)
            )

            self.LabelMA.place(x=30, y=280)

        else:
            self.LabelCS = Label(
                self.mastersp,
                text=("Candlestick Graph is generated by..."),
                font=("Avenir", 14))
            self.LabelCS.place(x=30, y=320)

    def FindCorrelation(self):
        pass


root = Tk()
root.geometry("660x440")

app = Window(root)
root.mainloop()
