#!/usr/in/env python

import os, random
import RPi.GPIO as GPIO
import time
import subprocess 
from threading import Thread

# Pin Definitions

#startButton = 23 # Pi pin 12
#goToNextTrack = 23 # Pi pin 16


# Which numbering system?
GPIO.setmode(GPIO.BCM) # THIS IS BROADCOM NUBMERING SYSTEM

# declare pin mode
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def rndmp3():
	print "play button pressed"
	randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
	#randomfile2 = random.choice(os.listdir("/home/pi/robotPA/pa/"))
	file1 =' /home/pi/vacuumHold/music/'+randomfile1
	#file2 = ' /home/pi/robotPA/pa/' +randomfile2
	os.system('aplay' + ' -N ' + ' -D allmono  '+ file1 + ' &')
	#os.system('aplay' + ' -D allmono '+ file2)

def rndmp3_main():
	print "loop play"
	randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
	file1 =' /home/pi/vacuumHold/music/'+randomfile1
	os.system('aplay' + ' -N ' + ' -D allmono '+ file1 )

def killallplay():
	print "stop previous track and play next"
	subprocess.call(['killall', 'aplay'])

class loopmp3:
	def __init__(self):
		self._running = True

	def terminate(self):
		self._running = False
		killallplay()

	def run(self):
		while self._running:
			rndmp3_main()

loopSound = loopmp3()
loopSoundThread = Thread(target=loopSound.run)
loopSoundThread.start()


def buttonpressed(channel):
	if GPIO.input(23):
		loopSound.terminate()
		print "Rising Edge Detected"
		loopSound.run()
	else:		
		print "Falling Edge detected on 18"
		loopSound.terminate()
		loopSound.run()

GPIO.add_event_detect(23, GPIO.BOTH, callback=buttonpressed, bouncetime=200)


# MAIN
print "script start"

try:
	while True:
		time.sleep(0.1)

except KeyboardInterrupt:
	GPIO.cleanup()

print "script end"


