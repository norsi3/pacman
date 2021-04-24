"""
    Game logic

Classes:
    Board:  processes request and passes to player, creates 
            and manages player instance
    Player: plays game, keeps track of walls, coins, position
"""

__author__ = "Natalie Orsi"

from grid import GridObject as GO, Request



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
    r: Request = Request(input_file)
    b: Board = Board(r.process_req())
    p: Player = b.p
    final_pos_x: int = p.pos.x
    final_pos_y: int = p.pos.y
    coins_collected: int = p.balance()
    return final_pos_x, final_pos_y, coins_collected

class Board(GO):
    cardinals = {
        "N": "0 1",
        "S": "0 -1",
        "W": "-1 0",
        "E": "1 0"
    }
    
    def __init__(self, req):
        self.p: Player = self.create_player(req)
        if not self.p.error:
            self.p.act()
        return 
        
    def obstructed(self, cell): return cell in self.wall_list
    
    def create_player(self, req):
        p: Player = Player(req)
        return Board.bad_game(p) if p.error else p
    
    @staticmethod
    def bad_game(p):
        p.coins = 0
        p.loc = GO.loc_error()
        return p
        
    def __str__(self):
        return(f"Board(max={str(self.max_dim)},walls={self.wall_list})")

class Player(GO): 
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
            self.pos = GO.loc_error()
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
            
            _next = self.coords(Board.cardinals[next_instruction])
            target = self.look(_next)
            
            if self.move(target):
                if target not in self.visited:
                    self.coin()                    
                self.visited.add(target) #includes repeat visits

        if (not self.visited) or self.balance()<0:
            self.error = True

    def move(self, dest):
        if self.out_of_bounds(dest) or self.obstructed(dest): 
            return False
        else: self.pos = dest
        return True        

    def look(self, d):
        x = self.pos.x + d.x
        y = self.pos.y + d.y
        return self.coords(f"{x} {y}")

    def is_cardinal(self,d: str):
        if Board.cardinals[d]:
            return Board.cardinals[d]
        else:
            return False
    
    def coin(self): self.coins += 1
    
    def balance(self): return self.coins
    
    def out_of_bounds(self, c):
        if (c.x < 0) or (c.y < 0): 
            return True
        elif ((c.x > self.bounds.x-1) or
              (c.y > self.bounds.y-1)):
            return True
        return False

    def obstructed(self, c): 
        return c in self.wall_list

    def __str__(self):
        s=f"Player(x={self.pos.x},y={self.pos.y},coins={self.balance()})"
        return s