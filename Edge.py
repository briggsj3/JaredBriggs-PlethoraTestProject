# This file contains the definition for the parent Edge object (this is inherited by other edge objects).
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015


class Edge(object):
    def __init__(self, id):
        self.ID = id
    
    def getBounds(self, vertex_dict):
        pass
    
    def calcMachinePrice(self, vertex_dict):
        pass
