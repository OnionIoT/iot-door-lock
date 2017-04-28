# for use with the IoT Door Lock project
# script is in cgi-bin by default

from subprocess import call

# lock or unlock the door
def setLock(status):
    # script to call
    baseCommand = ["sh", "/www/cgi-bin/door.sh"]
    
    # determine the arguments to send
    if status == "lock":
        baseCommand.append("lock")
    elif status == "unlock":
        baseCommand.append("unlock")
    # if no valid arguments, do nothing
    elif status == "toggle":
        pass   # call the script without any commands to briefly open and close the lock
    else:
        print "Invalid lock command!"
        return False
        
    # call the command
    # print baseCommand
    call(baseCommand)
    
    return