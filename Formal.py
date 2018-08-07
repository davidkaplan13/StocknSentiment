from tweepy import *
import re
import emoji

consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'


class Twitter(object):

    def __init__(self):
        self.auth = OAuthHandler(consumer_key,consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = API(self.auth)
        self.MainLoop()


    def Remove_URL(self,tweet):
        Remove_URL = []
        try:
            noUrl = re.sub(r'http\S+', '',str(tweet.text))
            Remove_URL.append(noUrl)
            self.Emoji(Remove_URL)

        except:
            print("Error")

    def Emoji(self,Remove_URL):
        s = []
        try:
            for i in range(0,len(Remove_URL)):
                d = emoji.demojize(Remove_URL[i])     #Converting Emoji to description
                s.append(d)
                i += 1

            self.CategroiseWords(s)


        except:
            print("Error in converting emojis")


    def CategroiseWords(self,s):
        pass

    def MainLoop(self):

        search = Cursor(self.api.search,q='Drake',lang='en',count=20)
        try:
            for tweet in search.items(20):
                self.Remove_URL(tweet)


        except error.TweepError as e:
            print(e.reason)
            print("error")



Twitter()

