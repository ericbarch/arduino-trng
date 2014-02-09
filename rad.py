#!/usr/bin/env python

import time
import httplib, urllib
import RPi.GPIO as GPIO

waitUntil = time.time() + 1
events = []

def upload():
    cpm = str(float(len(events))/float(5))
    params = urllib.urlencode({'field1': cpm})
    headers = {
	"X-THINGSPEAKAPIKEY": "YOUR-CHANNEL-KEY",
	"Content-Type": "application/x-www-form-urlencoded",
	"Content-Length": str(len(params))
    }
    conn = httplib.HTTPConnection("api.thingspeak.com")
    conn.request("POST", "/update", params, headers)
    response = conn.getresponse()
    if response.status == 200:
        print 'upload'
    else:
	print 'upload fail'
    data = response.read()
    conn.close()


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

    # wait 5 mins before posting to thingspeak (data needs to stabilize)
    loops = -270

    # sleepy time
    while True:
        time.sleep(1)
	for event in events:
		if event < time.time() - 300:
			events.remove(event)
	print "cpm: " + str(float(len(events))/float(5))
	loops = loops + 1
	if (loops > 30):
		loops = 0
		upload()

    # done
    GPIO.cleanup()


# start 'er up
if __name__=="__main__":
    main()
