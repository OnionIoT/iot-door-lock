import helpers

import json
# print json.dumps(config)

# main function
def __main__():
    # import raw config
    config = helpers.config
    
    # initialize twitter app and API connection
    twitterApp = helpers.twitter.TwitterApp(config["consumerCredentials"], config["accessCredentials"])
    
    # process the config file
    # need access to Twitter API to resolve usernames to numeric user ids
    processedConfig = helpers.processTwitterConfig(twitterApp, config)
    
    
    print "Checking for tweets."
    # begin checking tweets
    helpers.controlDoor(twitterApp, processedConfig["allowedUsers"], processedConfig["hashtags"])
    
    # runs forever

if __name__ == '__main__':
    __main__()