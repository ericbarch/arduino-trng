#!/usr/bin/env python

import time
import RPi.GPIO as GPIO

waitUntil = time.time() + 1
events = []

def radiationEventHandler (pin):
    if time.time() >= waitUntil:
        events.append(time.time())

def noiseEventHandler (pin):
    waitUntil = time.time() + 1
    for event in events:
	current_time = time.time()
	if event >= (current_time - 1) and event <= current_time:
	    try:
		events.remove(event)
            except:
		pass


# main function
def main():
    # tell the GPIO module that we want to use 
    # the chip's pin numbering scheme
    GPIO.setmode(GPIO.BCM)

    GPIO.setup(17, GPIO.IN)
    GPIO.setup(17, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(18, GPIO.IN)
    GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    GPIO.add_event_detect(17, GPIO.FALLING)
    GPIO.add_event_callback(17, radiationEventHandler)

    GPIO.add_event_detect(18, GPIO.FALLING)
    GPIO.add_event_callback(18, noiseEventHandler)

    # sleepy time
    while True:
        time.sleep(1)
	for event in events:
		if event < time.time() - 300:
			events.remove(event)
	print "cpm: " + str(float(len(events))/float(5))

    # done
    GPIO.cleanup()


# start 'er up
if __name__=="__main__":
    main()
