# This file contains the object definition for the Vertex object.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015


import math

class Vertex(object):
    def __init__(self, id, json_dict):
        # Get the information about this vertex from the json_dict:
        try:
            ob_dict = json_dict["Vertices"][str(id)]
        except Exception, e:
            print ' ERROR:  Vertex::__init__() -> Error caught getting information from dictionary (error = \"' + str(e) + '\", object ID = \"' + str(id) + '\").'
            return
        
        self.ID = id
        self.X = ob_dict["Position"]["X"]
        self.Y = ob_dict["Position"]["Y"]

    
    def calcDistance(self, x, y):
        return(math.sqrt((self.X - x)*(self.X - x) + (self.Y - y)*(self.Y - y)))
