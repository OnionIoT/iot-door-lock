# tweepy method
import tweepy

# streaming from scratch
class TwitterApp(object):
    # extend the stream listener class
    # provide a dict of callbacks to extend
    # they must be object methods, so don't forget to include self as the first argument!
    class StreamListener(tweepy.StreamListener):
        def __init__(self, callbacks):
            for name, callback in callbacks.iteritems():
                self[name] = callback
            return
            
    # initialization
    def __init__(self, consumerCredentials, accessCredentials):
        self.authenticateApp(consumerCredentials, accessCredentials)
        
    # authenticate this app    
    def authenticateApp(self, consumerCredentials, accessCredentials):
        self.auth = tweepy.OAuthHandler(consumerCredentials.consumerKey, consumerCredentials.consumerSecret)
        self.auth.set_access_token(accessCredentials.accessToken, accessCredentials.accessTokenSecret)
    
    # filter a twitter stream
    # provide a filter type, criteria, and the callbacks for the stream listener
    def filterStream(self, filterType, filterCriteria, callbacks):
        streamListener = StreamListener(callbacks)
        stream = tweepy.Stream(auth=self.api.auth, listener=streamListener)
        
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
        return sorted(tweet.entities.hashtags, key=lambda x: x["indices"][0])
    # add more types of sorting later
    
    else:
        return None