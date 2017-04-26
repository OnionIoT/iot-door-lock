import helpers
import configHelper
config = configHelper.readConfig()

import json
print json.dumps(config)

# strip any at signs and pound signs that users may have entered in the config file
config["userId"] = helpers.stripAtSigns(config["userId"])
config["hashtags"] = helpers.stripConfigHashtags(config["hashtags"])

# main function
def __main__():
    print "Cleaned userId and hashtags:"
    print json.dumps(config["userId"])
    print json.dumps(config["hashtags"])
    
    print "Checking for tweets."
    # begin checking tweets
    helpers.controlDoorViaTwitter(
        config["consumerCredentials"],
        config["accessCredentials"],
        config["userId"],
        config["hashtags"]
    )
    
    # runs forever
    
    
if __name__ == '__main__':
    __main__()