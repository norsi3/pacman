"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple

from grid import GridObject, Request
DEBUG = True

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
    return p.pos.x, p.pos.y, p.balance()
    # return final_pos_x, final_pos_y, coins_collected 

class Board(GridObject):
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
        print(f"player created: {self.player}")
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
    def __init__(self, req):
        self.wall_list = req.get_walls()
        self.bounds = req.get_max_dim()
        self.movements = req.get_moves()
        self.pos = req.get_initial_pos()
        self.visited = []
        self.coins = 0
        self.original_movements_length = len(req.get_moves())
        
    def act(self):        
        while self.movements:
            next_instruction = self.movements.pop(0)
            print(f"next_instruction={next_instruction}")
            if not self.is_direction(next_instruction): pass
            
            _next = self.coords(Board.cardinals[next_instruction])
            target = self.look(_next)
            
            if self.move(target):
                if not target in self.visited:
                    self.coin()
                    print(f"got a coin: total is {self.balance()}")
                else:
                    print(f"I already gathered a coin from {target}.")
                    
                self.visited.append(target) #includes repeat visits

                    
            print(f"===   location is now {self.pos}   ===")
        if len(self.visited) < 1 or self.balance()<1:
            self.pos = super().coords(Request.ERROR[0])
            self.coins = 0
        print(f">>>>>>>I got {self.balance()} coins from visiting {len(self.visited)} cells, out of {self.original_movements_length} instructions. There were {len(self.wall_list)} walls.")

    def move(self, dest):
        if self.out_of_bounds(dest): 
            return False
        else: self.pos = dest
        return True        

    def look(self, d):
        x = self.pos.x + d.x
        y = self.pos.y + d.y
        print(f"looked at {self.pos} and direction {d} and got {x},{y}")
        return self.coords(f"{x} {y}")

    def is_direction(self,d: str):
        # print(f"is_direction: {Board.cardinals[d]}, which is {bool(Board.cardinals[d])}")
        if Board.cardinals[d]:
            return Board.cardinals[d]
        else:
            return False
    
    def coin(self): self.coins += 1
    
    def balance(self): return self.coins
    
    def out_of_bounds(self, c):
        if (c.x < 0) or (c.y < 0): 
            print(f"didn't move - {c} < (0,0)")
            return True
        elif (c.x > self.bounds.x-1) or \
            (c.y > self.bounds.y-1):
            print(f"didn't move - {c} > max {self.bounds}")
            return True
        else: return self.obstructed(c)

    def obstructed(self, c): 
        if c in self.wall_list:
            print(f"{c} is a wall, can\'t go there")
        return c in self.wall_list

    def __str__(self):
        s=f"Player(coins={self.balance()}, visited={self.visited}, next_dir={self.movements[0]})"
        return s

    