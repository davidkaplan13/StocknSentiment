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
import quandl
from tkinter import *
import pandas as pd
from scipy.stats import pearsonr
import matplotlib
from mpl_finance import candlestick_ohlc
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib import *
import json
import random

#======== API Keys (Tweepy and Quandl) ========#

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

global negative_tweets
global positive_tweets
negative_tweets = dict()
positive_tweets = dict()

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

class Twitter(object):

    def __init__(self):
        """
        Access Twitter Database by calling on the API Keys
        """
        self.auth = OAuthHandler(consumer_key, consumer_secret) 
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.api = API(self.auth) # Used for the search method in the Main Function

    def Trends(self):
        global TopTopics
        Trends = self.api.trends_place(1)  # Uses the API to get most retweeted tweets in the world(1)
        Trend_Data = Trends[0]
        Trend_Data = Trend_Data['trends']  # Creates a data frame for Trend data
        topicname = [Trend_Data['name'] for Trend_Data in Trend_Data]
        TopTopics = list()
        for i in topicname[0:5]:
            TopTopics.append(i)  # Appends the top 5 retweeted tweets.

        TopTopics = '\n'.join(TopTopics) 
        # Creates a line between every Top Topic
        # TopTopics will be displayed in the tkinter page
        print(TopTopics)

    def Remove_URL(self, tweet):
        """
        Remove URL function
        Removes URL from parsed_tweet and replaces them with '', (space)
        """
        try:
            noUrl = re.sub(r'http\S+', '', str(tweet.text)) # Uses regex module to convert URL patterns to spaces
            return noUrl # Returns the text without URLS

        except:
            print("Error") # Basic Error Handling

    def IdentifyEmoji(self, CleanTweet):
        """
        Identify Emojis
        Calls on Emoji class and convert the image of emojis to description from the no url tweet data
        """
        try:
            noEmoji = emoji.demojize(CleanTweet) # Uses Emoji module to convert emoji image to description
            return noEmoji # Return text without emojis

        except:
            print("Error in converting emojis") #  Basic Error Handling

    def CountSentimentOfEmojis(self, CleanTweetNoEmoji):
        """
        Count sentiment of Emojis by comparing emojis to the array of positive and negative emojis
        """
        global positiveCounter
        global negativeCounter
        positiveCounter = 0 # Sets the positve counter to 0
        negativeCounter = 0 # Sets the negative counter to 0

        for word in CleanTweetNoEmoji.split(): # Splits the sentence to words
            if word in positiveEmojiList: # Checks for emojis in the positve emoji list
                positiveCounter += 1 # Adds 1 if emoji present in the positve emoji list

            elif word in negativeEmojiList: # Checks for emojis in the negative emoji list
                negativeCounter += 1 # Adds 1 if emoji present in the negative emoji list

            else:
                pass

        return positiveCounter, negativeCounter # Return positive and negative emoji counter

    def ClassifyWords(self, CleanTweet):
        global posWordCounter
        global negWordCounter

        posWordCounter = 0 # Sets the positive word counter to 0
        negWordCounter = 0 # Sets the negative word counter to 0

        PosFile = open("PositiveWords.txt").read() # Reads the positive word files
        NegFile = open("NegativeWords.txt").read() # Reads the negative word file

        nomarks = CleanTweet.replace('!', '') # Removes exclatiom marks from tweets
        nomarks = nomarks.lower() # Converts the text to lower, so no capitals as the word list are all lower case
        nomarks = nomarks.replace('.', '') # Replaces full stops with spaces
        nomarks = nomarks.replace(':', '') # Replaces colons with spaces

        word_counter = dict() # Creates an empty dictionary

        try:
            for words in nomarks.split(): # Iterates through words in the tweet text
                if words in word_counter:
                    word_counter[words] += 1 # Adds 1 to diciontary for associted word if already present in dictionary
                else:
                    word_counter[words] = 1 # Sets the value of the key (Word) to 1.
            for words in nomarks.split():
                if words in PosFile.splitlines(): # Checks if a word in the text is present in the positive file
                    if word_counter[words] > 1: # If the associated word is present in the text more than once
                        posWordCounter += (word_counter[words] * 1.3) # sets the positive counter to equal 1.3 * the value for the associated key word
                        print(word_counter[words], posWordCounter) 
                        print(words)
                    else:
                        posWordCounter += 1 # If word present in positive file but not present more than once in the tweet, then add 1 to the positive word counter
                        print(words)
                elif words in NegFile.splitlines(): # Checks if a word in the text is present in the negative file
                    if word_counter[words] > 1: # If the associated word is present in the text more than once
                        negWordCounter += (word_counter[words] * 1.3) #sets the negative counter to equal 1.3 * the value for the associated key word
                        print(word_counter[words], negWordCounter)
                        print(words)
                    else:
                        negWordCounter += 1 #If word present in negative file but not present more than once in the tweet, then add 1 to the positive word counter
                        print(words)

        except:
            print("Error") # Basic Error Handling

        return posWordCounter, negWordCounter

    def FrequencyTables(self, CleanTweet):
        global OverallTotal
        positiveTweets = 0 # Sets the positve tweet counter to 0
        negativeTweets = 0 # Sets the negative tweet counter to 0

        TotalPos = posWordCounter + positiveCounter # Adds the positive word counter and positve emoji counter together
        TotalNeg = negWordCounter + negativeCounter # Adds the negative word counter and negative emoji counter together
        OverallTotal = (TotalPos - TotalNeg) / (len(CleanTweet.split())) # Subtract negative counter from positive counter and divides result
        OverallTotalToPlot.append(OverallTotal) # Appends Results to array which would be used to plot sentiment of tweets in the main graph

        if OverallTotal > 0:
            print("Positive Tweet", OverallTotal)
            try:
                positive_tweets[CleanTweet] = OverallTotal # Appends the tweet and sets the value to sentiment result
                print(positive_tweets) # Prints out the positive value to user on the python console
            except:
                print("error") # Basic Error handling
        elif OverallTotal < 0:
            print("Negative Tweet", OverallTotal)
            try:
                negative_tweets[CleanTweet] = OverallTotal # Append the tweet and sets the value to sentiment result
                print(negative_tweets) # Prints out the negative value to user on the python console

            except:
                print("error") # Basic Error Handling

        else:
            print("Neutral") #Prints out neutral for any other tweet that is not classified in the If statements above.

        return positiveTweets, negativeTweets, OverallTotal # Return Variables

    def Main(self):

        search = Cursor(
            self.api.search, q=('#' + str(query)), lang='en', count=10)
        # Search Method for Twitter API. Uses the user entry for the query
        # Sets the parameters of the search method; Language = english, Count of retweets = 10

        global counterOfTweets
        counterOfTweets = 0 # Sets the counter of tweets to 0
        TotalPosTweets = 0 # Sets the positive tweet counter to 0
        TotalNegTweets = 0 # Sets the neutral tweets counter to 0
        TotalNeuTweets = 0 # Sets the negatuve tweets counter to 0

        try:
            for tweet in search.items(20): #Iterates through 20 pulled tweets
                counterOfTweets += 1 # Adds 1 to the parsed tweets
                CleanTweet = self.Remove_URL(tweet) # Calls on Remove URL function
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet) # Calls on Identify Emoji function
                CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji) # Calls on classification of emojis function
                classifyWords = self.ClassifyWords(CleanTweet) # Calls on classify word function
                countNumbers = self.FrequencyTables(CleanTweet) # Calls on Sentiment calculator

                print("noEmoji:", counterOfTweets, CleanTweet,
                      CleanTweetNoEmoji, CountEmoji, classifyWords,
                      countNumbers)
                if OverallTotal > 0: #  If the Overall value of sentiment is bigger than 0
                    TotalPosTweets += 1 # Add 1 to the positve tweet counter

                elif OverallTotal < 0: #If Overall value of sentiment is bigger than 0
                    TotalNegTweets += 1 # Add 1 to the negative tweet counter

                else:
                    TotalNeuTweets += 1 # Add 1 to neutral tweet counter

            print(TotalPosTweets, TotalNegTweets)

            global OverallSentiment
            OverallSentiment = ((TotalPosTweets - TotalNegTweets) / (
                TotalPosTweets + TotalNegTweets + TotalNeuTweets))
            # Overall Sentiment Shows the overall sentiment of all tweets
            # Calculated by subtracting negaitve tweets from positive tweets and dividing the result by all the parsed tweets
            print("Overall the Total Sentiment of", str(counterOfTweets),
                  "tweets is:", OverallSentiment)
            # Print statement showing the overall sentiment of CounterOfTweets(20) and the overall sentiment of those tweets
            if OverallSentiment > 0:
                print("Hence , Positive") # If the pverall sentiment is bigger than 0, then overall sentiment of 20 parsed tweets is positive
            elif OverallSentiment < 0:
                print("Hence, Negative") # If the overall sentiment is smaller than 0, then overall sentiment of 20 parsed tweets is negative
            else:
                print("Hence, Neutral") # Prints Neutral if overall sentiment not classified in the IF statments above.

        except error.TweepError as e:
            print(e.reason) # Prints Error of Twitter Search method to the user
            print("error") # Basic Error Handling


class Stock(object):

    def __init__(self):
        """
        Access the Quandl Databse via API keys
        """
        quandl.ApiConfig.api_key = Quandl_API
        self.Twitter = Twitter()
        self.StockData() # Calls on StockData Function

    def StockData(self):
        """
            Pulls Stock Data via the Quandl API
        """
        try:
            print(stockentry) # Print Statement showing user entry; done for compeltion purposes
            global Data
            data = quandl.get('EOD/' + str(stockentry), rows=7) # Retrieves the last 7 days end of day prices for the user selected company
            print(data)
            Data = data

            return Data

        except:
            pass # Basic Error Handling


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master) # initiate the Frame of the window
        self.master = master
        self.Stock = Stock()
        self.Twitter = Twitter()
        self.main_window()

    def main_window(self):
        self.master.title("Main") # Sets the title of the page as main.
        self.master.configure(
            background='snow', highlightbackground='light steel blue') # Sets the background color of the page

        self.Twitter.Trends() # Calls on the twitter trend function by referral statment

        self.canvas = Canvas(self.master, width=670, height=450) # Initiate the canvas size
        self.canvas.grid(row=0, column=0, sticky='nsew') # Places the canvas at row 0 and column 0

        self.line = self.canvas.create_rectangle(
            329, -10, 332, 450, fill='light blue')  
        #Seprates the Main window - Left=Stock Right=Twitter Query

        self.rectangle = self.canvas.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        # Creates a rectangle and fills the rectangle with a light sky blue color. This will be used as a banner for the title of the page
        self.rectangle_bottomn = self.canvas.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')
        # Creates a rectangle and fills the rectange with a salmon color. 
        self.LabelTQ = Label(
            self.master, text='Twitter Query:', font=("Avenir", 14))
        # Creates a text label. Created for easier navigation for the user
        self.EntryTQ = Entry(self.master, borderwidth=2)
        # Creates an entry box where the user can enter a query
        self.ButtonTQ = Button(
            self.master,
            text="Enter",
            font=("Avenir", 14),
            command=self.TwitterQueryEntry)
        # Creates a button to retrive user entry. Calls on function Twitter Query Entry, which retrives user entry
        self.LabelT = Label(
            self.master, text="Select Company:", font=("Avenir", 14))
        # Creates a text label. Created for easier navigation for the user
        self.var = StringVar(self.master)

        self.Choice = ["AAPL", "MCD", "MSFT", "NKE", "INTC", "BA", "DIS"]
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

        self.canvashp = Canvas(self.masters, width=670, height=480)
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

        self.LabelHp.place(x=280, y=10)

        self.LabelHP = Label(self.masters, text="Select an Option:")
        self.var = StringVar(self.masters)
        self.Choice = [
            "Help With Stock Graph", "Help with Twitter Query", "About"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.masters, self.var,
                            *self.Choice)  # Drop Down Menu
        self.buttonx = Button(
            self.masters, text="Enter", command=self.getEntry)

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

        choice = ["AAPL", "MCD", "MSFT", "NKE", "INTC", "BA", "DIS"]
        Ticker_Names = [
            "Apple", "McDonalds", "Microsoft", "Nike", "Intel Coporation",
            "Boeing Company", "The Walt Disney Company"
        ]

        Ticker_Name = dict()
        i = 0
        for i in range(0, len(choice)):
            Ticker_Name[choice[i]] = Ticker_Names[i]
            i += 1

        PrettyTicker_Name = json.dumps(Ticker_Name, indent=2)
        self.LabelHS = Label(
            self.masters,
            text=PrettyTicker_Name,
            font=("Avenir", 12),
            foreground='black',
            relief='groove')

        self.LabelHS.place(x=300, y=250)

    def HelpTwitter(self):

        self.LabelHT = Label(
            self.masters,
            text=
            "Enter your Query and Hit Enter Button \n This query will used to pull Twitter Data from the Database",
            font=("Avenir", 12))
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

        self.Labelsp.place(x=240, y=10)

        self.LabelGO = Label(
            self.mastersp,
            text=("Overall Sentiment of Tweets:", OverallSentiment),
            font=("Avenir", 14),
            relief='groove')

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

        self.canvashp.create_rectangle(300,50,600,350,outline='black',fill='white')
        self.canvashp.update()


        for k,i in positive_tweets.items():
            if i > 0.0 and i <= 0.05:
                x = random.randint(300,350)
                y = random.randint(100,150)

                def SmallCircle(event):
                    while event.x < 300 and event.x <600 and event.y < 50 and event.y > 350:
                        move = random.randint(0,4)
                        if move == 1:
                            self.canvashp.move(self.s,0,-10)
                        if move == 2:
                            self.canvashp.move(self.s,0,10)
                        if move == 3:
                            self.canvashp.move(self.s,-10,0)
                        else:
                            self.canvashp.move(self.s,10,0)

                self.s = self.canvashp.create_oval(x,y,x+15,y+15,fill='green')

                self.canvashp.tag_bind(self.s,"<ButtonPress-1>",SmallCircle)
                self.canvashp.update()

            if i > 0.05 and i <= 0.2:
                x = random.randint(350, 450)
                y = random.randint(150, 300)

                self.e = self.canvashp.create_oval(x,y,x+40,y+40,fill='green')
                self.canvashp.tag_bind(self.e,"<ButtonPress-1>",k)


            if i > 0.2 and i <= 0.4:
                x = random.randint(450, 500)
                y = random.randint(300, 350)

                def LargeCircle(event):
                    print(list(positive_tweets.keys())[list(positive_tweets.values()).index(i)])

                self.t = self.canvashp.create_oval(x,y,x+60,y+60,fill='green')
                self.canvashp.tag_bind(self.t,"ButtonPress-1>",LargeCircle)

            if i > 0.4:
                x = random.randint(500, 600)
                y = random.randint(400, 450)

                def XLargeCirle(event):
                    print(list(positive_tweets.keys())[list(positive_tweets.values()).index(i)])

                self.r = self.canvashp.create_oval(x,y,x+80,x+100,fill='green')
                self.canvashp.tag_bind(self.r,"<ButtonPRess-1>",XLargeCirle)

            self.canvashp.update()

        for ni in negative_tweets.values():
            if ni < 0.0 and ni > -0.05:
                x = random.randint(400, 350)
                y = random.randint(100, 150)
                self.s = self.canvashp.create_oval(x, y, x + 10, y + 10, fill='red')
            if ni < -0.05 and ni > -0.2:
                x = random.randint(450, 450)
                y = random.randint(150, 300)
                self.e = self.canvashp.create_oval(x, y, x + 20, y + 20, fill='red')
            if ni < -0.2 and ni > -0.4:
                x = random.randint(500, 500)
                y = random.randint(300, 350)
                self.t = self.canvashp.create_oval(x, y, x + 30, y + 30, fill='red')
            if ni < -0.4:
                x = random.randint(550, 600)
                y = random.randint(400, 450)
                self.r = self.canvashp.create_oval(x, y, x + 40, x + 50, fill='red')

        self.canvashp.update()


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
                font=("Avenir", 14))
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
