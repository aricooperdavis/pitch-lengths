# pitch-lengths
The pitch-lengths project intends to make rope buying decisions easier for those interested in SRT caving in the UK. Its central aim is the creation of a .csv file containing required rope lengths for caves across the country, and the statistical analysis of this data to inform rope buying for clubs.

This project requires the numpy package for array manipulation and statistics; everything else should be included in your python package.

For the moment this project runs from the command line; so ensure that the .csv file is in the same folder as the PLS2.py file, and make the PLS2.py file executable by navigating to the folder and running:

    chmod u+x pitch-lengths.py
    
An example operation is shown below:

    Last login: Tue Apr 12 12:49:28 on ttys000
    Marvin:~ Ari$ .\pitch-lengths.py help
    
        usage: .\pitch-lengths.py <pitchFile> command [command]
        
        The <pitchFile> argument should contain the name of your file.
        If no name is given this defaults to 'pitchFile.csv'.
            
        The following commands can be run:
            reqRope     returns min rope needed for every cave without joining ropes
            totCave     returns the number of caves to be evaluated
            noJoinN     returns the number of caves possible without joining ropes
            noJoinL     returns a list of the caves possible without joining ropes
            yesJoinN    returns the number of caves possible with joining ropes
            yesJoinL    returns a list of caves in which rope joining would be required
            help        displays this usage information
        
        Some of these commands will require you to specify the rope you have using:
            .\pitch-lengths.py update_rope
        
        For example, a common usage might be:
            .\pitch-lengths.py pitchFile.csv reqRope totCave
        
Please feel free to ask any questions or get involved with the development of this project.