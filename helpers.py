import json
import twitterHelper as twitter
import doorHelper as door
import configHelper

# load the config
config = configHelper.readConfig()

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

# get numeric user ids given a list of usernames
# user id is required for filter(follow="userid")
def getUserIds(app, users):
    userIdList = []
    for user in users:
        userIdList.append(app.getUserId(user))
        
    return userIdList

# process the config file
def processTwitterConfig(app, config):
    processed = config
    # strip @ signs
    # convert to user id (numeric format)
    processed["allowedUsers"] = stripAtSigns(config["allowedUsers"])
    processed["allowedUsers"] = getUserIds(app, config["allowedUsers"])
    # remove # symbols
    processed["hashtags"] = stripConfigHashtags(config["hashtags"])
    
    return processed

# the meat and potatoes
def controlDoor(twitterApp, allowedUsers, hashtags):
    # initialize stream listener
    listener = twitter.StreamListener()
    listener.initOverrides()  
    
    # set up stream callback overrides
    # when a status is received from the targeted user with the correct hashtag
    def on_status(status):
        # print the json of the tweet - debug only
        # print json.dumps(status._json)
        
        # sort the hashtags in order of appearance, just in case they're not
        orderedHashtags = twitter.sortHashTags(status, "appearance")
        
        # check hashtags for commands
        for hashtag in orderedHashtags:
            # prioritize locking
            if hashtag["text"] == hashtags["lock"]:
                door.setLock("lock")
                return
            elif hashtag["text"] == hashtags["unlock"]:
                door.setLock("unlock")
                return
            elif hashtag["text"] == hashtags["toggle"]:
                door.setLock("toggle")
                return
        
        # no valid hashtag was found
        return

    # non-200 responses
    def on_error(status_code):
        if status_code == 420:
            print "Status code " + status_code + ". Disconnecting and reconnecting using backoff strategy."
            return False
    
    # overrides to extend StreamListener
    listener.setEventOverride("status", on_status)
    listener.setEventOverride("error", on_error)
    
    # filter a twitter stream from the specified user and hashtag
    twitterApp.filterStream(listener, "follow", allowedUsers)