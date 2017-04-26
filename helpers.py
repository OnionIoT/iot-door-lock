import json
import twitterHelper as twitter
import doorHelper as door
import configHelper

def stripHashtagSymbols(hashtags):
    for hashtag in hashtags:
        hashtag["text"] = hashtag["text"].replace("#", "")
    
def controlDoorViaTwitter(consumerCredentials, accessCredentials, userId, hashtags):
    # initialize and authenticate this twitter app
    app = twitter.TwitterApp(consumerCredentials, accessCredentials)
    commands = {
        "lock": hashtags["lock"],
        "unlock": hashtags["unlock"]
    }
    
    # set up stream callback overrides
    # when a status is received from the targeted user with the correct hashtag
    def on_status(self, status):
        print json.dumps(status)
        
        # sort the hashtags in order of appearance, just in case they're not
        orderedHashtags = twitter.sortHashTags(status, "appearance")
        
        # check hashtags for commands
        for hashtag in orderedHashtags:
            # prioritize locking
            if hashtag["text"] == commands["lock"]:
                # door.setLock("lock")
                print "I should lock the door now!"
                return
            else if hashtag["text"] == commands["unlock"]:
                # door.setLock("unlock")
                print "I should unlock the door now!"
                return
        
        # no valid hashtag was found
        print "No valid hashtag was found."
        return
    
    # overrides to extend StreamListener
    callbacks = {
        "on_status": on_status
    }
    # filter a twitter stream from the specified user and hashtag
    # operate the door
    app.filterStream("follow", [userId], callbacks)