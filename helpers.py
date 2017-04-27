import json
import twitterHelper as twitter
import doorHelper as door
import configHelper

# remove @ signs from the allowed users config
def stripAtSigns(allowedUsers):
    ret = []
    for user in allowedUsers:
        ret.append(user.replace("@",""))
    return ret

# remove any # signs from hashtags in config
def stripConfigHashtags(hashtags):
    ret = {}
    for hashtag, value in hashtags.iteritems():
        ret[hashtag] = value.replace("#", "")
    return ret

# set up stream callback overrides
# when a status is received from the targeted user with the correct hashtag
def on_status(status):
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
        elif hashtag["text"] == commands["unlock"]:
            # door.setLock("unlock")
            print "I should unlock the door now!"
            return
    
    # no valid hashtag was found
    print "No valid hashtag was found."
    return

# non-200 responses
def on_error(status_code):
    if status_code == 420:
        print "Status code 420. Disconnecting and reconnecting backoff strategy"
        return False

# the meat and potatoes
def controlDoorViaTwitter(consumerCredentials, accessCredentials, allowedUsers, hashtags):
    # initialize stream listener
    print "initializing listener"
    listener = twitter.StreamListener()
    # initialize and authenticate this twitter app
    print "initializing app"
    app = twitter.TwitterApp(consumerCredentials, accessCredentials)
    
    
    # hashtags for opening the door
    commands = {
        "lock": hashtags["lock"],
        "unlock": hashtags["unlock"]
    }
    
    # overrides to extend StreamListener
    print "adding overrides"
    listener.setEventOverride("status", on_status)
    listener.setEventOverride("error", on_error)
    
    # filter a twitter stream from the specified user and hashtag
    # operate the door
    print "filtering stream"
    app.filterStream(listener, "follow", allowedUsers)