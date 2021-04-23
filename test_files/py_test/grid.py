"""
Write a module docstring here
"""

__author__ = "Your Name"
from collections import namedtuple

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
    
    @staticmethod
    def debug(*args):
        readout = lambda x: f"{type(x).__name__}: {str(x)}"
        return [readout(x) for x in args]

class GridObject:
    loc = None
    def __init__(self,cell):
      self.loc = self.coords(cell)

    @staticmethod
    def coords(s):
        x,y=map(int, s.split(" "))
        return namedtuple("cell", ("x","y"))(x,y)

    def __str__(self):
        return f"{self.loc.x}, {self.loc.y})"