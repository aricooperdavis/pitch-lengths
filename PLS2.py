#! /usr/bin/env python

import csv
import sys
import numpy as np
from array import array

usage_string = """usage: .\PLS2.py [<pitchFile>] command

The first given argument should be your csv file. Default 'pitchFile.csv':
    
The following given arguments should be your desired command:
    reqRope     returns min rope needed for every cave without joining ropes
    totCave     returns the number of caves to be evaluated
    noJoinN     returns the number of caves possible without joining ropes
    noJoinL     returns a list of the caves possible without joining ropes
    yesJoinN    returns the number of caves possible with joining ropes
    yesJoinL    returns a list of caves in which rope joining would be required
    
For example, a common usage might be:
    .\PLS2.py pitchFile.csv reqRope totCave"""

def readFile(pitchFileName):
    """reads the csv file and outputs it as a python array"""
    mA = []
    f = open(pitchFileName, 'rb') # opens the csv file
    try:
        reader = csv.reader(f)  # creates the reader object
        data = list(reader)
        for row in data:   # iterates the rows of the file in orders
                if row == []:
                    continue #do nothing
                elif row[0][0] == "#":
                    continue #do nothing
                mA.append(row)
            
    finally:
        f.close()      # closing
    return mA

def numArray(mA):
    """takes an array outputed by readFile and cuts out headers and pitch information, returning a new array and stats"""
    number_caves = len(mA)
    max_pitches = 0
    number_pitches = 0
    pA = []
    
    for i in range (0, number_caves): #determine number of pitches
        number_pitches += int(mA[i][1])
        pA.append(int(mA[i][1]))
        if mA[i][1] > max_pitches:
            max_pitches = mA[i][1]

    mnA = np.zeros([int(number_caves), int(max_pitches)])

    for i in range (0, number_caves):
        for j in range (0, int(max_pitches)):
            try:
                mnA[i][j] = mA[i][j+2]
                pass
            except IndexError:
                pass
    return mnA, number_caves, max_pitches, number_pitches, pA

def sortNumeric(mnA, number_caves, pA):
    """sorts a numeric array to return a sorted array (top left high, bottom right low) with stats"""
    smnA = np.array(mnA)
    for i in range (0, number_caves):
        smnA[i] = sorted(smnA[i], reverse=True)
        
    max_pitch_length = np.max(mnA)
    min_pitch_length = np.min(mnA[np.nonzero(mnA)])
    avg_pitch_length = np.mean(mnA[np.nonzero(mnA)])
    max_pitch_num = np.max(pA)
    min_pitch_num = np.min(pA)
    avg_pitch_num = np.mean(pA)
    
    smnA2 = np.array(smnA)
    
    for i in range (0, max_pitch_num):
        smnA[:, i] = sorted(smnA[:, i], reverse=True)
        
    return max_pitch_length, min_pitch_length, avg_pitch_length, max_pitch_num, min_pitch_num, avg_pitch_num, smnA, smnA2

def ropeCheck(given_rope, halfSortedArray, max_pitches):
    """given a rope combination this checks the number of caves that can be done with it"""
    given_rope = sorted(given_rope, reverse=True)
    
    for i in range (0, int(max_pitches)):
        try:
            given_rope[i] = given_rope[i]
            pass
        except IndexError:
            given_rope.append(0)
            pass
    
    caves_accessible = 0
    which_caves_var = []
    
    for i in range (0, np.shape(halfSortedArray)[0]):
        caveFlag = 0
        for j in range (0, np.shape(halfSortedArray)[1]):
            if given_rope[j] >= halfSortedArray[i][j]:
                caveFlag += 1
        if caveFlag == np.shape(halfSortedArray)[1]:
            caves_accessible += 1
            which_caves_var.append(i+1)
    
    return caves_accessible, which_caves_var

def nameCaves(which_caves_var, masterArray):
    which_caves = []
    if type(which_caves_var) is not list:
        which_caves_var = which_caves_var.astype(int)
    for i in range (0, len(which_caves_var)):
        which_caves.append(masterArray[which_caves_var[i]-1][0])
    return which_caves

def withTying(given_rope, halfSortedArray, max_pitches, which_caves_var):
    new_caves_var_possible = np.zeros(0)
    for i in range (0, len(given_rope)-1):
        for j in range (1, len(given_rope)-i):
            given_rope_copy = np.array(given_rope)
            given_rope_copy[i] = given_rope_copy[i]+given_rope_copy[i+j]
            given_rope_copy[i+j] = 0
            caves_accessible_now, which_caves_var_now = ropeCheck(given_rope_copy, halfSortedArray, max_pitches)
            new_caves = np.setdiff1d(which_caves_var_now, which_caves_var)
            if new_caves != []:
                new_caves_var_possible = np.append(new_caves_var_possible, new_caves)
                new_caves_var_possible = np.unique(new_caves_var_possible) 
    which_caves_var = sorted(np.append(which_caves_var, new_caves_var_possible), reverse=False)
    return which_caves_var, new_caves_var_possible
            
def argumentProcessing(usage_string):
    commands = []
    sub=0
    numArg = len(sys.argv)-1
    pitchFileName = "pitchFile.csv"
    if numArg == 0:
        print usage_string
        sys.exit()
    elif numArg > 0:
        if sys.argv[1][-4:] == ".csv" and numArg == 1:
            print usage_string
        elif sys.argv[1][-4:] == ".csv" and numArg != 1:
            pitchFileName = sys.argv[1]
        elif sys.argv[1][-4:] != ".csv":
            sub=1
            print "Using default pitch file: 'pitchFile.csv'..." #TODO supress this message when just help is called
        for i in range(2-sub,numArg+1):
            commands.append(sys.argv[i])
    return pitchFileName, commands

def runArgs(commands, pitchFileName, usage_string):
    my_rope = [50,50,30,30,15] #put your currently owned ropes here, or required_rope to test
    masterArray = readFile(pitchFileName)
    numericArray, total_caves, max_pitches, total_pitches, pitchesArray = numArray(masterArray)
    max_pitch_length, min_pitch_length, avg_pitch_length, max_pitch_num, min_pitch_num, avg_pitch_num, sortedArray, halfSortedArray = sortNumeric(numericArray, total_caves, pitchesArray)
    required_rope = sortedArray[0]
    caves_accessible, which_caves_var = ropeCheck(my_rope, halfSortedArray, max_pitch_num)
    which_caves = nameCaves(which_caves_var, masterArray)
    which_caves_var_updated, new_caves_var_possible = withTying(my_rope, halfSortedArray, max_pitches, which_caves_var)
    new_cave_names = nameCaves(new_caves_var_possible, masterArray)
    
    for i in range (0, len(commands)):
        if commands[i] == "reqRope":
            print "reqRope: "+str(required_rope)
        elif commands[i] == "totCave":
            print "totCave: "+str(total_caves)
        elif commands[i] == "noJoinN":
            print "noJoinN: "+str(caves_accessible)
        elif commands[i] == "noJoinL":
            print "noJoinL: "+str(which_caves)
        elif commands[i] == "yesJoinN":
            print "yesJoinN: "+str(len(which_caves_var_updated))
        elif commands[i] == "yesJoinL":
            print "yesJoinL: "+str(new_cave_names)
        elif commands[i] == "help" or "Help" or "HELP":
            print usage_string
            sys.exit()
        else:
            print "Command error!"
            sys.exit()
            
pitchFileName, commands = argumentProcessing(usage_string)
runArgs(commands, pitchFileName, usage_string)

#print "You've told me that you have the following rope lengths: "+str(sorted(np.array(my_rope), reverse=True))
#print "To access all caves without joining rope you'd require, at minimum, the following lengths of rope: "+str(required_rope)
#print "You can access "+str(caves_accessible)+" of a possible "+str(total_caves)+" caves without joining rope."
#print "These are caves: "+str(which_caves)
#print "If you are happy to join ropes then you can do "+str(len(new_caves_var_possible))+" new caves, for a total of "+str(len(which_caves_var_updated))+" of a possible "+str(total_caves)+" caves."
#print "You will have to join ropes in: "+str(new_cave_names)