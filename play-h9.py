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

# def rndmp3():
# 	print "play button pressed"
# 	randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
# 	#randomfile2 = random.choice(os.listdir("/home/pi/robotPA/pa/"))
# 	file1 =' /home/pi/vacuumHold/music/'+randomfile1
# 	#file2 = ' /home/pi/robotPA/pa/' +randomfile2
# 	os.system('aplay' + ' -N ' + ' -D allmono  '+ file1 + ' &')
# 	#os.system('aplay' + ' -D allmono '+ file2)

# def rndmp3_main():
# 	print "loop play"
# 	randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
# 	file1 =' /home/pi/vacuumHold/music/'+randomfile1
# 	os.system('aplay' + ' -N ' + ' -D allmono '+ file1 )

def pick_random_mp3():
  randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
  print("Selecting {} for play".format(randomfile1))
	file1 =' /home/pi/vacuumHold/music/' + randomfile1
  return file1

def play_mp3(filename):
  print("Playing {}".format(filename))
	os.system('aplay' + ' -N ' + ' -D allmono '+ filename)

def kill_all_aplay():
	print("Killing all aplay processes...")
	subprocess.call(['killall', 'aplay'])

# class loopmp3:
# 	def __init__(self):
# 		self._running = True

# 	def terminate(self):
# 		self._running = False
# 		killallplay()
    
#   def restart(self):
#     self._running = True

# 	def run(self):
# 		while self._running:
# 			rndmp3_main()

# loopSound = loopmp3()
# loopSoundThread = Thread(target=loopSound.run)
# loopSoundThread.start()

def run_audio_thread(filename):
  audio_thread = Thread(target=play_mp3, args=(filename,))
  audio_thread.start()
  return audio_thread

# def buttonpressed(channel):
# 	if GPIO.input(23):
#     # should this instead terminate the running thread and spawn a new thread?
# 		killallplay()
# 		print "Rising Edge Detected"
#     loopSoundThread = Thread(target=loopSound.run)
#     loopSoundThread.start()
#   else:		
# 		print "Falling Edge detected on 18"
# 		killallplay()
#     # you need to make a new thread here
#     # loopSoundThread = Thread(target=your_function)
#     loopSoundThread = Thread(target=loopSound.run)
#     loopSoundThread.start()

# GPIO.add_event_detect(23, GPIO.BOTH, callback=buttonpressed, bouncetime=200)

# MAIN
print "script start"

try:
  GPIO.add_event_detect(23, GPIO.BOTH, bouncetime=200)
  
  filename = pick_random_mp3()
  at = run_audio_thread(filename)
  
  while True:
    if GPIO.event_detected(23):
      kill_all_aplay()
  		filename = pick_random_mp3()
      
    if not at.is_alive():
      # loop it
      at = run_audio_thread(filename)
      at.start()      
      
except KeyboardInterrupt:
	GPIO.cleanup()

print "script end"
