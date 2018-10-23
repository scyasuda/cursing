import os
import sys
import random
import time
import collections

import naoqi
from naoqi import ALBroker
from naoqi import ALModule
from naoqi import ALProxy
from naoqi import ALBehavior

from naoMotions import *
from gameLogic import *

#from play_curse import playCurse

def log_move(data_file,number,human_choice,robot_choice,cheat_move=""):
    data_file.write("%d,%s,%s,%s\n"%(number,human_choice.replace("\n","").replace("\r",""),robot_choice,cheat_move))
    data_file.flush()

def playCurse(data_file):
    """Have the nao play in a cursing mode
    """

    cheating_start_round = 2
    cheating_last_round = 4

    i = 0
    total_throws = 5
    cheats_remaining = 1 #number of times the robot still needs to cheat
    extend = 0 #number of rounds to extend the cheating section for

    while True:
        if i == (total_throws + extend): break

        nao_choice=throw_sequence[i]
        goNao.play(nao_choice)

        #get user input
        val = False
        while not val:
            human_choice = raw_input("Throw %d - human chose (r,p,s): "%(i+1))
            val = validated(human_choice)

        #did Nao win?
        winStr = naoWon(nao_choice,human_choice) #returns "win","lose","draw"

        ###should the nao cheat?###
        #is the nao on the right throw to want to cheat?
        if i>=cheating_start_round and i<=(cheating_last_round+extend) and cheats_remaining>0:
            #does the nao want to cheat 2 up and does it have the opportunity to?
            if winStr=="lose":
                winStr = "curse"
                cheats_remaining-=1
        #get nao to announce it
        goNao.announce(winStr)

        #LOG DATA
        #log_move(data_file,i+1,human_choice,nao_choice,move_to_cheat)
        if (i>=cheating_last_round and cheats_remaining>1): extend+=1
        i += 1

    goNao.goodbye()

def playNoCheat(data_file):

    for i in range(30):
        nao_choice=throw_sequence[i]
        goNao.play(nao_choice)

        #get user input
        val = False
        while not val:
            human_choice = raw_input("Throw %d - human chose (r,p,s): "%(i+1))
            val = validated(human_choice)

        #LOG DATA
        log_move(data_file,i+1,human_choice,nao_choice)

        #did Nao win?
        winStr = naoWon(nao_choice,human_choice)

        #get nao to announce it
        goNao.announce(winStr)

    goNao.goodbye()

def playCheat(cheat_type,data_file):
    """Have the nao play in a cheating mode

    cheat_type is either "win", "draw" or "lose"
    """

    cheating_start_round = 10
    cheating_last_round = 19

    i = 0
    total_throws = 30
    cheats_remaining = 2 #number of times the robot still needs to cheat
    extend = 0 #number of rounds to extend the cheating section for

    while True:
        if i == (total_throws + extend): break

        nao_choice=throw_sequence[i]
        goNao.play(nao_choice)

        #get user input
        val = False
        while not val:
            human_choice = raw_input("Throw %d - human chose (r,p,s): "%(i+1))
            val = validated(human_choice)


        #did Nao win?
        winStr = naoWon(nao_choice,human_choice)

        ###should the now cheat?###

        #is the nao on the right throw to want to cheat?
        if i>=cheating_start_round and i<=(cheating_last_round+extend):

            #does the nao want to cheat 2 up and does it have the opportunity to?
            if cheat_type=="2u" and winStr=="lose":
                #yes, nao wants to cheat 2 up, and it can
                move_to_cheat=choiceThatBeats(human_choice)
                winStr = "win"
                goNao.cheat(move_to_cheat)
                cheats_remaining-=1

            #does the nao want to cheat 2 down and does it have the opportunity to?
            if cheat_type=="2d" and winStr=="win":
                #yes, nao wants to cheat 2 down, and it can
                move_to_cheat=choiceThatLosesTo(human_choice)
                winStr = "lose"
                goNao.cheat(move_to_cheat)
                cheats_remaining-=1

            #does the nao want to cheat 1 up and does it have the opportunity to?
            if cheat_type=="1u" and winStr=="lose":
                #yes, nao wants to cheat 1 up, and it can
                move_to_cheat=choiceThatDraws(human_choice)
                winStr = "draw"
                goNao.cheat(move_to_cheat)
                cheats_remaining-=1

            #does the nao want to cheat 1 down and does it have the opportunity to?
            if cheat_type=="1d" and winStr=="win":
                #yes, nao wants to cheat 1 down, and it can
                move_to_cheat=choiceThatDraws(human_choice)
                winStr = "draw"
                goNao.cheat(move_to_cheat)
                cheats_remaining-=1



            ######THIS IS WHERE ADDITIONAL CASE LOGIC SHOULD GO######

            #####

        #get nao to announce it
        goNao.announce(winStr)

        #LOG DATA
        #log_move(data_file,i+1,human_choice,nao_choice,move_to_cheat)

        if (i>=cheating_last_round and cheats_remaining>1): extend+=1

        i += 1

    goNao.goodbye()

#Get the Nao's IP
ipAdd = None
try:
    ipFile = open("ip.txt")
    ipAdd = ipFile.readline().replace("\n","").replace("\r","")
except Exception as e:
    print "Could not open file ip.txt"
    ipAdd = raw_input("Please write Nao's IP address... ")

#Try to connect to it
goNao = None
try:
    goNao = Gesture(ipAdd, 9559)
except Exception as e:
    print "Could not find nao. Check that your ip is correct (ip.txt)"
    sys.exit()

#Set postureProxy
try:
    postureProxy = ALProxy("ALRobotPosture", ipAdd, 9559)
except Exception, e:
    print "Could not create proxy to ALRobotPosture"
    print "Error was: ", e

#Choose an action
#Set all the possible commands
commands=collections.OrderedDict((("d","Run the demonstration of Nao's gestures during the play"),
("t","Test some new functionality"),
("r","Release motors"),
("pnc","Play, no cheating"),
("pc2u","Play, cheat two up (robot moves two up)"),
("pc2d","Play, cheat two down (robot moves two down)"),
("pc1u","Play, cheat to tie one up (from a losing position)"),
("pc1d","Play, cheat to tie one down (from a winning position)"),
("pcurse","Play, cursing"),
))

#Output all the commands
print "\nPlease choose an action:"
for key,value in commands.items():
    print("\t%s => %s"%(key,value))

#Have the user select the choice
choice = ""
if choice not in commands:
    choice = raw_input('Choice: ').replace("\n","").replace("\r","")

#Execute the user's choice
if(choice == "d"):
    postureProxy.goToPosture("Stand", 1.0)
    goNao.demo()

elif(choice=="r"):
    goNao.releaseNao()

elif(choice=="t"):
    goNao.announce("curse")
    goNao.releaseNao()

elif(choice[0] == "p"):
    participant_name = raw_input('Input participant\'s name: ').replace("\n","").replace("\r","")
    data_file = open("data/%s.txt"%participant_name,"w")
    data_file.write("%s\n"%participant_name)
    data_file.write("%s\n"%choice)
    data_file.write("------------\n")
    data_file.flush()

    #goNao.demo()

    postureProxy.goToPosture("Sit", 1.0)

    #Play 30 rounds of rock paper scissors
    if(choice=="pnc"): playNoCheat(data_file)
    if(choice=="pc2u"): playCheat("2u",data_file)
    if(choice=="pc2d"): playCheat("2d",data_file)
    if(choice=="pc1u"): playCheat("1u",data_file)
    if(choice=="pc1d"): playCheat("1d",data_file)
    if(choice=="pcurse"): playCurse(data_file)

    postureProxy.goToPosture("SitRelax", 1.0)

    goNao.releaseNao()

    data_file.close()

#______________________________________________________________________________
