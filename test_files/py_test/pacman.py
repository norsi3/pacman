"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple
import json


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
    return("req: "+str(b))
    # return final_pos_x, final_pos_y, coins_collected 

class Request:
    _raw_req = None
    _final_req = None
    ERROR = (-1, -1, 0)
    
    def __init__(self, file_name):
        if file_name:
            self._raw_req = self.filerequest(file_name)
        self.process_req()
    
    def process_req(self):
        rr = self._raw_req
        if not self.validateraw(rr):
            return self.ERROR
        board_max_location = GridObject.coords(rr[0])
        initial_position = GridObject.coords(rr[1])
        movements = list(rr[2])
        assert(len(movements)>0)
        walls = []
        if len(rr) > 3:
            for line in rr[3:]:
                walls.append(GridObject.coords(line))
        self._final_req = board_max_location, initial_position, movements, walls
        return self._final_req
        
    @staticmethod
    def filerequest(f):
        with open(f, "r") as f:
             #ignore anything after 1000 bytes as out of scope
             return f.readlines(1000)

    @staticmethod
    def validateraw(o):
        return isinstance(o,list)

class GridObject:
    loc = None
    # define named tuple for organization
    def __init__(self,cell):
      self.loc = self.coords(cell)

    @staticmethod
    def coords(s):
        x,y=map(int, s.split(" "))
        return namedtuple("cell", ("x","y"))(x,y)

    def __str__(self):
        return f"{self.loc.x}, {self.loc.y})"
class Board(GridObject):
    max_dim = None
    player = None
    movements = None
    wall_list = None
    
    def __init__(self, req):
        self.max_dim = req[0]
        if req[3]: self.wall_list = req[3:]
        self.player = self.createplayer(req[1],req[2])
        return 
    
    def out_of_bounds(self, c):
        if (c.x < 0) or (c.y < 0): return False
        elif (c.x > self.max_dim.x) or \
            (c.y > self.max_dim.y):
            return False
        else: return not self.obstructed(c)
        
    def obstructed(self, c): return c in self.wall_list
    
    def createplayer(self,initial_pos, movements):
        p = Player(initial_pos, movements)
        assert(not p.loc in self.wall_list)
        return p
    
    def __str__(self):
        return(f"Board({self.max_dim},{self.movements},{self.wall_list})")

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
    