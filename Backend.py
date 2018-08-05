from tweepy import *
import quandl
import re,emoji
import nltk
import pandas as pd



consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'
class Twitter(object):

    def __init__(self):
        self.auth = OAuthHandler(consumer_key,consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        api = API(self.auth)
        self.api = api
        self.PullTwitterData(api)



    def PullTwitterData(self,api):
        parsed_tweets = []
        try:
            for tweet in Cursor(self.api.search,q='#Apple',lang='en', count=10).items(10):
                parsed_tweets.append(tweet.text)

            self.Remove_URL(parsed_tweets)


        except error.TweepError as e:
            print(e.reason)


    def Remove_URL(self,parsed_tweets):
        Removed_URL_Data = []
        try:
            for i in range(0,len(parsed_tweets)):
                ft = parsed_tweets[i].split()
                ftl = re.sub(r'http\S+', '', str(ft))       #Removing URL links from Data
                Removed_URL_Data.append(ftl)
                i += 1

            print(Removed_URL_Data)
            self.TokenizeWords(Removed_URL_Data)

        except:
            print("Error")


    def TokenizeWords(self,Removed_URL_Data):
        Tokens = []
        try:
            for i in range(0,len(Removed_URL_Data)):
                token = nltk.word_tokenize(Removed_URL_Data[i])
                Tokens.append(token)
                i += 1

            print(Tokens)

            self.CreatePandasFrame(Tokens)

        except:
            pass

    def CreatePandasFrame(self,Tokens):
        self.df = pd.DataFrame(data=Tokens)
        print(self.df.head())

        ############FIX PROBLEM############




Twitter()