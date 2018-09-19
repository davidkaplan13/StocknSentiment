#============= Main Program ==================#

#========== Imports (Python Modules)==========#

from tweepy import *
import re
import emoji
import statistics
import math
import quandl
from tkinter import *
import pandas as pd

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

#========== Arrays(For Classification of Emojis) ==========#

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
    'face_with_tears_of_joy',
    ':fire:',
    ':money_bag:',
    ':dollar_banknote:',
    ':glowing_star:'
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
    ':crying_face:'
]

class Twitter(object):

    def __init__(self):
        #=====Access Twitter Database by calling on the API Keys=====#
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.api = API(self.auth)

    def Trends(self):
        global TopTopics
        Trends = self.api.trends_place(1)
        Trend_Data = Trends[0]
        Trend_Data = Trend_Data['trends']
        topicname = [Trend_Data['name'] for Trend_Data in Trend_Data]
        TopTopics = list()
        for i in topicname[0:5]:
            TopTopics.append(i)

        TopTopics = '\n'.join(TopTopics)
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
        """Needs Fixing"""
        global posWordCounter
        global negWordCounter

        posWordCounter = 0
        negWordCounter = 0

        PosFile = open(
            "PositiveWords.txt"
        )  # PositiveWord List extracted from : http://ptrckprry.com/course/ssd/data/positive-words.txt
        NegFile = open("NegativeWords.txt")

        wordlist = []
        try:
            for words in CleanTweet.split():
                words.replace("#", "")  #Removes URL for analysis of words
                wordlist.append(words.lower())

            for i in range(0, len(wordlist)):
                if wordlist[i] in PosFile.read():
                    posWordCounter += 1
                    i += 1

                elif wordlist[i] in NegFile.read():
                    print(wordlist[i])
                    negWordCounter += 1
                    i += 1

                else:
                    i += 1

        except:
            print("No Such String")

        return posWordCounter, negWordCounter

    def FrequencyTables(self, CleanTweet):
        global OverallTotal
        positiveTweets = 0
        negativeTweets = 0

        TotalPos = posWordCounter + positiveCounter
        TotalNeg = negWordCounter + negativeCounter
        OverallTotal = (TotalPos - TotalNeg) / (len(CleanTweet.split()))
        OverallTotalToPlot.append(OverallTotal)

        if OverallTotal > 0:
            print("Positive Tweet", OverallTotal)
        elif OverallTotal < 0:
            print("Negative Tweet", OverallTotal)

        else:
            print("Neutral")

        return positiveTweets, negativeTweets, OverallTotal

    def FindCorrelation(self):

        closeValues = Data['Close'].get_values()
        x = closeValues
        y = OverallTotal
        N = 50
        n = 50
        t = ((statistics.mean(x) - statistics.mean(y)) / (math.sqrt((
            (statistics.stdev(x) ^ 2) / N)) + ((statistics.stdev(y) ^ 2) / n)))
        #Student T-test - x - Sample 1, y-Sample 2 , N is sample 1, n is sample 2

    def Main(self):

        startDate = datetime.datetime(2018, 9, 10, 0, 0, 0)
        endDate = datetime.datetime(2018, 9, 17, 0, 0, 0)

        search = Cursor(
            self.api.search, q=('#' + str(query)), lang='en', count=2)

        #search = got3.manager.TweetCriteria().setQuerySearch('westbrook').setSince("2018-01-01").setUntil("2018-01-31")
        #AllTweets = got3.manager.TweetManager.getTweets(search)

        global counterOfTweets
        counterOfTweets = 0
        TotalPosTweets = 0
        TotalNegTweets = 0
        TotalNeuTweets = 0

        posTweets = list()
        negTweets = list()

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
                    posTweets.append(tweet.text)
                elif OverallTotal < 0:
                    TotalNegTweets += 1
                    negTweets.append(tweet.text)
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

            #self.Twitter.FindCorrelation()

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

        self.line = self.canvas.create_line(
            329, -10, 329, 450, fill='light steel blue'
        )  #Seprates the Main window - Left=Stock Right=Twitter Query

        self.LabelT = Label(
            self.master, text="Select Company:", font=("Avenir", 14))
        self.var = StringVar(self.master)

        self.LabelTQ = Label(
            self.master, text='Twitter Query:', font=("Avenir", 14))
        self.EntryTQ = Entry(self.master, borderwidth=2)
        self.ButtonTQ = Button(
            self.master,
            text="Enter",
            font=("Avenir", 14),
            command=self.TwitterQueryEntry)

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
            text="Welcome To Stock/Sentiment",
            font=("Avenir", 16),
            foreground='blue')
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
            foreground='red')
        self.LabelTt = Label(
            self.master,
            text=(TopTopics),
            font=("Avenir", 14),
            relief='groove')

        self.LabelTt.place(x=30, y=300)
        self.LabelTT.place(x=45, y=270)
        self.LabelSH.place(x=360, y=50)
        self.LabelGU.place(x=30, y=50)
        self.LabelWP.place(x=30, y=10)

        self.ButtonHP = Button(
            self.master, text="Help", command=self.GoToHelpPage)
        self.ButtonVG = Button(
            self.master, text="View Graph", command=self.GoToStockPage)
        self.ButtonVG.place(x=350, y=350)
        self.ButtonHP.place(x=600, y=10)

    def CompanyEntry(self):
        """Retrives Entry of USER"""
        global stockentry
        try:
            self.LabelCP = Label(
                self.master, text="Loading", font=("Avenir", 12))
            self.LabelCP.place(x=350, y=400)
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
        self.master = master
        self.master.geometry("660x440")
        self.create_Help_Page()

    def create_Help_Page(self):
        self.master.title("Help Page")
        self.master.configure(
            background='snow', highlightbackground='light steel blue')

        self.LabelHP = Label(self.master, text="Select an Option:")
        self.var = StringVar(self.master)
        self.Choice = [
            "Help With Stock Graph", "Help with Twitter Query", "About"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master, self.var,
                            *self.Choice)  # Drop Down Menu
        self.buttonx = Button(self.master, text="Enter", command=self.getEntry)

        self.LabelHP.place(x=39, y=100)
        self.w.place(x=30, y=130)
        self.buttonx.place(x=30, y=170)

        self.canvas = Canvas(root, width=1000, height=1000)
        self.canvas.pack()

        self.line = self.canvas.create_line(
            329, -10, 329, 450, fill='light steel blue')

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
            self.master,
            text=
            "Ticker Information \n AAPL = APPLE \n AMZN = AMAZON \n MSFT = MICROSOFT \n NKE = NIKE",
            font=("Avenir", 12))
        self.LabelHS.place(x=300, y=150)

    def HelpTwitter(self):

        self.LabelHT = Label(
            self.master,
            text=
            "Enter your Query and Hit Enter Button \n This query will used to pull Twitter Data from the Database",
            font=("Avenir", 12))
        self.LabelHT.place(x=300, y=100)

    def About(self):
        pass


class StockPage(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("660x440")
        self.Twitter = Twitter()
        self.GraphStock()

    def GraphStock(self):

        self.master.title("Tweet and Graph Page")
        s = []
        with open("Parsed_Tweets.txt", 'r') as r:
            s.append(r.read())

        print(OverallTotalToPlot)
        today = datetime.datetime.now()
        past_week = today - datetime.timedelta(days=7)
        days = pd.date_range(past_week, today, periods=len(OverallTotalToPlot))
        df = pd.DataFrame({'date': days, 'values': OverallTotalToPlot})
        df.set_index(['date'])
        print(df)

        self.LabelGO = Label(
            self.master,
            text=("Overall Sentiment of Tweets:", str(OverallSentiment)),
            font=("Avenir", 14))

        self.LabelWI = Label(
            self.master,
            text=("Information About Indicators/Graph:"),
            font=("Avenir", 14))
        self.varc = StringVar(self.master)
        self.Choices = ["Bollinger Bands", "Moving Average", "Candlestick"]
        self.varc.set(self.Choices[0])
        self.om = OptionMenu(self.master, self.varc,
                             *self.Choices)  # Drop Down Menu
        self.buttonx = Button(
            self.master, text="Enter", command=self.GetEntryIndicator)

        self.LabelWI.place(x=20, y=100)
        self.om.place(x=20, y=130)
        self.buttonx.place(x=20, y=170)

        self.LabelGO.place(x=20, y=50)

        plt.style.use('ggplot')
        # Creates A 3-Day Moving Average
        Data['MA50'] = Data['Close'].rolling(3).mean()
        MovingAverage = Data['Close'].rolling(3).mean()

        # Calculates Standard Deviation on rolling mean
        StandardDeviation = Data['Close'].rolling(3).std()

        # Bollinger Bands Indicator - Upper Boundary
        Data['UpBB'] = MovingAverage + (2 * StandardDeviation)

        # Bollinger Bands Indicator- Lower Boundary
        Data['LowBB'] = MovingAverage - (2 * StandardDeviation)

        fig = plt.figure(figsize=(9, 9))
        fig.suptitle(stockentry + ' STOCK DATA', fontsize=12)

        ax = fig.add_subplot(2, 1, 1)
        Data['Date'] = Data.index.map(mdates.date2num)
        plt.plot(Data['Close'], Label="Close", color="green")
        plt.pause(0.05)
        plt.plot(Data['MA50'], label="Moving Average", color="blue")
        plt.pause(0.05)
        plt.plot(Data['UpBB'], Label="Upper Bollinger Band", color="red")
        plt.pause(0.05)
        plt.plot(Data['LowBB'], Label="Lower Bollinger Band", color="grey")
        plt.pause(0.05)
        plt.xlabel("Date")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.legend(loc='best')

        ax2 = fig.add_subplot(2, 1, 2)
        Data['Date'] = Data.index.map(mdates.date2num)
        candlestickData = Data[['Date', 'Open', 'High', 'Low', 'Close']]
        candlestick_ohlc(
            ax2,
            candlestickData.values,
            width=.7,
            colorup='green',
            colordown='red')
        plt.xlabel("Date")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        ax.get_shared_x_axes().join(ax, ax2)
        plt.show(ax)

        ax3 = fig.add_subplot(2, 1, 2)
        ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
        plt.plot(df['values'])
        plt.show()

    def GetEntryIndicator(self):
        choice_entry = self.varc.get()
        if choice_entry == 'Bollinger Bands':
            self.LabelBB = Label(
                self.master,
                text=
                ("Bollinger Bands: \nWhen the market is volatile, the bands widen.\n When the market is under a less volatile period, the bands contract. "
                 ),
                font=("Avenir", 14))
            self.LabelBB.place(x=30, y=200)

        elif choice_entry == 'Moving Average':
            self.LabelMA = Label(
                self.master,
                text=("Moving Average is calculated by..."),
                font=("Avenir", 14))
            self.LabelMA.place(x=30, y=280)

        else:
            self.LabelCS = Label(
                self.master,
                text=("Candlestick Graph is generated by..."),
                font=("Avenir", 14))
            self.LabelCS.place(x=30, y=320)


root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()
