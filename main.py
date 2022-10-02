from BirdBrain import Finch
import time
import random

# init
bird = Finch()

def countdown(num):
    for i in range(num, 0, -1):
        time.sleep(1)
        print(str(i) + "...")

# get threshold
print("Place on white surface...")
countdown(6)
white = (bird.getLine('L') + bird.getLine('R')) / 2
print("Place on black surface...")
countdown(6)
black = (bird.getLine('L') + bird.getLine('R')) / 2
threshold = (white + black) / 2
print("Threshold:", threshold)
print("Place on track now...")
countdown(6)

# start movin'
fs = 3 # full speed
bird.setMotors(fs, fs)

# functions
def avoidObstacle():
    bird.setTurn('L', 45, fs) # turn 45* left
    bird.setMove('F', 30, fs) # move 30 cm forward
    bird.setTurn('R', 45, fs) # turn 45* right
    bird.setMove('F', 20, fs) # move 30 cm forward

def rv():
    # This function returns a "random value" from 0-100
    # The name is short on purpose because it needs to be called so many times
    return random.randrange(101)

def randomLights():
    bird.setBeak(rv(), rv(), rv())
    for i in range(1, 5):
        bird.setTail(i, rv(), rv(), rv())

# program
while not bird.getButton("A"): # stop if 'A' is pressed

    # checking for obstacle
    if bird.getDistance() < 15:
        bird.stop() # stop motors
        bird.setBeak(100, 0, 0) # turn beak red
        bird.setTail("all", 100, 0, 0) # turn tail red
        bird.playNote(30, 1)
        avoidObstacle()
        bird.playNote(60, 3)
        break
    
    randomLights()
       
    # line tracking
    if bird.getLine('R') < threshold and bird.getLine('L') < threshold: # if at a fork in the road
        bird.setMotors(0, fs) # turn left
    elif bird.getLine('R') < threshold:
        bird.setMotors(fs, 0) # turn right
    elif bird.getLine('L') < threshold:
        bird.setMotors(0, fs) # turn left
    else:
        bird.setMotors(fs, fs) # go straight

time.sleep(1)
bird.stopAll() # turn everything off after 1s
