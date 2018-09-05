from tweepy import *
import re
import emoji
import statistics
import math
import quandl
from tkinter import *
import numpy as np
import matplotlib
from mpl_finance import candlestick_ohlc
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import *
import datetime
consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

Quandl_API = "9AK1N1LNy7PzHefyRR9w"

global TotalPosTweets
global TotalNegTweets

positiveEmojiList = [':smile:', ':simple_smile:', ':laughing:', ':blush:',
                     ':smiley:', ':relaxed:', ':heart_eyes:', ':grin:',
                     ':grinning:', ':kissing:', ':sweat_smile:', ':joy:',
                     ':satisfied:', ':crown:', 'face_with_tears_of_joy', ':fire:', ':money_bag:', ':dollar_banknote:',
                     ':glowing_star:']

negativeEmojiList = [':worried:', ':frowning:', ':anguished:', ':grimacing:',
                     ':disappointed_relieved:', ':unamused:', ':fearful:', ':sob:',
                     ':cry:', ':angry:', ':rage:', ':frowning:', ':man_shrugging:', ':face_screaming_in_fear:']


class Twitter(object):

    def __init__(self):
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token, access_token_secret)
        self.api = API(self.auth)


    def Remove_URL(self, tweet):

        try:
            noUrl = re.sub(r'http\S+', '', str(tweet.text))
            return noUrl

        except:
            print("Error")

    def IdentifyEmoji(self, CleanTweet):

        try:
            noEmoji = emoji.demojize(CleanTweet)
            return noEmoji

        except:
            print("Error in converting emojis")

    def CountSentimentOfEmojis(self, CleanTweetNoEmoji):

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
            "PositiveWords.txt")  # PositiveWord List extracted from : http://ptrckprry.com/course/ssd/data/positive-words.txt
        NegFile = open("NegativeWords.txt")

        wordlist = []
        try:
            for words in CleanTweet.split():
                wordlist.append(words.lower())

            for i in range(0, len(wordlist)):
                if wordlist[i] in PosFile.read():
                    posWordCounter += 1
                    i += 1

                elif wordlist[i] in NegFile.read():
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

        if OverallTotal > 0:
            print("Positive Tweet", OverallTotal)
        elif OverallTotal < 0:
            print("Negative Tweet", OverallTotal)

        else:
            print("Neutral")

        return positiveTweets, negativeTweets,OverallTotal


    def FindCorrelation(self):

        closeValues = Data['Close'].get_values()
        x = closeValues
        y = OverallTotal
        N = 50
        n = 50
        t = ((statistics.mean(x) - statistics.mean(y)) / (math.sqrt(((statistics.stdev(x) ^ 2) / N)) + ((statistics.stdev(y) ^ 2)/ n)))
        #Student T-test - x - Sample 1, y-Sample 2 , N is sample 1, n is sample 2

    def Main(self):
        x = 0
        y = 0
        if date == 1:
            print("Jan")
            x = datetime.datetime(2018,1,1)
            y = datetime.datetime(2018,1,31)
        elif date == 2:
            print("Feb")
            x = datetime.datetime(2018,2,1)
            y = datetime.datetime(2018,2,28)
        else:
            print("March")
            x = datetime.datetime(2018,3,1)
            y = datetime.datetime(2018,3,31)

        search = Cursor(self.api.search, q='#westbrook', lang='en', count=20)
        counterOfTweets = 0
        TotalPosTweets = 0
        TotalNegTweets = 0
        TotalNeuTweets = 0

        try:
            for tweet in search.items(50):
                if tweet.created_at < y and tweet.created_at > x: #NEEDS fixing
                    print(tweet)
                    counterOfTweets += 1
                    CleanTweet = self.Remove_URL(tweet)
                    CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)
                    CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji)
                    classifyWords = self.ClassifyWords(CleanTweet)
                    countNumbers = self.FrequencyTables(CleanTweet)

                    print("noEmoji:", counterOfTweets, CleanTweetNoEmoji, CountEmoji, classifyWords, countNumbers)
                    if OverallTotal > 0:
                        TotalPosTweets += 1
                    elif OverallTotal < 0:
                        TotalNegTweets += 1
                    else:
                        TotalNeuTweets += 1
                else:
                    print("NOPE")
            print(TotalPosTweets,TotalNegTweets)

            global OverallSentiment
            OverallSentiment = ((TotalPosTweets-TotalNegTweets)/(TotalPosTweets+TotalNegTweets+TotalNeuTweets))
            print("Overall the Total Sentiment of 50 tweets is:",OverallSentiment)

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
        try:
            print(stockentry)
            global Data
            data = quandl.get('WIKI/'+str(stockentry), rows=50)
            Data = data
            self.DisplayStockGraph()
            self.Twitter.FindCorrelation()

        except:
            pass

    def GraphClick(self,event):
        """Finds Location of CLICK x-data"""
        cx = float(event.xdata)
        global date
        date = 0
        if cx >= 734670 and cx < 736730:
            date = 1
        elif cx > 736730 and cx < 736760:
            date = 2
        else:
            date = 3

        self.Twitter.Main()

    def DisplayStockGraph(self):
        plt.style.use('ggplot')

        Data['MA50'] = Data['Close'].rolling(7).mean()#Creates A 7-Day Moving Average
        MovingAverage = Data['Close'].rolling(7).mean()
        StandardDeviation = Data['Close'].rolling(7).std()
        Data['UpBB'] = MovingAverage + (2 * StandardDeviation) #Bollinger Bands Indicator - Upper Boundary
        Data['LowBB'] = MovingAverage - (2 * StandardDeviation) #Bollinger Bands Indicator- Lower Boundary

        fig = plt.figure(figsize=(9, 9))
        fig.suptitle(stockentry + ' STOCK DATA', fontsize=12)

        ax = fig.add_subplot(2, 1, 1)
        Data['Date'] = Data.index.map(mdates.date2num)
        plt.plot(Data['Close'], Label="Close",color="green")
        plt.plot(Data['MA50'], label="Moving Average",color="blue")
        plt.plot(Data['UpBB'], Label="Upper Bollinger Band",color="red")
        plt.plot(Data['LowBB'], Label="Lower Bollinger Band",color="grey")
        plt.xlabel("Date")
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        plt.legend(loc='best')

        ax2 = fig.add_subplot(2, 1, 2)
        Data['Date'] = Data.index.map(mdates.date2num)
        candlestickData = Data[['Date', 'Open', 'High', 'Low', 'Close']]
        candlestick_ohlc(ax2, candlestickData.values, width=.6, colorup='green', colordown='red')
        plt.xlabel("Date")
        ax2.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        fig.canvas.mpl_connect('button_press_event',self.GraphClick)
        plt.show(ax)



class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.main_window()
        self.Stock = Stock()
        self.Twitter = Twitter()

    def main_window(self):
        self.master.title("Main")
        self.master.configure(background='snow', highlightbackground='light steel blue')
        #self.image = PhotoImage(Image.open(""))

        self.canvas = Canvas(root,width=670,height=450)
        self.canvas.pack()

        self.line = self.canvas.create_line(329,-10,329,450,fill='light steel blue') #Seprates the Main window - Left=Stock Right=Twitter Query

        self.LabelT = Label(self.master, text="Select Company:", font=("Calibri", 14))
        self.var = StringVar(self.master)

        self.LabelTQ = Label(self.master,text='Twitter Query:',font=("Calibri",14))
        self.EntryTQ = Entry(self.master,borderwidth=2)
        self.ButtonTQ = Button(self.master, text="Enter", command=self.TwitterQueryEntry)

        self.Choice = [
            "AAPL",
            "AMZN",
            "MSFT"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master, self.var, *self.Choice)  # Drop Down Menu
        self.ButtonT = Button(self.master, text="Enter", command=self.CompanyEntry)

        self.LabelT.place(x=30, y=100)
        self.w.place(x=30, y=130)
        self.ButtonT.place(x=30, y=170)

        self.LabelTQ.place(x=360,y=100)
        self.EntryTQ.place(x=360,y=130)
        self.ButtonTQ.place(x=360,y=170)

        self.LabelWP = Label(self.master, text="Welcome To Stock/Sentiment", font=("Calibri", 14), underline=True)
        self.LabelWP.place(x=50, y=10)

        self.ButtonHP = Button(self.master,text="Help",command=self.GoToHelpPage)
        self.ButtonHP.place(x=600,y=10)


    #def DisplayOS(self):
        #self.LabelOS = Label(self.master, text='Overall Sentiment: ' + str(OverallSentiment), font=("Calibri", 14))
        #self.LabelOS.place(x=360, y=300)

    def CompanyEntry(self):
        """Retrives Entry of USER"""
        global stockentry
        try:
            stockentry = self.var.get()
            self.Stock.StockData()

        except:
            print("Error")

    def TwitterQueryEntry(self):
        global query
        try:
            query = self.EntryTQ.get()
            print(query)
            self.Twitter.Main()

        except:
            print("Error")

    def GoToHelpPage(self):
        self.helppage= Toplevel(self.master)
        self.app = HelpPage(self.helppage)

class HelpPage(Frame):

    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("660x440")
        self.create_Help_Page()


    def create_Help_Page(self):
        self.master.title("Help Page")
        self.master.configure(background='snow',highlightbackground='light steel blue')

        self.LabelHP = Label(self.master,text="Select an Option:")
        self.var = StringVar(self.master)
        self.Choice = [
            "Help With Stock Graph",
            "Help with Twitter Query",
            "About"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master, self.var, *self.Choice)  # Drop Down Menu
        self.buttonx = Button(self.master,text="Enter",command=self.getEntry)

        self.LabelHP.place(x=39,y=100)
        self.w.place(x=30, y=130)
        self.buttonx.place(x=30, y=170)

        self.canvas = Canvas(root, width=670, height=450)
        self.canvas.pack()

        self.line = self.canvas.create_line(329, -10, 329, 450, fill='light steel blue')


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
        self.LabelHS = Label(self.master,text="Ticker Information \n AAPL = APPLE \n AMZN = AMAZON \n MSFT = MICROSOFT" , font=("Calibri", 12))
        self.LabelHS.place(x=300,y=150)

    def HelpTwitter(self):

        self.LabelHT = Label(self.master,text="Enter your Query and Hit Enter Button \n This query will used to pull Twitter Data from the Database",font=("Calibri",12))
        self.LabelHT.place(x=300,y=100)

    def About(self):
        pass


root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()