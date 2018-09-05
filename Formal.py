from tweepy import *
import re
import emoji
import statistics
import math
import quandl
from tkinter import *
import numpy as np
import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt


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
        search = Cursor(self.api.search, q='#'+str(query), lang='en', count=20)
        counterOfTweets = 0
        TotalPosTweets = 0
        TotalNegTweets = 0
        TotalNeuTweets = 0

        try:
            for tweet in search.items(50):
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

    def RSIFunction(self):
        """RSI function : RSI = 100 - (100/1+RS)
        Where RS = Average Gain/Average LOSS"""

        Close = Data['Close'].get_values()
        print(Close)
        diffdelta = Close.diff()
        print(diffdelta)
        diffdelta = diffdelta[1:]
        print(diffdelta)#Gets rid of the first row, as it has no upper row to calculate differences
        up, down = diffdelta.copy(), diffdelta.copy()
        up[up < 0] = 0
        down[down > 0] = 0

        rollmeanup = up.rolling(14).mean()
        rollmeandown = down.rolling(14).mean()

        print(rollmeanup)
        RS = rollmeanup/rollmeandown
        RSI = 100.0 - (100.0 / (1.0 + RS))
        print(RSI)                          #NEEDS FIXING


    def DisplayStockGraph(self):

        plt.style.use('ggplot')
        fig = plt.figure()
        fig.suptitle(stockentry+' STOCK DATA', fontsize=12)

        Data['MA50'] = Data['Close'].rolling(5).mean()#Creates A 5-Day Moving Average
        plt.plot(Data['Close'])
        plt.plot(Data['MA50'], label="Moving Average")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand",borderaxespad=0.)  # Line of code taken from https://matplotlib.org/users/legend_guide.html
        plt.show()
        self.RSIFunction()

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
        self.master.configure(background='snow')

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
        if entry == "Help With Stock Graph":
            self.HelpStock()
        elif entry == "Help with Twitter Query":
            self.HelpTwitter()
        else:
            self.About()

    def HelpStock(self):
        pass

    def HelpTwitter(self):
        pass

    def About(self):
        pass

root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()