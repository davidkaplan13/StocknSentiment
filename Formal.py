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

global positiveEmojiList
global negativeEmojiList

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
        self.MainLoop()

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

        return positiveTweets, negativeTweets

    def FindCorrelation(self):

        closeValues = Data['Close'].get_values()
        #t = ((statistics.mean(x) - statistics.mean(y)) / (math.sqrt((statistics.stdev(x) ^ 2 / N)) + (statistics.stdev(y) ^ 2 / n)))
        ##Student T-test - x - Sample 1, y-Sample 2 , N is sample 1, n is sample 2

    def MainLoop(self):

        search = Cursor(self.api.search, q='#westbrook', lang='en', count=20)
        counterOfTweets = 0

        try:
            for tweet in search.items(7):
                counterOfTweets += 1
                CleanTweet = self.Remove_URL(tweet)
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)
                CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji)
                classifyWords = self.ClassifyWords(CleanTweet)
                countNumbers = self.FrequencyTables(CleanTweet)

                print("noEmoji:", counterOfTweets, CleanTweetNoEmoji, CountEmoji, classifyWords, countNumbers)


        except error.TweepError as e:
            print(e.reason)
            print("error")


Twitter()

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
            #self.Twitter.FindCorrelation()

        except:
            pass


    def DisplayStockGraph(self):

        plt.style.use('ggplot')
        fig = plt.figure()
        fig.suptitle(stockentry+' STOCK DATA', fontsize=12)

        Data['MA50'] = Data['Close'].rolling(5).mean()#Creates A 5-Day Moving Average
        plt.plot(Data['Close'])
        plt.plot(Data['MA50'], label="Moving Average")
        plt.legend(bbox_to_anchor=(0., 1.02, 1., .102), loc=3, ncol=2, mode="expand",borderaxespad=0.)  # Line of code taken from https://matplotlib.org/users/legend_guide.html
        plt.show()

class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.master = master
        self.main_window()
        self.Stock = Stock()

    def main_window(self):

        self.master.title("Main")
        self.master.configure(background='snow', highlightbackground='light steel blue')

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

    def CompanyEntry(self):
        """Retrives Entry of USER"""
        global stockentry
        try:
            stockentry = self.var.get()
            self.Stock.StockData()

        except:
            print("Error")

    def TwitterQueryEntry(self):
        query = self.EntryTQ.get()
        print(query)

root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()