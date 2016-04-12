# pitch-lengths
###### A Python 2.7 Project

The pitch-lengths project intends to make rope buying decisions easier for those interested in SRT caving in the UK. Its central aim is the creation of a `.csv` file containing required rope lengths for caves across the country, and the statistical analysis of this data to inform rope buying for clubs.

This project is designed for a `unix` operating system and requires the `numpy` package for array manipulation and statistics, and the `matplotlib.pyplot` package for histogram plotting (_experimental_); everything else should be included in your `python` package. It should be easy to get it running on Windows, but I have no experience with that.

For the moment this project runs from the command line; so ensure that the `.csv` file is in the same folder as the pitch-lengths.py file.
This should be the case by default if you download the zipped project, but you do need to make the `pitch-lengths.py` file executable by navigating to the folder and running:

    chmod u+x pitch-lengths.py
    
An example operation is shown below:

    Last login: Tue Apr 12 12:49:28 on ttys000
    Marvin:~ Ari$ .\pitch-lengths.py help
    
        usage: .\pitch-lengths.py <pitchFile> command(s)

        The <pitchFile> argument should contain the name of your file.
        If no name is given this defaults to 'pitchFile.csv'.
    
        The following commands can be run:
            ideal_rope          min rope needed for every cave w/o joining ropes
            total_caves         number of caves in .csv file
            num_poss_norm       number of caves possible w/o joining ropes
            list_poss_norm      list of the caves possible w/o joining ropes
            num_poss_join       number of caves possible w/ joining ropes
            list_poss_join      list of caves in which rope joining is required
            histogram           display histogram of all pitch (experimental)
            help                displays this usage information
        
        Some of these commands will require you to specify the rope you have using:
            .\pitch-lengths.py update_rope

        For example, a common usage might be:
            .\pitch-lengths.py pitchFile.csv ideal_rope total_caves
        
Please feel free to ask any questions or get involved with the development of this project.