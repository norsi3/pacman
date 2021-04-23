"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple

Coords = namedtuple("Coords", ("x","y"))


def pacman(input_file):
    """ Use this function to format your input/output arguments. Be sure not to change the order of the output arguments. 
    Remember that code organization is very important to us, so we encourage the use of helper fuctions and classes as you see fit.
    
    Input:
        1. input_file (String) = contains the name of a text file you need to read that is in the same directory, includes the ".txt" extension
           (ie. "input.txt")
    Outputs:
        1. final_pos_x (int) = final x location of Pacman
        2. final_pos_y (int) = final y location of Pacman
        3. coins_collected (int) = the number of coins that have been collected by Pacman across all movements
    """
    r = Request(input_file)
    return r._raw_req
    # return final_pos_x, final_pos_y, coins_collected 

class Request:
    _raw_req = None
    _final_req = None
    
    def __init__(self, file_name):
        if file_name:
            self._raw_req = self.filerequest(file_name)
        return
    
    @staticmethod
    def filerequest(f):
        with open(f, "r") as f:
             #ignore anything after 1000 bytes as out of scope
             return f.readlines(1000)
                
