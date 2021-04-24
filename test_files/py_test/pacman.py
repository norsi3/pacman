"""
Write a module docstring here
"""

__author__ = "Your Name"


from collections import namedtuple

from grid import GridObject, Request
DEBUG = True
LOC_ERROR = GridObject.coords("-1 -1")

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
        if not self.player.error:
            self.player.act()
        

        return 
        
    def obstructed(self, c): return c in self.wall_list
    
    def create_player(self, req):
        p = Player(req)
        if p.error:
            # print(f"aborted board ({p.abort}) of max size: {req.get_max_dim()}, the player visited {p.visited}. There were walls at {p.wall_list}.")
            p = self.bad_game(p)
        return p
    
    @staticmethod
    def bad_game(p):
        print("aborted bad game")
        p.coins = 0
        p.loc = LOC_ERROR
        return p
        
    def __str__(self):
        return(f"Board(max={str(self.max_dim)},walls={self.wall_list})")

class Player(GridObject): 
    def __init__(self, req):
        self.error = False
        self.wall_list = req.get_walls()
        self.bounds = req.get_max_dim()
        self.movements = req.get_moves()
        self.pos = req.get_initial_pos()
        self.visited = set([self.pos])
        self.coins = 0
        self.error = not self.valid_instructions()
        if self.error:
            self.pos = LOC_ERROR
            self.coins = 0
            
    def valid_instructions(self):
        if not self.movements: return False
        for letter in self.movements:
            if letter not in Board.cardinals.keys(): return False
        for wall in self.wall_list:
            if self.out_of_bounds(wall): return False
        return not(self.out_of_bounds(self.pos) or self.obstructed(self.pos))
    
    def act(self):
                
        while self.movements:
            next_instruction = self.movements.pop(0)
            # print(f"next_instruction={next_instruction}")
            
            _next = self.coords(Board.cardinals[next_instruction])
            target = self.look(_next)
            
            if self.move(target):
                if target not in self.visited:
                    self.coin()
                    # print(f"got a coin: total is {self.balance()}")
                # else: print(f"I already gathered a coin from {target}.")
                    
                self.visited.add(target) #includes repeat visits

            # print(f"===   location is now {self.pos}   ===")
        if (not self.visited) or self.balance()<0:
            # print(f"self.visited? {self.visited} and self.balance? {self.balance}")
            self.error = True
        # print(f">>>>>>>I got {self.balance()} coins from visiting {len(self.visited)} cells, out of {self.original_movements_length} instructions. There were {len(self.wall_list)} walls.")

    def move(self, dest):
        if self.out_of_bounds(dest) or self.obstructed(dest): 
            return False
        else: self.pos = dest
        return True        

    def look(self, d):
        x = self.pos.x + d.x
        y = self.pos.y + d.y
        print(f"starting at {self.pos}, facing {d} brings you to (x={x},y={y})")
        return self.coords(f"{x} {y}")

    def is_cardinal(self,d: str):
        print(f"is_direction: {Board.cardinals[d]}, which is {bool(Board.cardinals[d])}")
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
        elif ((c.x > self.bounds.x-1) or
              (c.y > self.bounds.y-1)):
            print(f"didn't move - {c} > max {self.bounds}")
            return True
        return False

    def obstructed(self, c): 
        return c in self.wall_list

    def __str__(self):
        s=f"Player(x={self.pos.x},y={self.pos.y},coins={self.balance()})"
        return s