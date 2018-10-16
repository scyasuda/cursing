#!/usr/bin/env python
import almath
import time
from naoqi import ALProxy

robotIP = "192.168.1.140"
PORT=9559
#
def main(robotIP, PORT=9559):

    motion  = ALProxy("ALMotion", robotIP, PORT)
    posture = ALProxy("ALRobotPosture", robotIP, PORT)
    tts = ALProxy("ALTextToSpeech", robotIP, PORT)

    # Wake up robot
    motion.wakeUp()

    # Send robot to Sit Init
    posture.goToPosture("Sit", 0.5)

    #tts.say("Would you like to play a game with me?")
    #Allow motion
    motion.setStiffnesses("Body", 1.0)
    names = ["RWristYaw", "RShoulderPitch", "RShoulderRoll", "RElbowRoll"]
    angles = [90.0*almath.TO_RAD, 0.0*almath.TO_RAD,50.0*almath.TO_RAD, 0.0*almath.TO_RAD]
    fractionMaxSpeed= 0.5
    motion.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(1.0)
    #motion.setStiffnesses("Body", 0)
    tts.say("Rock")
    names = ["RShoulderPitch", "RElbowRoll"]
    angles = [-30*almath.TO_RAD, 10.0*almath.TO_RAD]
    fractionMaxSpeed= 0.6
    motion.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(0.5)
    names = ["RShoulderPitch"]
    angles = [30*almath.TO_RAD]
    fractionMaxSpeed= 0.6
    motion.setAngles(names, angles, fractionMaxSpeed)
    time.sleep(1.0)

    # motion = ALProxy("ALMotion", "nao.local", 9559)

# def scissors:
#     motion.setStiffnesses("Body", 1.0)
#     names = "LWristYaw"
#     angles = 50.0*almath.TO_RAD
#     fractionMaxSpeed= 0.1
#     motion.setAngles(names, angles, fractionMaxSpeed)
#     time.sleep(1.0)
#     motion.setStiffnesses("Body", 0)

main(robotIP, PORT)
