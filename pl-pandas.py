#! /usr/bin/env python

try:
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import sys
except Exception,e:
    print "Your system does not have the necessary pre-requisites: "
    print str(e)
    sys.exit()

usage_string = """usage: .\pl-pandas.py command [command(s)]

Commands that can be run include:
    pitch_info          displays a graph pitch number frequency with stats
    length_info         displays a histogram of rope lengths with stats
    help                displays this usage information

For example a common usage might be:
    .\pl-pandas.py pitch_info length_info"""

def import_data():
    """takes data from the pitch file"""
    master_frame = pd.DataFrame()
    with open("pitchFile.csv", 'r') as file:
        for line in file:
            if line != "\n" and line[0] != "#":
                master_frame = pd.concat([master_frame, pd.DataFrame([tuple(line.strip().split(','))])], ignore_index=True)
    numeric_frame = master_frame.ix[:,1:].astype(float)

    return master_frame, numeric_frame

def pitch_info(master_frame):
    number_pitches = numeric_frame.count()
    mean_number_pitches = number_pitches.mean()
    axis = number_pitches.plot(kind="bar", grid=True, rot=0)
    axis.set_xlabel("Number of Pitches")
    axis.set_ylabel("Number of Caves")
    axis.annotate("Mean number of pitches: "+str(mean_number_pitches),(4,75),bbox=dict(facecolor="white", alpha=0.75, boxstyle="round,pad=1"))
    plt.show()
    
def length_info(numeric_frame):
    mean_length_pitches = np.around(numeric_frame.mean().mean(), decimals=2)
    max_pitch_length = numeric_frame.max().max()
    min_pitch_length = numeric_frame.min().min()
    axis = numeric_frame.plot.hist(stacked=False, legend=False, bins=18, grid=True, rot=0, alpha=0.75)
    axis.set_xlabel("Length of Pitch")
    axis.set_ylabel("Number of Pitches")
    axis.annotate("Mean length of pitches: "+str(mean_length_pitches)+"\n"+"Max pitch length: "+str(max_pitch_length)+"\n"+"Min pitch length: "+str(min_pitch_length),(110,20),bbox=dict(facecolor="white", alpha=0.75, boxstyle="round,pad=1"))
    plt.show()

def get_arguments(usage_string):
    if len(sys.argv) == 1:
        print usage_string
        sys.exit()
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "pitch_info":
            pitch_info(master_frame)
        elif sys.argv[i] == "length_info":
            length_info(numeric_frame)
        elif sys.argv[i] == "help":
            print usage_string
            sys.exit()
        else:
            print "Invalid command: "
            print usage_string
            sys.exit()

master_frame, numeric_frame = import_data()
get_arguments(usage_string)