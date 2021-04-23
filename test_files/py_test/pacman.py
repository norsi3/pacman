"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple

from grid import GridObject, Request


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
    p = b.player
    testing = False
    if testing:
        return r.debug(p)
    return p.pos.x, p.pos.y, p.coins
    # return final_pos_x, final_pos_y, coins_collected 

class Board(GridObject):
    player = None
    wall_list = None
    cardinals = {
        "N": "0 1",
        "S": "0 -1",
        "W": "-1 0",
        "E": "1 0"
    }
    
    def __init__(self, req):
        self.max_dim = req.get_max_dim()
        if req.get_walls():
            self.wall_list = req.get_walls()
        self.player = self.create_player(req)
        self.player.act()
        return 
        
    def obstructed(self, c): return c in self.wall_list
    
    def create_player(self, req):
        p = Player(req)
        if self.wall_list:
            assert(not p.pos in self.wall_list)
        return p
    
    def __str__(self):
        return(f"Board({str(self.max_dim)},{self.wall_list})")

class Player(GridObject):
    coins = 0
    movements = None
    pos = None
    wall_list = None
    bounds = None
    
    def __init__(self, req):
        self.wall_list = req.get_walls()
        self.bounds = req.get_max_dim()
        self.movements = req.get_moves()
        self.pos = req.get_initial_pos()
        
    def act(self):        
        while self.movements:
            next_instruction = self.movements.pop(0)
            
            if not self.is_direction(next_instruction): pass
            
            _next = self.coords(Board.cardinals[next_instruction])
            target = self.look(_next)
            
            if self.move(target):
                self.coin()
    
    def move(self, dest):
        d = self.look(dest)
        if self.out_of_bounds(d): 
            return False
        else: self.pos = d
        return True        

    def look(self, d):
        x = self.pos.x + d.x
        y = self.pos.y + d.y
        return self.coords(f"{x} {y}")
        
    def is_direction(self,d: str):
        return Board.cardinals[d]
    
    def coin(self): self.coins += 1
    
    def balance(self): return self.coins
    
    def out_of_bounds(self, c):
        if (c.x < 0) or (c.y < 0): 
            return True
        elif (c.x > self.bounds.x) or \
            (c.y > self.bounds.y):
            return True
        else: return self.obstructed(c)

    def obstructed(self, c): 
        return c in self.wall_list

    def __str__(self):
        return(f"Player(coins={self.coins})")

    