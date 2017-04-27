# for use with the IoT Door Lock project
# script is in cgi-bin by default

from subprocess import call

# lock or unlock the door
def setLock(status):
    # script to call
    baseCommand = ["sh", "/www/cgi-bin/door.sh"]
    
    # determine the arguments to send
    if status == True:
        baseCommand.append("lock")
    elif status == False:
        baseCommand.append("unlock")
    # if no valid arguments, do nothing
    else:
        print "Invalid lock command!"
        return False
    # call the command
    # call(baseCommand)
    print baseCommand
    return