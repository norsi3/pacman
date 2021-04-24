"""
Write a module docstring here
"""

__author__ = "Your Name"
from abc import abstractclassmethod
from collections import namedtuple

class Request:
    _raw_req = None
    
    ERROR = ("-1 -1", 0)
    
    _max = None
    _initial = None
    _moves = None
    _walls = None
    
    def __init__(self, file_name):
        if file_name:
            self._raw_req = self.filerequest(file_name)
        self.process_req()
    
    def process_req(self):
        rr = self._raw_req
        if not self.validateraw(rr):
            return self.ERROR
        self._max = GridObject.coords(rr[0].strip())
        self._initial = GridObject.coords(rr[1].strip())
        self._moves = list(rr[2].strip())
        assert(len(self._moves)>0)
        self._walls = []
        if len(rr) > 3:
            for line in rr[3:]:
                self._walls.append(GridObject.coords(line.strip()))
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
        return isinstance(o,list)
    
    @staticmethod
    def debug(*args):
        readout = lambda x: f"{type(x).__name__}: {str(x)}"
        return [readout(x) for x in args]

class GridObject:
    max_dim = None
    loc = None
    
    def __init__(self,cell):
      self.loc = self.coords(cell)

    @staticmethod
    def coords(s):
        x,y=map(int, s.split(" "))
        return namedtuple("cell", ("x","y"))(x,y)
        
    @abstractclassmethod
    def obstructed(self, *args):
        pass
        
    def __str__(self):
        return f"{self.loc.x}, {self.loc.y})"