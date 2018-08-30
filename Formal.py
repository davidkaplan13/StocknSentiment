from tweepy import *
import re
import emoji
import statistics
import math

consumer_key = 'kgfbFJJwwp3I2gHyT1ibNVvPJ'
consumer_secret = 'AoNjgNDvRn528ZnMG1funqEXeTZ760ZX7JGAmAgkKskrkzWNVp'
access_token = '1017368312081154048-MQnLaHAveFccgzDlHBXyiwWBSSWSXc'
access_token_secret = 'i2x3zhDRqgEAjyuP9puLBMLR0bLDje63rPeDIqDi1J1lY'

global positiveEmojiList
global negativeEmojiList

positiveEmojiList =[':smile:',':simple_smile:',':laughing:',':blush:',
                    ':smiley:',':relaxed:',':heart_eyes:',':grin:',
                    ':grinning:',':kissing:',':sweat_smile:',':joy:',
                    ':satisfied:',':crown:','face_with_tears_of_joy',':fire:',':money_bag:',':dollar_banknote:',':glowing_star:']

negativeEmojiList = [':worried:',':frowning:',':anguished:',':grimacing:',
                     ':disappointed_relieved:',':unamused:',':fearful:',':sob:',
                     ':cry:',':angry:',':rage:',':frowning:',':man_shrugging:',':face_screaming_in_fear:']
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

        return positiveCounter,negativeCounter

    def ClassifyWords(self,CleanTweet):
        """Needs Fixing"""
        global posWordCounter
        global negWordCounter
        posWordCounter = 0
        negWordCounter = 0

        PosFile = open("PositiveWords.txt")     #PositiveWord List extracted from : http://ptrckprry.com/course/ssd/data/positive-words.txt
        NegFile = open("NegativeWords.txt")

        wordlist = []
        try:
            for words in CleanTweet.split():
                wordlist.append(words.lower())

            for i in range(0,len(wordlist)):
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


        return posWordCounter,negWordCounter

    def FrequencyTables(self,CleanTweet):

        positiveTweets = 0
        negativeTweets = 0

        TotalPos = posWordCounter+positiveCounter
        TotalNeg = negWordCounter+negativeCounter
        OverallTotal = (TotalPos - TotalNeg)/(len(CleanTweet.split()))

        if OverallTotal > 0:
            print("Positive Tweet",OverallTotal)
        elif OverallTotal < 0:
            print("Negative Tweet",OverallTotal)
        else:
            print("Neutral")


        return positiveTweets,negativeTweets

    def FindCorrelation(self):

        t = ((statistics.mean(x) - statistics.mean(y))/(math.sqrt((statistics.stdev(x)^2/N))+(statistics.stdev(y)^2/n)))
        ##Student T-test - x - Sample 1, y-Sample 2 , N is sample 1, n is sample 2


    def MainLoop(self):

        search = Cursor(self.api.search,q='#westbrook',lang='en',count=20)
        counterOfTweets=0

        try:
            for tweet in search.items(7):
                counterOfTweets+=1
                CleanTweet = self.Remove_URL(tweet)
                CleanTweetNoEmoji = self.IdentifyEmoji(CleanTweet)
                CountEmoji = self.CountSentimentOfEmojis(CleanTweetNoEmoji)
                classifyWords = self.ClassifyWords(CleanTweet)
                countNumbers = self.FrequencyTables(CleanTweet)

                print("noEmoji:",counterOfTweets,CleanTweetNoEmoji,CountEmoji,classifyWords,countNumbers)


        except error.TweepError as e:
            print(e.reason)
            print("error")



Twitter()

