# pitch-lengths
The pitch-lengths project intends to make rope buying decisions easier for those interested in SRT caving in the UK. Its central aim is the creation of a .csv file containing required rope lengths for caves across the country, and the statistical analysis of this data to inform rope buying for clubs.

This project requires the numpy package for array manipulation and statistics; everything else should be included in your python package.

For the moment this project runs from the command line; so ensure that the .csv file is in the same folder as the PLS2.py file, and make the PLS2.py file executable by navigating to the folder and running:

    chmod u+x PLS2.py
    
An example operation is shown below:

    Last login: Tue Apr 12 12:49:28 on ttys000
    Marvin:~ Ari$ .\PLS2.py help
    
        usage: .\PLS2.py [<pitchFile>] command
        
        The first given argument should be your csv file. Default 'pitchFile.csv':
            
        The following given arguments should be your desired command:
            reqRope     returns min rope needed for every cave without joining ropes
            totCave     returns the number of caves to be evaluated
            noJoinN     returns the number of caves possible without joining ropes
            noJoinL     returns a list of the caves possible without joining ropes
            yesJoinN    returns the number of caves possible with joining ropes
            yesJoinL    returns a list of caves in which rope joining would be required
            
        For example, a common usage might be:
            .\PLS2.py pitchFile.csv reqRope maxCaveN