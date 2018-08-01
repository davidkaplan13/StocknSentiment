from tweepy import *
from tkinter import *
import re
import emoji
import quandl


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
            for tweet in Cursor(api.search, q='#Apple', count=10,lang="en", since_id=2018 - 7 - 30).items(10):
                parsed_tweets.append(tweet.text)
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

Twitter()

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

        self.buttonL = Button(self.master,text='Twitter Data',fg='light steel blue',bg='light steel blue')
        self.buttonL.place(x=240,y=280,width=150)

        self.buttonM = Button(self.master,text='View Graphs',fg='light steel blue',bg='light steel blue')
        self.buttonM.place(x=240,y=320,width=150)

    def new_window(self):
        """Calls on for a new page"""
        self.nWindow = Toplevel(self.master)
        self.app = StockPage(self.nWindow)

class StockPage(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.create_twitterWindow()
        self.master.geometry("660x440")

    def create_twitterWindow(self):
        self.master.title("Stock Page")
        self.master.configure(background='linen')

        self.LabelT = Label(self.master,text="Enter Company name in ticker format:",font=("Calibri",12))
        self.EntryT = Entry(self.master)
        self.ButtonT = Button(self.master,text="Enter",command=self.CompanyEntry)
        self.LabelT.place(x=50,y=100)
        self.EntryT.place(x=50,y=120)
        self.ButtonT.place(x=50,y=180)


    def CompanyEntry(self):
        try:
            x = self.EntryT.get()
            print(x)
            with open("Stock.txt",'w') as company: #Writes x over Stock.txt file which is read bu the Stock Class
                company.write(x)
        except:
            print("Unable to create Stock.txt File")


root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()

class Stock(object):

    def __init__(self):
        """Accessing Quandl API"""
        quandl.ApiConfig.api_key = Quandl_API
        self.PullStockData()


    def PullStockData(self):
        """Pulling Stock Data"""
        try:
            with open("Stock.txt",'r') as read_company:
                y = read_company.read()
                stock = quandl.get("WIKI/" + str(y), rows=5)
                print(str(stock))

        except:
            print("Unable to read Stock.txt")
            
Stock()
