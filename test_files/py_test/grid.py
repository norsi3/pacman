"""
    Request handling & grid class/object definitions

Classes:
    Request: receives request, validates and passes onto Board for processing
    GridObject: standardizes coordinate handling, inherited by Board and Player
"""

__author__ = "Natalie Orsi"
from collections import namedtuple

class Request:
    def __init__(self, file_name):
        self.fail = False
        self.raw_req = None
        self._max = None
        self._initial = None
        self._walls = None
        self._moves = None
        if file_name:
            self._raw_req = Request.filerequest(file_name)
        self.process_req()
        if self.fail:
            self._initial = GridObject.coords("-1 -1")
            self._max = GridObject.coords("0 0")

    def process_req(self):
        rr = self._raw_req
        if not Request.validateraw(rr):
            self.fail = True
            return self
        self._max = GridObject.coords(rr[0].strip())
        self._initial = GridObject.coords(rr[1].strip())
        self._moves = list(rr[2].strip())
        assert(len(self._moves)>0)
        self._walls = set() #find in set is O(1) rather than find in list O(n)
        if len(rr) > 3:
            for line in rr[3:]:
                line = line.strip()
                if line:
                    self._walls.add(GridObject.coords(line))
        return self
        
    def get_max_dim(self): return self._max
    def get_initial_pos(self): return self._initial
    def get_moves(self): return self._moves
    def get_walls(self): return self._walls
    
    @staticmethod
    def filerequest(f):
        with open(f, "r") as f:
             #ignore anything after 1000 bytes as out of scope
             return f.readlines(1000)

    @staticmethod
    def validateraw(o):
        return o and isinstance(o,list)
    
    @staticmethod
    def debug(*args):
        readout = lambda x: f"{type(x).__name__}: {str(x)}"
        return [readout(x) for x in args]

class GridObject:
    def __init__(self,cell):
      self.pos = self.coords(cell)
    
    @staticmethod
    def coords(s):
        x,y=map(int, s.split(" "))
        return namedtuple("cell", ("x","y"))(x,y)
    def __str__(self):
        return f"({self.loc.x}, {self.loc.y})"