#! /usr/bin/env python

import csv
import sys
import json
import numpy as np
import matplotlib.pyplot as plt
from array import array

usage_string = """usage: .\pitch-lengths.py <pitchFile> command(s)

The <pitchFile> argument should contain the name of your file.
If no name is given this defaults to 'pitchFile.csv'.
    
The following commands can be run:
    reqRope     returns min rope needed for every cave without joining ropes
    totCave     returns the number of caves to be evaluated
    noJoinN     returns the number of caves possible without joining ropes
    noJoinL     returns a list of the caves possible without joining ropes
    yesJoinN    returns the number of caves possible with joining ropes
    yesJoinL    returns a list of caves in which rope joining would be required
    histogram   displays a histogram of the pitch inforamtion (experimental)
    help        displays this usage information

Some of these commands will require you to specify the rope you have using:
    .\pitch-lengths.py update_rope

For example, a common usage might be:
    .\pitch-lengths.py pitchFile.csv reqRope totCave"""

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
    """given cave variables returns the names of the caves"""
    which_caves = []
    if type(which_caves_var) is not list:
        which_caves_var = which_caves_var.astype(int)
    for i in range (0, len(which_caves_var)):
        which_caves.append(masterArray[which_caves_var[i]-1][0])
    return which_caves

def withTying(given_rope, halfSortedArray, max_pitches, which_caves_var):
    """given a length of rope returns the caves that would be possible with tying it together"""
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

def makeHistogram(numericArray):
    numericList = np.trim_zeros(sorted(numericArray.flatten()))
    n, bins, patches = plt.hist(numericList, bins=10, normed=1, facecolor='green', alpha=0.75)
    plt.title(r'$\mathrm{Histogram\ of\ pitch\ lengths}$')
    plt.xlabel('Pitch Length')
    plt.ylabel('Probability')
    plt.axis([0, 90, 0, 0.04])
    plt.grid(True)
    plt.show()

def argumentProcessing(usage_string):
    """processes command line arguments"""
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
    """runs command line arguments processed above"""
    for i in range (0, len(commands)):
        if commands[i] == "help" or commands[i] == "Help" or commands[i] == "HELP":
            print usage_string
            sys.exit()
        elif commands[i] == "update_rope":
            write_rope()
        else:
            masterArray = readFile(pitchFileName)
            numericArray, total_caves, max_pitches, total_pitches, pitchesArray = numArray(masterArray)
            max_pitch_length, min_pitch_length, avg_pitch_length, max_pitch_num, min_pitch_num, avg_pitch_num, sortedArray, halfSortedArray = sortNumeric(numericArray, total_caves, pitchesArray)
            required_rope = sortedArray[0]
            if commands[i] == "reqRope":
                print "reqRope: "+str(required_rope)
            elif commands[i] == "totCave":
                print "totCave: "+str(total_caves)
            else:
                my_rope = read_rope()
                caves_accessible, which_caves_var = ropeCheck(my_rope, halfSortedArray, max_pitch_num)
                which_caves = nameCaves(which_caves_var, masterArray)
                which_caves_var_updated, new_caves_var_possible = withTying(my_rope, halfSortedArray, max_pitches, which_caves_var)
                new_cave_names = nameCaves(new_caves_var_possible, masterArray)
                if commands[i] == "noJoinN":
                    print "noJoinN: "+str(caves_accessible)
                elif commands[i] == "noJoinL":
                    print "noJoinL: "+str(which_caves)
                elif commands[i] == "yesJoinN":
                    print "yesJoinN: "+str(len(which_caves_var_updated))
                elif commands[i] == "yesJoinL":
                    print "yesJoinL: "+str(new_cave_names)
                elif commands[i] == "histogram":
                    print "Displaying histogram."
                    makeHistogram(numericArray)
                else:
                    print "Command error!"
                    sys.exit()
    
def read_rope():
    """reads rope values from hidden .rope_file.text"""
    try:
        rope_file = open('.rope_file.txt', 'r')
        my_rope = json.load(rope_file)
        if my_rope == "":
            print "This feature requires your rope lengths; please update this using: "+"\n"+"./pitch-lengths.py update_rope"
            rope_file.close()
            sys.exit()
        else:
            rope_file.close()
            return my_rope
    except:
        print "This feature requires your rope lengths; please update this using: "+"\n"+"./pitch-lengths.py update_rope"
        sys.exit()
    
def write_rope():
    """creates hidden rope_file.text by asking for rope lengths"""
    rope_file = open('.rope_file.txt', 'w')
    my_rope = []
    end_ask = 0
    print "To update your rope lengths enter the length of your ropes one by one and press enter after each rope. Once you've run out of ropes just press enter."
    while end_ask != 100:
        rope = raw_input("Rope "+str(end_ask+1)+": ")
        if rope != "":
            my_rope.append(int(rope))
            end_ask += 1
        else:
            end_ask = 100
    rope_file.write(str(my_rope))
    rope_file.close()
            
pitchFileName, commands = argumentProcessing(usage_string)
runArgs(commands, pitchFileName, usage_string)