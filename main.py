import helpers
import configHelper
config = configHelper.readConfig()
# strip any pound signs that users may have entered in the config file
config.hashtags = helpers.stripHashtagSymbols(config.hashtags)


def __main__():
    # begin checking tweets
    helpers.controlDoorViaTwitter(
        config.consumerCredentials,
        config.accessCredentials,
        config.userId,
        config.hashtags
    )
    
    
if __name__ == '__main__':
    __main__()