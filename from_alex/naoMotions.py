import os
import sys
import random
import time

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior

BASEPATH="/home/nao/behaviors/"

import animacyStrings as anim

#____________________________________________________________

class Gesture:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.stiffness = 1.0

        self.frame = None
        self.speechDevice = None
        self.motion = None
        self.posture = None
        self.led = None
        self.win = anim.win
        self.lose = anim.lose
        self.draw = anim.draw
        self.curse = anim.curse
        self.hi = anim.hi
        self.meet = anim.meet
        self.standing =anim.standing
        self.ready = anim.ready
        self.bye =anim.bye
        self.connectNao()
    #initialize all nao devices____________________________________________________________
    def connectNao(self):
        #FRAME MANAGER FOR CALLING BEHAVIORS
        try:
            self.frame  = ALProxy("ALFrameManager", self.host, self.port)
        except Exception, e:
            print "Error when creating frame manager device proxy:"+str(e)
            exit(1)
        #POSTURE MANAGER#
        try:
            self.posture = postureProxy = ALProxy("ALRobotPosture", self.host, self.port)
        except Exception, e:
            print "Error creating posture proxy"+str(e)
            exit(1)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.motion = ALProxy("ALMotion", self.host, self.port)
        except Exception, e:
            print "Error when creating motion device proxy:"+str(e)
            exit(1)

        #MAKE NAO STIFF (OTHERWISE IT WON'T MOVE)
        self.motion.stiffnessInterpolation("Body",self.stiffness,1.0)

        #MOTION DEVICE FOR MOVEMENTS
        try:
            self.led = ALProxy("ALLeds", self.host, self.port)
        except Exception, e:
            print "Error when creating led proxy:"+str(e)
            exit(1)

        #CONNECT TO A SPEECH PROXY
        try:
            self.speechDevice = ALProxy("ALTextToSpeech", self.host, self.port)
        except Exception, e:
            print "Error when creating speech device proxy:"+str(e)
            exit(1)

    #SAY A SENTENCE___________________________________________________________________________________
    def genSpeech(self, sentence):
        try:
            self.speechDevice.post.say(sentence)
        except Exception, e:
            print "Error when saying a sentence: "+str(e)

    #____________________________________________________________
    def send_command(self, doBehavior):
        gesture_path = BASEPATH + doBehavior
        gesture_id   = self.frame.newBehaviorFromFile(gesture_path, "")
        self.frame.playBehavior(gesture_id)
        self.frame.completeBehavior(gesture_id)

    def goodbye(self):
        self.genSpeech(anim.finish)
        time.sleep(5)
        self.posture.goToPosture("SitRelax", 1.0)

    #____________________________________________________________

    def demo(self):
        self.posture.goToPosture("Stand", 1.0)
        self.led.fadeListRGB("FaceLeds",[0x00FFFFFF],[0.1])

        #self.genSpeech("Hello! My name is Nao.")
        #self.send_command("wave.xar")
        self.posture.goToPosture("Stand", 1.0)

        self.genSpeech("I am excited to play rock paper scissors with you. Let me demonstrate the gestures that I can make")
        time.sleep(8)

        #INITIALIZE POSITION OF THE HAND
        self.genSpeech("Let me show you how I do rock")
        self.rock()
        self.genSpeech("This is my rock gesture")
        time.sleep(3)

        self.genSpeech("Let me show you how I do paper")
        self.paper()
        self.genSpeech("This is my paper gesture")
        time.sleep(3)

        self.genSpeech("Let me show you how I do scissors")
        self.scissors()
        self.genSpeech("This is my scissors gesture")
        time.sleep(3)

    def rock(self):
        self.prepareThrow(self.rockShoot)

    def rockShoot(self):
        self.motion.setAngles("RWristYaw",0.3,0.6)
        if (self.motion.getAngles("RHand",False)[0]>0.5):
            self.motion.closeHand("RHand")
        else:
            time.sleep(0.3)

    def paper(self):
        self.prepareThrow(self.paperShoot)

    def paperShoot(self):
        self.motion.setAngles("RWristYaw",-1.2,1.0)
        if (self.motion.getAngles("RHand",False)[0]<0.5):
            self.motion.openHand("RHand")

    def scissors(self):
        self.prepareThrow(self.scissorsShoot)

    def scissorsShoot(self):
        self.motion.setAngles("RWristYaw",0.3,0.6)
        if (self.motion.getAngles("RHand",True)[0]<0.5):
            self.motion.openHand("RHand")

    def prepareThrow(self,shootFunc):
        angleTopShoulder = 0.2
        angleBotShoulder = 0.6

        angleTopElbow = 1.4
        angleBotElbow = 0.4
        wristYaw = 0.3

        self.motion.setAngles("RShoulderPitch",angleBotShoulder,0.2)
        time.sleep(1)

        phrases = ["Rock", "Paper", "Scissors", "SHOOT!"]

        self.motion.setAngles("RWristYaw",wristYaw,0.6)
        self.motion.closeHand("RHand")
        for i in range(4):
            self.motion.setAngles("RShoulderPitch",angleTopShoulder,0.1)
            self.motion.setAngles("RElbowRoll",angleTopElbow,0.3)
            time.sleep(0.8)
            self.motion.setAngles("RShoulderPitch",angleBotShoulder,0.1)
            self.motion.setAngles("RElbowRoll",angleBotElbow,0.3)
            if i==3:
                shootFunc()
                self.genSpeech(phrases[i])
            else:
                time.sleep(0.4)
                self.genSpeech(phrases[i])
            time.sleep(0.6)

    def prepareThrow2(self,shootFunc):
        angleTop = -0.5

        angleBot = 0.8
        wristYaw = 0.3

        self.motion.setAngles("RShoulderPitch",angleBot,0.2)
        time.sleep(1)

        phrases = ["Rock", "Paper", "Scissors", "SHOOT!"]

        self.motion.setAngles("RWristYaw",wristYaw,0.6)
        self.motion.closeHand("RHand")
        for i in range(4):
            self.motion.setAngles("RShoulderPitch",angleTop,0.5)
            time.sleep(0.5)
            self.genSpeech(phrases[i])
            self.motion.setAngles("RShoulderPitch",angleBot,0.5)
            if i==3:shootFunc()
            time.sleep(0.4)

    def move(self,move,prepare=True):
        if prepare:
            if move=="r": self.rock()
            if move=="p": self.paper()
            if move=="s": self.scissors()
        else:
            if move=="r": self.rockShoot()
            if move=="p": self.paperShoot()
            if move=="s": self.scissorsShoot()

    def cheat(self, move):
        self.move(move,False)

    def play(self, move):
        self.genSpeech("Lets play")
        time.sleep(1)

        #choose default one of the bahviors
        self.move(move)
        time.sleep(1)

    def announce(self, what):
        if(what is "win"): # NAO WON
            randnr = random.randint(0,len(self.win)-1)
            self.genSpeech(self.win[randnr])
            time.sleep(1)
        elif(what is "lose"): # NAO LOST
            randnr = random.randint(0,len(self.lose)-1)
            self.genSpeech(self.lose[randnr])
            time.sleep(1)
        elif(what is "draw"): # DRAW
            randnr = random.randint(0,len(self.draw)-1)
            self.genSpeech(self.draw[randnr])
            time.sleep(1)
        elif(what is "curse"): #CURSE
            print("in curse")
            randnr = random.randint(0,len(self.curse)-1)
            self.genSpeech(self.curse[randnr])
            time.sleep(1)

    def sayhi(self):
        self.motion.setStiffnesses("Body", 1.0)
        headYawHi = -0.7
        headYaw = 0.0
        self.motion.setAngles("HeadYaw", headYawHi, 0.1)
        time.sleep(1)
        self.genSpeech(self.hi)

    def saymeet(self):
        self.genSpeech(self.meet)

    def saystanding(self):
        self.genSpeech(self.standing)

    def sayready(self):
        self.genSpeech(self.ready)

    def saybye(self):
        self.motion.setStiffnesses("Body", 1.0)
        headYawHi = -0.6
        headYaw = 0.0
        self.motion.setAngles("HeadYaw", headYawHi, 0.1)
        time.sleep(1)
        self.genSpeech(self.bye)
        time.sleep(1)
        self.motion.setAngles("HeadYaw", headYaw, 0.2)
        #self.motion.setStiffnesses("Body", 0.0)

    # RELEASE THE JOINTS SO IT WON'T COMPLAIN
    def releaseNao(self):
        try:
            self.posture.goToPosture("SitRelax", 1.0)
            self.motion.stiffnessInterpolation("Body",0.0,self.stiffness)
        except Exception, e:
            print "Error when sitting down nao and making nao unstiff: "+str(e)
#____________________________________________________________
