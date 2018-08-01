from tweepy import *
from tkinter import *
import re ,emoji
import quandl
import time


#Twitter API Keys
consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

#Quandl API key
Quandl_API = "9AK1N1LNy7PzHefyRR9w"


class Twitter(object):

    def __init__(self):
        """Accessing Twitter Database"""
        self.Auth = OAuthHandler(consumer_key, consumer_secret)
        self.Auth.set_access_token(access_token, access_token_secret)
        api = API(self.Auth)
        self.api = api
        self.PullData(api)

    def PullData(self,api):
        """Pulling Data from Twitter"""
        parsed_tweets = []
        try:
            with open("TwitterSearch.txt",'r') as twitter:      #Resolve Issue
                y = twitter.read()
                self.PullData()

        except:
            print("Error")

        try:
            for tweet in Cursor(api.search,q=('#'+str(y)),count=10,lang="en", since_id=2018 - 7 - 30).items(10):
                print(parsed_tweets.append(tweet.text))

            self.Remove_URL(parsed_tweets)

        except error.TweepError as e:
            print("Sorry, The following Occured",e.reason)

    def Remove_URL(self,parsed_tweets):
        """Data Preparation on Parsed Tweets"""
        Removed_URL_Data = []
        try:
            for i in range(0,len(parsed_tweets)):
                ft = parsed_tweets[i].split()
                ftl = re.sub(r'http\S+', '', str(ft))       #Removing URL links from Data
                Removed_URL_Data.append(ftl)
                i += 1

            self.ClassifyEmoticons(Removed_URL_Data)

        except:
            print("Error")

    def ClassifyEmoticons(self,Removed_URL_Data):
        """Classifying Emoticons on pre-processed data"""
        s = []
        try:
            for i in range(0,len(Removed_URL_Data)):
                d = emoji.demojize(Removed_URL_Data[i])     #Converting Emoji to description
                s.append(d)
                i += 1

            print(Removed_URL_Data,s)

        except:
            print("Error in converting emojis")


class Stock(object):
    def __init__(self):
        """Accessing Quandl API"""
        quandl.ApiConfig.api_key = Quandl_API
        self.PullStockData()

    def PullStockData(self):
        """Pulling Stock Data"""
        try:
            with open("Stock.txt", 'r') as read_company:
                y = read_company.read()
                stock = quandl.get("WIKI/"+str(y),rows=5)

            self.DisplayStockData(stock)

        except:
            print("Unable to read Stock.txt")

    def DisplayStockData(self,stock):
        """Writes Pulled Stock Data into a File which is read by DisplayStockFigures()"""
        with open("StockData.txt", 'w') as append_stock:
            append_stock.write(str(stock))


class Window(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master= master
        self.Main_window()

    def Main_window(self):
        """Creating The Main Window Widgets"""
        self.master.title("Main")
        self.master.configure(background='light steel blue',highlightbackground='light steel blue')

        self.welcome = Label(self.master,text="Welcome \n Stock/Sentiment Analysis Program",font=("Calibri",16))
        self.welcome.place(x=175,y=50)

        self.buttonN = Button(self.master,text='Stock Data',fg='light steel blue',bg="light steel blue",command=self.new_window)
        self.buttonN.place(x=240,y=240,width=150)

        self.buttonL = Button(self.master,text='Twitter Data',fg='light steel blue',bg='light steel blue',command=self.tWindow)
        self.buttonL.place(x=240,y=280,width=150)

        self.buttonM = Button(self.master,text='View Graphs',fg='light steel blue',bg='light steel blue',command=self.ViewWindow)
        self.buttonM.place(x=240,y=320,width=150)

    def tWindow(self):
        self.twitterWindow = Toplevel(self.master)
        self.app = TwitterPage(self.twitterWindow)

    def ViewWindow(self):
        self.vWindow = Toplevel(self.master)
        self.app = ViewGraphs(self.vWindow)

    def new_window(self):
        """Calls on for a new page"""
        self.nWindow = Toplevel(self.master)
        self.app = StockPage(self.nWindow)

class StockPage(Frame):
    """Stock Page"""

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.create_twitterWindow()
        self.master.geometry("660x440")
        self.stock = Stock()

    def create_twitterWindow(self):
        self.master.title("Stock Page")
        self.master.configure(background='linen')

        self.LabelT = Label(self.master,text="Select Company:",font=("Calibri",12))
        self.var = StringVar(self.master)

        self.Choice = [
            "AAPL",
            "AMZN",
            "MSFT"
        ]
        self.var.set(self.Choice[0])
        self.w = OptionMenu(self.master,self.var,*self.Choice)      #Drop Down Menu
        self.ButtonT = Button(self.master,text="Enter",command=self.CompanyEntry)

        self.LabelT.place(x=30,y=100)
        self.w.place(x=30,y=120)
        self.ButtonT.place(x=30,y=170)


    def CompanyEntry(self):
        """Retrives Entry of USER and calls on Pull Stock Data from Class Stock"""
        try:
            x = self.var.get()
            print(x)
            with open("Stock.txt",'w') as company:  #Writes x over Stock.txt file which is read by the Stock Class
                company.write(x)

            self.stock.PullStockData()
            time.sleep(5)                           #Allows time for DisplayStockData() to run
            self.DisplayStockFigures()

        except:
            print("Unable to create Stock.txt File")

    def DisplayStockFigures(self):
        with open("StockData.txt", 'r') as read_stock:
            x = read_stock.read()

        self.LabelS = Label(self.master,text=x,font=("Calibri",10),bg="linen",borderwidth=3,relief="groove")
        self.LabelS.place(x=170,y=100)


class ViewGraphs(Frame):
    """View Graphs for Stock and Sentiment"""
    def __init__(self,master=None):
        Frame.__init__(self, master)
        self.master = master
        self.master.geometry("660x440")
        self.ViewGraphWindow()

    def ViewGraphWindow(self):
        self.master.title("View Graphs")
        self.master.configure(background='white smoke')

class TwitterPage(Frame):
    """Twitter Page"""
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.master.geometry("660x440")
        self.twittersearch = Twitter()
        self.MainTwitterPage()


    def MainTwitterPage(self):
        self.master.title("Twitter Page")
        self.master.configure(background='floral white')

        self.twitterLabel = Label(self.master,text="Twitter Query", font=("Calibri",14),bg='floral white',borderwidth = 2,relief = 'groove')
        self.twitterEntry = Entry(self.master,borderwidth=2,relief='groove')
        self.twitterButton = Button(self.master,text="Submit",command=self.GetEntry)
        self.twitterLabel.place(x=50,y=100)
        self.twitterEntry.place(x=50,y=125)
        self.twitterButton.place(x=50,y=160)

    def GetEntry(self):
        try:
            m = self.twitterEntry.get()
            with open("TwitterSearch.txt",'w') as submit:   #Resolve Issue
                submit.write(m)

            time.sleep(10)
            self.twittersearch.PullData()

        except:
            print("Errors")

root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()