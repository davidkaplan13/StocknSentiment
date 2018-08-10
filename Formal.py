from tweepy import *
import re
import emoji

consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

global positiveEmojiList
global negativeEmojiList

positiveEmojiList =[':smile:',':simple_smile:',':laughing:',':blush:',
                    ':smiley:',':relaxed:',':heart_eyes:',':grin:',
                    ':grinning:',':kissing:',':sweat_smile:',':joy:',':satisfied:',':crown:']

negativeEmojiList = [':worried:',':frowning:',':anguished:',':grimacing:',
                     ':disappointed_relieved:',':unamused:',':fearful:',':sob:',
                     ':cry:',':angry:',':rage:',':frowning:',]

class Twitter(object):

    def __init__(self):
        self.auth = OAuthHandler(consumer_key,consumer_secret)
        self.auth.set_access_token(access_token,access_token_secret)
        self.api = API(self.auth)
        self.MainLoop()


    def Remove_URL(self,tweet):

        try:
            noUrl = re.sub(r'http\S+','',str(tweet.text))
            return noUrl

        except:
            print("Error")

    def IdentifyEmoji(self,CleanTweet):

        try:
            noEmoji = emoji.demojize(CleanTweet)
            return noEmoji

        except:
            print("Error in converting emojis")


    def CountSentimentOfEmojis(self,CleanTweetNoEmoji):

        positiveCounter = 0
        negativeCounter = 0

        for word in CleanTweetNoEmoji.split():
            if word in positiveEmojiList:
                positiveCounter += 1

            elif word in negativeEmojiList:
                negativeCounter += 1

            else:
                pass

        return positiveCounter,negativeCounter

    def MainLoop(self):

        search = Cursor(self.api.search,q='apple',lang='en',count=20)
        counterOfTweets=0

        try:
            for tweet in search.items(2):
                counterOfTweets+=1
                #print(counterOfTweets,tweet.text)

                CleanTweet = self.Remove_URL(tweet)
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)
                CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji)

                print("noEmoji:",CleanTweetNoEmoji,CountEmoji)


        except error.TweepError as e:
            print(e.reason)
            print("error")



Twitter()

