# This file contains the object definition for the Line object.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015

from Vertex import Vertex
from Edge import Edge
import Constants

class Line(Edge):
    def __init__(self, id, json_dict):
        Edge.__init__(self, id)
        
        # Get the information about this edge from the json_dict:
        try:
            ob_dict = json_dict["Edges"][str(id)]
        except Exception, e:
            print ' ERROR:  Line::__init__() -> Error caught getting information from dictionary (error = \"' + str(e) + '\", object ID = \"' + str(id) + '\").'
            return
        
        # Make sure the object definition is for a Line:
        if ("Type" not in ob_dict):
            print ' ERROR:  Line::__init__() -> No Type detected (object ID = \"' + str(id) + '\").'
            return
        elif (ob_dict["Type"] != "LineSegment"):
            print ' ERROR:  Line::__init__() -> Incorrect Type detected (type given = \"' + ob_dict["Type"] + '\", object ID = \"' + str(id) + '\").'
            return
        
        # Make sure there are a sufficient number of vertices defined for this line:
        if ("Vertices" not in ob_dict):
            print ' ERROR:  Line::__init__() -> \"Vertices\" not found in ob_dict (object ID = \"' + str(id) + '\").'
            return
        elif (len(ob_dict["Vertices"]) != 2):
            print ' ERROR:  Line::__init__() -> Incorrect number of vertices supplied in ob_dict (number = ' + str(len(ob_dict["Vertices"])) + ', object ID = \"' + str(id) + '\").'
            return            
        
        # NOTE:  I am storing only the vertex ID here because it is unknown whether all vertices will have been read in yet at this point.
        self.V1 = ob_dict["Vertices"][0]
        self.V2 = ob_dict["Vertices"][1]
    
    
    def getBounds(self, vertex_dict):
        # Make sure that the line's vertices exist in vertex_dict:
        if (self.V1 not in vertex_dict):
            print ' ERROR:  Line::getBounds() -> Vertex ' + str(self.V1) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V1]) is not Vertex):
            print ' ERROR:  Line::getBounds() -> Vertex ' + str(self.V1) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V1]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        elif (self.V2 not in vertex_dict):
            print ' ERROR:  Line::getBounds() -> Vertex ' + str(self.V2) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V2]) is not Vertex):
            print ' ERROR:  Line::getBounds() -> Vertex ' + str(self.V2) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V2]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        
        # Get the vertex objects:
        v1 = vertex_dict[self.V1]
        v2 = vertex_dict[self.V2]
        
        # Find bounds:
        bounds = [min(v1.X, v2.X), max(v1.X, v2.X), min(v1.Y, v2.Y), max(v1.Y, v2.Y)]
        return bounds
        
    
    def calcMachinePrice(self, vertex_dict):
        # Make sure that the line's vertices exist in vertex_dict:
        if (self.V1 not in vertex_dict):
            print ' ERROR:  Line::calcMachinePrice() -> Vertex ' + str(self.V1) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V1]) is not Vertex):
            print ' ERROR:  Line::calcMachinePrice() -> Vertex ' + str(self.V1) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V1]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        elif (self.V2 not in vertex_dict):
            print ' ERROR:  Line::calcMachinePrice() -> Vertex ' + str(self.V2) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V2]) is not Vertex):
            print ' ERROR:  Line::calcMachinePrice() -> Vertex ' + str(self.V2) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V2]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
    
        # Get the length of the line (distance between the vertices):
        v2 = vertex_dict[self.V2]
        length = vertex_dict[self.V1].calcDistance(v2.X, v2.Y)
        
        return length * Constants.MachineCost_persecond / Constants.MaxSpeed 
