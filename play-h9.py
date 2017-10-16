#!/usr/in/env python

import os, random
import RPi.GPIO as GPIO
import time
import subprocess

# Pin Definitions
CHANNEL = 23

# Which numbering system?
GPIO.setmode(GPIO.BCM) # THIS IS BROADCOM NUBMERING SYSTEM

# declare pin mode
GPIO.setup(CHANNEL, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def pick_random_mp3():
    randomfile1 = random.choice(os.listdir("/home/pi/vacuumHold/music/"))
    print("Selecting {} for play".format(randomfile1))
    file1 =' /home/pi/vacuumHold/music/' + randomfile1
    return file1

def play_mp3(filename):
    print("Playing {}".format(filename))
    aplay_args = ['aplay', '-N', '-D allmono', filename]
    p = subprocess.Popen(aplay_args)
    return p

def kill_all_aplay():
    print("Killing all aplay processes...")
    subprocess.call(['killall', 'aplay'])

# def run_audio_thread(filename):
#     audio_thread = Thread(target=play_mp3, args=(filename,))
#     audio_thread.start()
#     return audio_thread

# MAIN
print "script start"

try:
    GPIO.add_event_detect(CHANNEL, GPIO.BOTH, bouncetime=200)
    
    filename = pick_random_mp3()
    proc = play_mp3(filename)
    
    while True:
        if GPIO.event_detected(CHANNEL):
            proc.terminate()
            filename = pick_random_mp3()
            
        if proc.poll() is not None:
            # process has finished, restart it
            proc = play_mp3(filename)
            
except KeyboardInterrupt:
    GPIO.cleanup()

print "script end"
