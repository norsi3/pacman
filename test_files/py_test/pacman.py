"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple
from grid import GridObject,Request


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
    b = Board(r.process_req())
    testing = True
    if testing:
        return r.debug(b)
    raise NotImplementedError
    # return final_pos_x, final_pos_y, coins_collected 

class Board(GridObject):
    max_dim = None
    player = None
    movements = None
    wall_list = None
    
    def __init__(self, req):
        self.max_dim = req[0]
        if req[3]: 
            self.wall_list = req[3:]
        self.player = self.createplayer(req[1],req[2])
        return 
    
    def out_of_bounds(self, c):
        if (c.x < 0) or (c.y < 0): return False
        elif (c.x > self.max_dim.x) or \
            (c.y > self.max_dim.y):
            return False
        else: return not self.obstructed(c)
        
    def obstructed(self, c): return c in self.wall_list
    
    def createplayer(self, initial_pos, movements):
        p = Player(initial_pos, movements)
        assert(not p.loc in self.wall_list)
        return p
    
    def __str__(self):
        return(f"Board({str(self.max_dim)},{self.movements},{self.wall_list})")

class Player(GridObject):
    coins = 0
    game_over = False
    movements = None
    
    def __init__(self, cell, movements):
        super()
        self.movements = movements
        
    def act(self):
        if self.game_over: return
        while self.movements:
            if self.move(self.movements.pop(0)):
                self.coin()
            
    def move(self, direction): return direction
    
    def coin(self): self.coins += 1
    
    def balance(self): return self.coins
    