# tweepy method
import tweepy

# streaming from scratch
# stream listener
class StreamListener(tweepy.StreamListener):
    # had trouble with extending __init__() using super()
    # so call this function immediately after instantiating
    def initOverrides(self):
        self.__overrides = {
            "on_connect": None,
            "on_data": None,
            "on_status": None,
            "on_error": None,
        }
        
    # add an override for one of the event types above.
    # callback should take the same arguments as the StreamListener methods
    # except for the self argument
    def setEventOverride(self, eventType, callback):
        overrideType = "on_" + eventType
        if overrideType in self.__overrides:
            self.__overrides[overrideType] = callback
    
    # overrides
    # when a new tweet is received
    def on_status(self, status):
        if self.__overrides["on_status"] is not None:
            self.__overrides["on_status"](status)
        else:
            return
    
    # when a non-200 status code is returned
    def on_error(self, statusCode):
        if self.__overrides["on_error"] is not None:
            self.__overrides["on_error"](statusCode)
        else:
            return False
    # extend with more if necessary
        
# main twitter handler class
class TwitterApp(object):
    # initialization
    def __init__(self, consumerCredentials, accessCredentials):
        # authenticate
        self.authenticateApp(consumerCredentials, accessCredentials)
        
    # authenticate this app    
    def authenticateApp(self, consumerCredentials, accessCredentials):
        auth = tweepy.OAuthHandler(consumerCredentials["consumerKey"], consumerCredentials["consumerSecret"])
        auth.set_access_token(accessCredentials["accessToken"], accessCredentials["accessTokenSecret"])
        self.api = tweepy.API(auth)
    
    # get numeric user id that is required by some of the tweepy APIs
    def getUserId(self, screenname):
        user = self.api.get_user(screenname)
        if user is not None:
            return user.id_str
        return None
    
    # filter a twitter stream
    # provide a filter type, corresponding criteria, and a listener with callbacks setup
    def filterStream(self, listener, filterType, filterCriteria):
        # setup a stream and pass it the listener from the caller
        stream = tweepy.Stream(auth=self.api.auth, listener=listener)
        
        # filter the stream
        # update with more parameters available, see https://github.com/tweepy/tweepy/blob/master/tweepy/streaming.py
        if filterType == 'follow':
            stream.filter(follow=filterCriteria)
        elif filterType == 'track':
            stream.filter(track=filterCriteria)
        
# helper functions for processing tweets
# sort hashtags
def sortHashTags(tweet, order):
    if order == "appearance":
        return sorted(tweet.entities["hashtags"], key=lambda x: x["indices"][0])
    # add more types of sorting later
    
    else:
        return None