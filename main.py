from tweepy import *
from tkinter import *



consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

Quandl_API = "9AK1N1LNy7PzHefyRR9w"


class Twitter(object):
    """Twitter Data"""

    def __init__(self):
        self.Auth = OAuthHandler(consumer_key, consumer_secret)
        self.Auth.set_access_token(access_token, access_token_secret)
        api = API(self.Auth)
        self.api = api

        print("Yep", api)
        self.PullData(api)

    def PullData(self,api):
        for tweet in Cursor(api.search, q='#Donald Trump', count=10,lang="en", since_id=2018 - 7 - 30).items():
            print(tweet.created_at, tweet.text)

Twitter()

class Window(Frame):

    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master= master
        self.create_window()

    def create_window(self):
        self.master.title("Main")
        self.pack(fill=BOTH,expand=1)
        self.buttonN = Button(self.master,text='Twitter Data',width=25,command=self.new_window)
        self.buttonN.place(height=100)

    def new_window(self):
        self.nWindow = Toplevel(self.master)
        self.app = TweetPage(self.nWindow)


class TweetPage(Frame):
    def __init__(self,master=None):
        Frame.__init__(self,master)
        self.master = master
        self.create_mainWindow()

    def create_mainWindow(self):
        self.master.title("Twitter Page")

root = Tk()
root.geometry("660x440")
app = Window(root)
root.mainloop()

