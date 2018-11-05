# ============= Main Program ==================#
"""
MAIN file. Program To be Run from here.
External files include PostiveeWords.txt and
Negative words.txt

"""
# ========== Imports (Python Modules)==========#

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
#===============================================#
# ======== API Keys (Tweepy and Quandl) ========#

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

#================================================#
# ===== Arrays(For Classification of Emojis) =====#

positiveEmojiList = [
    'smile',
    'simple_smile',
    'laughing',
    'blush',
    'smiley',
    'relaxed',
    'heart_eyes',
    'grin',
    ':grinning',
    'kissing',
    'sweat_smile',
    'joy',
    'satisfied',
    'crown',
    'face_with_tears_of_joy',
    'fire',
    'money_bag',
    'dollar_banknote',
    'glowing_star',
    'rolling_on_the_floor_laughing',
    'slightly_smiling_face',
    'smiling_face'
]

negativeEmojiList = [
    'worried',
    'frowning',
    'anguished',
    'grimacing',
    'disappointed_relieve',
    'unamused',
    'fearful',
    'sob',
    'cry',
    'angry',
    'rage',
    'frowning',
    'man_shrugging',
    'face_screaming_in_fear',
    'crying_face',
    'pouting_face',
    'flushed_face'
]

WordWeighPositive = {
    "amuse":"3",
    "awesome":"4",
    "breathtaking":"5",
    "brilliant":"4",
    "excellent":"3",
    "excited":"3",
    "fabulous": "4",
    "facinate":"3",
    "faithful":"3",
    "fantastic":"4",
    "funny":"3",
    "good":"2",
    "great":"3",
    "happiness": "2",
    "hurrah":"4",
    "impressive":"4",
    "perfect":"3",
    "love":"5"
}

WordWeighNegative = {
    "angry":"3",
    "abuse":"5",
    "accuse":"2",
    "aggressive":"3",
    "betrayal":"3",
    "bullshit":"4",
    "depressive":"4",
    "stupid":"2",
    "kill":"3",
    "lunatic":"4"
}

negationWords = [
    "no",
    "not",
    "none",
    "nothing",
    "never",
    "nowhere",
    "wasnt",
    "wasn't",
    "shouldnt",
    "shouldn't",
    "couldnt",
    "couldn't",
    "wont",
    "won't",
    "cant",
    "can't",
    "don't",
    "dont"
]
#==================================================#

class Twitter(object):

    def __init__(self):
        """
        Access Twitter Database by calling on the API Keys
        """
        self.auth = OAuthHandler(consumer_key, consumer_secret)
        self.auth.set_access_token(access_token_key, access_token_secret)
        self.api = API(self.auth)  # Used for the search method in the Main Function

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
            noUrl = re.sub(r'http\S+', '', str(tweet.text))  # Uses regex module to convert URL patterns to spaces
            return noUrl  # Returns the text without URLS

        except:
            print("Error")  # Basic Error Handling

    def IdentifyEmoji(self, CleanTweet):
        """
        Identify Emojis
        Calls on Emoji class and convert the image of emojis to description from the no url tweet data
        """
        try:
            noEmoji = emoji.demojize(CleanTweet)  # Uses Emoji module to convert emoji image to description
            return noEmoji  # Return text without emojis

        except:
            print("Error in converting emojis")  # Basic Error Handling

    def CountSentimentOfEmojis(self, CleanTweetNoEmoji):
        """
        Count sentiment of Emojis by comparing emojis to the array of positive and negative emojis
        """
        global positiveCounter
        global negativeCounter
        positiveCounter = 0  # Sets the positive counter to 0
        negativeCounter = 0  # Sets the negative counter to 0

        CleanTweetNoEmoji = CleanTweetNoEmoji.replace(":",' ')
        CleanTweetNoEmoji = CleanTweetNoEmoji.replace("!",'')

        for word in CleanTweetNoEmoji.split():  # Splits the sentence to words
            if word in positiveEmojiList:  # Checks for emojis in the positive emoji list
                positiveCounter += 1  # Adds 1 if emoji present in the positive emoji list

            elif word in negativeEmojiList:  # Checks for emojis in the negative emoji list
                negativeCounter += 1  # Adds 1 if emoji present in the negative emoji list

            else:
                pass

        return positiveCounter, negativeCounter  # Return positive and negative emoji counter

    def ClassifyWords(self, CleanTweet):
        global posWordCounter
        global negWordCounter

        posWordCounter = 0  # Sets the positive word counter to 0
        negWordCounter = 0  # Sets the negative word counter to 0

        PosFile = open("PositiveWords.txt").read()  # Reads the positive word files
        NegFile = open("NegativeWords.txt").read()  # Reads the negative word file

        nomarks = CleanTweet.replace('!', '')  # Removes exclatiom marks from tweets
        nomarks = nomarks.lower()  # Converts the text to lower, so no capitals as the word list are all lower case
        nomarks = nomarks.replace('.', '')  # Replaces full stops with spaces
        nomarks = nomarks.replace(':', '')  # Replaces colons with spaces

        word_counter = dict()  # Creates an empty dictionary

        try:
            for words in nomarks.split():  # Iterates through words in the tweet text
                if words in word_counter:
                    word_counter[words] += 1  # Adds 1 to diciontary for associted word if already present in dictionary
                else:
                    word_counter[words] = 1  # Sets the value of the key (Word) to 1.
            for words in nomarks.split(): # Splits the sentence into words
                if words in PosFile.splitlines():  # Checks if a word in the text is present in the positive file
                    if word_counter[words] > 1:# If the associated word is present in the text more than once
                        for k in WordWeighPositive: # Iterates through the WordWeighPositive
                            if k[words] in WordWeighPositive: # Checks if the word is in the list
                                posWordCounter += (word_counter[words] * WordWeighPositive.get(k[words])) # Multiply the occurence of the word by its special weighing
                                print(k[words]) # Print Statement
                                print(posWordCounter) # Print Statement
                            else:
                                posWordCounter += (word_counter[words] * 1.4)  # sets the positive counter to equal 1.4 * the value for the associated key word
                        print(word_counter[words], posWordCounter) # Print Statement
                        print(words) # Print Statement
                    else:
                        posWordCounter += 1  # If word present in positive file but not present more than once in the tweet, then add 1 to the positive word counter
                        print(words) # Print Statement
                    if words in negationWords and words+1 in PosFile.splitlines(): # checks if the first word is in the negation list and then checks if the next word is positive
                        negWordCounter += 1 # Adds 1 to the negative counter

                elif words in NegFile.splitlines():  # Checks if a word in the text is present in the negative file
                    if word_counter[words] > 1:  # If the associated word is present in the text more than once
                        for key in WordWeighNegative: # Iterates through the WordWeighNegative list
                            if key[words] in WordWeighNegative: # checks for the word in the list
                                negWordCounter += (word_counter[words] * WordWeighNegative.get(key[words])) # multiply the occurence of the word by its special weighing
                            else:
                                negWordCounter += (word_counter[words] * 1.4)  # sets the negative counter to equal 1.4 * the value for the associated key word
                        print(word_counter[words], negWordCounter)  # Print Statement
                        print(words) # Print Statement
                    else:
                        negWordCounter += 1  # If word present in negative file but not present more than once in the tweet, then add 1 to the positive word counter
                        print(words)
        except:
            print("Error")  # Basic Error Handling

        return posWordCounter, negWordCounter

    def FrequencyTables(self, CleanTweet):
        global OverallTotal
        positiveTweets = 0  # Sets the positve tweet counter to 0
        negativeTweets = 0  # Sets the negative tweet counter to 0

        CleanTweet = CleanTweet.replace(":",'')
        CleanTweet = CleanTweet.replace("!",'')
        CleanTweet = CleanTweet.replace("@rt",'')

        TotalPos = posWordCounter + positiveCounter  # Adds the positive word counter and positve emoji counter together
        TotalNeg = negWordCounter + negativeCounter  # Adds the negative word counter and negative emoji counter together
        OverallTotal = (TotalPos - TotalNeg) / (
            len(CleanTweet.split()))  # Subtract negative counter from positive counter and divides result
        OverallTotalToPlot.append(
            OverallTotal)  # Appends Results to array which would be used to plot sentiment of tweets in the main graph

        if OverallTotal > 0:
            print("Positive Tweet", OverallTotal)
            try:
                positive_tweets[CleanTweet] = OverallTotal  # Appends the tweet and sets the value to sentiment result
                print(positive_tweets)  # Prints out the positive value to user on the python console
            except:
                print("error")  # Basic Error handling
        elif OverallTotal < 0:
            print("Negative Tweet", OverallTotal)
            try:
                negative_tweets[CleanTweet] = OverallTotal  # Append the tweet and sets the value to sentiment result
                print(negative_tweets)  # Prints out the negative value to user on the python console

            except:
                print("error")  # Basic Error Handling

        else:
            print(
                "Neutral")  # Prints out neutral for any other tweet that is not classified in the If statements above.

        return positiveTweets, negativeTweets, OverallTotal  # Return Variables

    def Main(self):

        search = Cursor(
            self.api.search, q=('#' + str(query)), lang='en', count=10)
        # Search Method for Twitter API. Uses the user entry for the query
        # Sets the parameters of the search method; Language = english, Count of retweets = 10

        global counterOfTweets
        counterOfTweets = 0  # Sets the counter of tweets to 0
        TotalPosTweets = 0  # Sets the positive tweet counter to 0
        TotalNegTweets = 0  # Sets the neutral tweets counter to 0
        TotalNeuTweets = 0  # Sets the negatuve tweets counter to 0

        try:
            for tweet in search.items(20):  # Iterates through 20 pulled tweets
                counterOfTweets += 1  # Adds 1 to the parsed tweets
                CleanTweet = self.Remove_URL(tweet)  # Calls on Remove URL function
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)  # Calls on Identify Emoji function
                CountEmoji = self.CountSentimentOfEmojis(
                    CleanTweetNoEmoji)  # Calls on classification of emojis function
                classifyWords = self.ClassifyWords(CleanTweet)  # Calls on classify word function
                countNumbers = self.FrequencyTables(CleanTweet)  # Calls on Sentiment calculator

                print("noEmoji:", counterOfTweets, CleanTweet,
                      CleanTweetNoEmoji, CountEmoji, classifyWords,
                      countNumbers)
                if OverallTotal > 0:  # If the Overall value of sentiment is bigger than 0
                    TotalPosTweets += 1  # Add 1 to the positve tweet counter

                elif OverallTotal < 0:  # If Overall value of sentiment is bigger than 0
                    TotalNegTweets += 1  # Add 1 to the negative tweet counter

                else:
                    TotalNeuTweets += 1  # Add 1 to neutral tweet counter

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
                print(
                    "Hence , Positive")  # If the pverall sentiment is bigger than 0, then overall sentiment of 20 parsed tweets is positive
            elif OverallSentiment < 0:
                print(
                    "Hence, Negative")  # If the overall sentiment is smaller than 0, then overall sentiment of 20 parsed tweets is negative
            else:
                print("Hence, Neutral")  # Prints Neutral if overall sentiment not classified in the IF statments above.

        except error.TweepError as e:
            print(e.reason)  # Prints Error of Twitter Search method to the user
            print("error")  # Basic Error Handling


class Stock(object):

    def __init__(self):
        """
        Access the Quandl Databse via API keys
        """
        quandl.ApiConfig.api_key = Quandl_API
        self.Twitter = Twitter()
        self.StockData()  # Calls on StockData Function

    def StockData(self):
        """
            Pulls Stock Data via the Quandl API
        """
        try:
            print(stockentry)  # Print Statement showing user entry; done for compeltion purposes
            global Data
            data = quandl.get('EOD/' + str(stockentry),
                              rows=7)  # Retrieves the last 7 days end of day prices for the user selected company
            print(data)
            Data = data

            return Data

        except:
            pass  # Basic Error Handling


class Window(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)  # initiate the Frame of the window
        self.master = master
        self.Stock = Stock()
        self.Twitter = Twitter()
        self.main_window()

    def main_window(self):
        self.master.title("Main")  # Sets the title of the page as main.
        self.master.configure(
            background='snow', highlightbackground='light steel blue')  # Sets the background color of the page

        self.Twitter.Trends()  # Calls on the twitter trend function by referral statment

        self.canvas = Canvas(self.master, width=670, height=450)  # Initiate the canvas size
        self.canvas.grid(row=0, column=0, sticky='nsew')  # Places the canvas at row 0 and column 0

        self.line = self.canvas.create_rectangle(
            329, -10, 332, 450, fill='light blue')
        # Seprates the Main window - Left=Stock Right=Twitter Query

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
        # Choices of Tickers; Company Name Abbreviations
        self.var.set(self.Choice[0])  # Displays the first ticker as the pre-set
        self.w = OptionMenu(self.master, self.var,
                            *self.Choice)
        # Creates the drop-down menu
        self.ButtonT = Button(
            self.master,
            text="Enter",
            font=("Avenir", 14),
            command=self.CompanyEntry)
        # Creates a buttton to retrive user selection

        # ==== Placement of widgets ====#
        self.LabelT.place(x=360, y=100)
        self.w.place(x=360, y=130)
        self.ButtonT.place(x=360, y=170)
        self.LabelTQ.place(x=30, y=100)
        self.EntryTQ.place(x=30, y=130)
        self.ButtonTQ.place(x=30, y=170)
        # ==============================#

        # ============ Creates text Labels ============#
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
        # ============================================#

        # === Places Labels on Screen ===#
        self.LabelTt.place(x=40, y=300)
        self.LabelTT.place(x=48, y=270)
        self.LabelSH.place(x=360, y=50)
        self.LabelGU.place(x=30, y=50)
        self.LabelWP.place(x=195, y=10)
        # ===============================#

        self.ButtonHP = Button(
            self.master,
            text="Help",
            font=("Avenir", 14),
            background='light sky blue',
            activebackground='light sky blue',
            command=self.GoToHelpPage)
        # Creates button to allow user to navigate to the help page #
        self.ButtonHP.place(x=600, y=10)  # Places button on the screen

    def CompanyEntry(self):
        """Retrives Entry of USER"""
        global stockentry
        try:
            self.ButtonVG = Button(
                self.master, text="View Graph", command=self.GoToStockPage)
            # Creates a button that redirects to a function in the class that calls on the stock page
            self.ButtonVG.place(x=350, y=350)  # Places the button on the screen

            self.LabelCP = Label(
                self.master,
                text="Loading...",
                font=("Avenir", 12),
                foreground='salmon')
            # Text Label
            self.LabelCP.place(x=350, y=320)  # Label placed on the screen
            stockentry = self.var.get()  # Retrives the user stock entry
            self.Stock.StockData()  # Calls on the class stock, to pull 'EOD' data using the query

        except:
            print("Error")  # Basic error handling

    def TwitterQueryEntry(self):
        try:
            global query
            query = self.EntryTQ.get()  # Retrives user twitter query
            print(query)
            self.Twitter.Main()  # Calls on the function main in the twitter class

        except:
            print("Error")  # Basic error handling

    def GoToHelpPage(self):
        # ==== Redirects user to help page ====#
        self.helppage = Toplevel(self.master)
        self.app = HelpPage(self.helppage)
        # =====================================#

    def GoToStockPage(self):
        # ==== Redirects user to stock page ====#
        self.stockpage = Toplevel(self.master)
        self.app = StockPage(self.stockpage)
        # ======================================#


class HelpPage(Frame):

    def __init__(self, master=None):
        # ===== Initiate help page =====#
        Frame.__init__(self, master)
        self.masters = master
        self.master.geometry("660x440")
        self.create_Help_Page()
        # ==============================#

    def create_Help_Page(self):
        self.masters.title("Help Page")  # Sets the title of the page to help page
        self.masters.configure(
            background='white', highlightbackground='light steel blue')
        # Sets the background of the help page to white
        self.canvashp = Canvas(self.masters, width=670, height=480)  # Creates a canvas
        self.canvashp.grid(row=0, column=0, sticky='nsew')  # Places the canvas at row 0 column 0
        self.rectangle_top = self.canvashp.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        # Creates a rectangle. Used to make the page more user appeling
        self.rectangle_bottom = self.canvashp.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')
        # Creates a rectangle. Used to make the page more user appeling
        # ================ Creates Text Labels =====================#
        self.LabelHp = Label(
            self.master,
            text="Help Page",
            font=("Avenir", 20),
            foreground='white',
            activebackground='light sky blue',
            background='light sky blue')
        self.LabelHP = Label(self.masters, text="Select an Option:")
        # ==========================================================#
        self.var = StringVar(self.masters)
        self.Choice = [
            "Help With Stock Graph", "Help with Twitter Query", "About"
        ]  # Creates choices user can select
        self.var.set(self.Choice[0])  # sets the first choice as a pre-set
        self.w = OptionMenu(self.masters, self.var,
                            *self.Choice)
        # Creates a drop-down menu
        self.buttonx = Button(
            self.masters, text="Enter", command=self.getEntry)
        # Creates a button that retrieves the user entry; calls on function getEntry
        # == Places Labels and buttons ==#
        self.LabelHp.place(x=280, y=10)
        self.LabelHP.place(x=39, y=100)
        self.w.place(x=30, y=130)
        self.buttonx.place(x=30, y=170)
        # ===============================#

    def getEntry(self):
        entry = self.var.get()  # Retrives user entry
        print(entry)
        if entry == "Help With Stock Graph":
            self.HelpStock()  # Redirects and calls on function help stock
        elif entry == "Help with Twitter Query":
            self.HelpTwitter()  # Redirects and calls on functiono help twittter
        else:
            self.About()

    def HelpStock(self):

        choice = ["AAPL", "MCD", "MSFT", "NKE", "INTC", "BA", "DIS"]  # choices of tickers
        Ticker_Names = [
            "Apple", "McDonalds", "Microsoft", "Nike", "Intel Coporation",
            "Boeing Company", "The Walt Disney Company"
        ]  # Creates an array with the associate names of the company

        Ticker_Name = dict()  # Creates an empty dictionary
        i = 0  # Sets variable i = 0
        for i in range(0, len(choice)):  # Iterates from 0 to the length of choice array
            Ticker_Name[choice[i]] = Ticker_Names[
                i]  # Appends the ticker name as a key with the comapny name as a value
            i += 1  # Adds 1 to variable i.

        PrettyTicker_Name = json.dumps(Ticker_Name,
                                       indent=2)  # Idents the dictionary using the module json, for a nicer display
        self.LabelHS = Label(
            self.masters,
            text=PrettyTicker_Name,
            font=("Avenir", 12),
            foreground='black',
            relief='groove')
        # Creates a label displaying the ticker names
        self.LabelHS.place(x=300, y=80)  # Displays the label on the screen

    def HelpTwitter(self):
        self.LabelHT = Label(
            self.masters,
            text=
            "Enter your Query and Hit Enter Button \n This query will used to pull Twitter Data from the Database",
            font=("Avenir", 12))
        # Creates a text label
        self.LabelHT.place(x=300, y=100)  # Places the label on the screen

    def About(self):
        pass


class StockPage(Frame):

    def __init__(self, master=None):
        # ==== Initiate stock page ====#
        Frame.__init__(self, master)
        self.mastersp = master
        self.master.geometry("660x440")
        self.Twitter = Twitter()
        self.GraphStock()
        # =============================#

    def GraphStock(self):
        self.mastersp.title("Tweet and Graph Page")  # Sets the title of the page
        print(OverallTotalToPlot)
        df = pd.DataFrame({'values': OverallTotalToPlot})  # Appends values of sentiment to a pandas dataframe
        self.canvashp = Canvas(self.mastersp, width=670, height=480)  # Creates a canvas
        self.canvashp.grid(row=0, column=0, sticky='nsew')  # Displays canvas at row = 0 and column =0
        self.rectangle_top = self.canvashp.create_rectangle(
            0, 0, 660, 45, fill='light sky blue', outline='light sky blue')
        # Creates a rectangle for a nicer GUI display
        self.rectangle_bottom = self.canvashp.create_rectangle(
            0, 405, 660, 440, fill='salmon', outline='salmon')
        # Creates a rectangle for a nicer GUI display
        # ================== Creates text labels ==================#
        self.Labelsp = Label(
            self.mastersp,
            text="Twiter Sentiment Page",
            font=("Avenir", 20),
            foreground='white',
            activebackground='light sky blue',
            background='light sky blue')
        self.LabelGO = Label(
            self.mastersp,
            text=("Overall Sentiment of Tweets:", OverallSentiment),
            font=("Avenir", 14),
            relief='groove')
        self.LabelWI = Label(
            self.mastersp,
            text=("Information About Indicators/Graph:"),
            font=("Avenir", 14))
        # ==========================================================#
        self.Labelsp.place(x=240, y=10)
        self.varc = StringVar(self.mastersp)
        self.Choices = ["Bollinger Bands", "Moving Average", "Candlestick"]  # Creates Choices
        self.varc.set(self.Choices[0])  # Sets the first chocie as a pre-set for display
        self.om = OptionMenu(self.mastersp, self.varc,
                             *self.Choices)  # Creates drop-down menu
        self.buttonx = Button(
            self.mastersp, text="Enter", command=self.GetEntryIndicator)
        # Create a button that retrieves user entry
        #==== Places label and Menu ====#
        self.Labelsp.place(x=240, y=10)
        self.LabelWI.place(x=20, y=50)
        self.om.place(x=20, y=80)
        self.buttonx.place(x=20, y=100)
        self.LabelGO.place(x=20, y=140)
        # ==============================#
        print("YES", positive_tweets)
        print("No,", negative_tweets)

        self.canvashp.create_rectangle(10, 200,650, 400, outline='black', fill='white')  # creates a rectangle
        self.canvashp.update()  # Updates the canvas

        positive_tweets_lines = json.dumps(positive_tweets,indent=2) # Indents the positive tweets with lines for a better display
        self.LabelPT = Label(self.mastersp,text=positive_tweets_lines,font=("Avenir",6),foreground='SpringGreen3') # Creates the text label
        self.LabelPT.place(x=50,y=270) # Places the label on the frame

        negative_tweets_lines = json.dumps(negative_tweets,indent=2) # Indents the negative tweets with lines for a better display
        self.labelNT = Label(self.mastersp,text=negative_tweets_lines,font=("Avenir",6),foreground='tomato') # Creates the text label
        self.labelNT.place(x=50,y=205) # Places the text label

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

        fig = plt.figure(figsize=(9, 9)) # Initiate figure size
        fig.suptitle(stockentry + ' STOCK DATA', fontsize=12) # Creates a title to be plotted on the figure

        ax = plt.subplot2grid((2, 2), (0, 0), colspan=4, rowspan=1) # Adds a subplot to the figure
        Data['Date'] = Data.index.map(mdates.date2num)  # Converts dates to number format, to allow for it to be plotted
        plt.plot(Data['Close'], Label="Close", color="yellow") # Plots closing price; Adds a label on the line, and sets the color of the line to yellow
        plt.plot(Data['MA50'], label="Moving Average", color="blue") # Plots the moving average; Adds a label for the line, and sets the color of the line to blue
        plt.plot(Data['UpBB'], Label="Upper Bollinger Band", color="black") # Plots the upper bollinger band; sets the label and sets the color of the line
        plt.plot(Data['LowBB'], Label="Lower Bollinger Band", color="grey") # Plots the lower bollinger band; sets the label and sets the color of the line
        plt.xlabel("Date") # Places x-axis label of Date
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d')) # Formats he axis to months and days
        plt.legend(loc='best') # Places the key in the best location on the graph
        ax.set_ylabel('Value') # Assigns the y label to Value

        Data['Date'] = Data.index.map(mdates.date2num) # Converts the dates to number format to allow for it to be plotted
        candlestickData = Data[['Date', 'Open', 'High', 'Low', 'Close']] # Creates and array full of the data needed to generate a candlestick graph
        candlestick_ohlc(
            ax, # Plots the candlestick graph on the main ax
            candlestickData.values, # uses the candlestick data and extract the values of each column
            width=.3, # Sets the width of the bars to 0.3
            colorup='green', # Sets the up colour of the bar to green
            colordown='red') # Sets the down colour of the bar tot red
        plt.xlabel("Date") # Sets the x-label as Date

        ax4 = fig.add_subplot(2, 2, 3) # Creates another subplot
        Data['Date'] = Data.index.map(mdates.date2num) # Converts the dates to number format to allow for it to be plotted
        ax4.plot(Data['Close'], label='Close Price') # Plots the closing price
        ax4.xaxis.set_major_formatter(mdates.DateFormatter('%d')) # formats the x-axis dates as days
        ax4.set_xlabel('Date') # Adds a x-axis label
        ax4.set_ylabel('Value') # Adds a y-axis label
        ax4.legend(loc='best') # Adds a key in the best location on the graph

        ax5 = fig.add_subplot(2, 2, 4) # Adds another subplot to the graph
        ax5.scatter(df, df['values'], label='Sentiment Value', color='blue') # scatters the tweet sentiment values
        cofficient = pearsonr((df['values'][0:7]), Data['Close']) # Creates the correlation coeffienct
        print("correlaction coefficient: ", str(cofficient))
        ax5.plot(
            cofficient,
            label='Pearson correlation coefficient', # Plots the correlation Coefficient
            color='magenta')
        ax5.set_xlabel('Tweet') # Adds an x-axis label
        ax5.legend(loc='best') # Adds the key to the best location on the subplot
        plt.show(ax) # Shows all of the graph

    def GetEntryIndicator(self):
        choice_entry = self.varc.get() # Get user entry from drop down menu
        if choice_entry == 'Bollinger Bands': # Checks if the choice is bolliger bands
            self.LabelBB = Label(
                self.mastersp,
                text=
                (
                    "Bollinger Bands: \nWhen the market is volatile, the bands widen.\n When the market is under a less volatile period, the bands contract."
                    ),
                font=("Avenir", 10)) # Creates a text label
            self.LabelBB.place(x=200, y=50)

        elif choice_entry == 'Moving Average':
            self.LabelMA = Label(
                self.mastersp,
                text=("Moving Average is calculated by..."),
                font=("Avenir", 10)) # Creates a text label
            self.LabelMA.place(x=200, y=100) # Plots a text label

        else:
            self.LabelCS = Label(
                self.mastersp,
                text=("Candlestick Graph is generated by..."),
                font=("Avenir", 10)) # Creates a text label
            self.LabelCS.place(x=200, y=150) # Plots a text label


root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop() # Runs the tkinter main window where the program starts from.