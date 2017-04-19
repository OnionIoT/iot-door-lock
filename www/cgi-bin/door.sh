#!/bin/sh
# set the relay channel
CHANNEL=0

# relayState 	lockState
#	OFF			locked		(0)
#	ON			unlocked	(1)
LOCKED=0
UNLOCKED=1


if [ "$1" == "lock" ]
then
	relay-exp -q $CHANNEL $LOCKED
elif [ "$1" == "unlock" ]
then
	relay-exp -q $CHANNEL $UNLOCKED
else
	# find the current value of the lock
	relayStateRaw=$(relay-exp read $CHANNEL)
	relayStateOff=$(echo $relayStateRaw | grep OFF)

	if [ "$relayStateOff" == "" ]
	then
		# already unlocked
		initialState=1 #unlocked
	else
		relay-exp -q $CHANNEL $UNLOCKED
		sleep 5
		relay-exp -q $CHANNEL $LOCKED
	fi
fi
