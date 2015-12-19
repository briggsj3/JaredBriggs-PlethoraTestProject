# This file contains the definition for the Profile object.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015


from Vertex import Vertex
from Line import Line
from CircularArc import CircularArc
import Constants

class Profile(object):
    def __init__(self, json_dict):
        # These store the created objects (in dictionaries, keyed by ID):
        self.VertexDict = dict()
        self.EdgeDict = dict()
        
        # Step through all of the edges in json_dict, and create them:
        for edge in json_dict["Edges"]:
            id_str = edge
            
            # Determine the edge Type, and create the appropriate one:
            type = json_dict["Edges"][id_str]["Type"]
            if (type == "LineSegment"):
                self.EdgeDict[int(id_str)] = Line(int(id_str), json_dict)
            elif (type == "CircularArc"):
                self.EdgeDict[int(id_str)] = CircularArc(int(id_str), json_dict)
            else:
                print ' WARNING:  Profile::__init__() -> Unrecognized edge type = \"' + type + '\" (object ID = ' + id_str + ').'
        
        # Step through all of the vertices in json_dict, and create them:
        for vertex in json_dict["Vertices"]:
            id_str = vertex
            
            # Create the Vertex:
            self.VertexDict[int(id_str)] = Vertex(int(id_str), json_dict)
        
        print str(len(self.EdgeDict)) + ' edges created.'
        print str(len(self.VertexDict)) + ' vertices created.'
        
        # Calculate the overall bounds and machine cost:
        xmin_G = None
        xmax_G = None
        ymin_G = None
        ymax_G = None
        machine_cost = 0.0
        for edge in self.EdgeDict.values():
            # Bounds:
            [xmin, xmax, ymin, ymax] = edge.getBounds(self.VertexDict)
            if (xmin_G == None):
                xmin_G = xmin
                xmax_G = xmax
                ymin_G = ymin
                ymax_G = ymax
            else:
                xmin_G = min(xmin_G, xmin)
                xmax_G = max(xmax_G, xmax)
                ymin_G = min(ymin_G, ymin)
                ymax_G = max(ymax_G, ymax)
            
            # Machine Cost:
            machine_cost += edge.calcMachinePrice(self.VertexDict)
        
        if (xmin_G == None):
            print ' ERROR:  Profile::__init__() -> No bounds found.'
            return
        
        
        # Calculate the material cost:
        area = (xmax_G - xmin_G + Constants.Padding) * (ymax_G - ymin_G + Constants.Padding)
        material_cost = Constants.MaterialCost_persqin * area
        
        # Total cost:
        total_cost = machine_cost + material_cost
        
        print 'Total Profile Cost = $' + str(total_cost)
        
        
    
  #  def calcPrice(self):
        