# This file contains the object definition for the CircularArc (Circular Arc) object.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015

from Vertex import Vertex
from Edge import Edge
import Constants
import math

class CircularArc(Edge):
    def __init__(self, id, json_dict):
        Edge.__init__(self, id)
        
        # Get the information about this edge from the json_dict:
        try:
            ob_dict = json_dict["Edges"][str(id)]
        except Exception, e:
            print ' ERROR:  CircularArc::__init__() -> Error caught getting information from dictionary (error = \"' + str(e) + '\", object ID = \"' + str(id) + '\").'
            return
            
        if ("Type" not in ob_dict):
            print ' ERROR:  CircularArc::__init__() -> No Type detected (object ID = \"' + str(id) + '\").'
            return
        elif (ob_dict["Type"] != "CircularArc"):
            print ' ERROR:  CircularArc::__init__() -> Incorrect Type detected (type given = \"' + ob_dict["Type"] + '\", object ID = \"' + str(id) + '\").'
            return
        
        # Make sure there are a sufficient number of vertices defined for this line:
        if ("Vertices" not in ob_dict):
            print ' ERROR:  CircularArc::__init__() -> \"Vertices\" not found in ob_dict (object ID = \"' + str(id) + '\").'
            return
        elif (len(ob_dict["Vertices"]) != 2):
            print ' ERROR:  CircularArc::__init__() -> Incorrect number of vertices supplied in ob_dict (number = ' + str(len(ob_dict["Vertices"])) + ', object ID = \"' + str(id) + '\").'
            return            
        
        # NOTE:  I am storing only the vertex IDs here because it is unknown whether all vertices will have been read in yet at this point.
        self.V1 = ob_dict["Vertices"][0]
        self.V2 = ob_dict["Vertices"][1]
        
        # Ensure that the center point is fully defined:
        if ("X" not in ob_dict["Center"] or "Y" not in ob_dict["Center"]):
            print ' ERROR:  CircularArc::__init__() -> Center point is not fully defined (object ID = \"' + str(id) + '\").'
            return
        
        self.X = ob_dict["Center"]["X"]
        self.Y = ob_dict["Center"]["Y"]
        
        # Make sure the ClockwiseFrom field exists:
        if ("ClockwiseFrom" not in ob_dict):
            print ' ERROR:  CircularArc::__init__() -> No \"ClockwiseFrom\" field found in the input (object ID = \"' + str(id) + '\").'
            return
        
        self.ClockwiseFrom = ob_dict["ClockwiseFrom"]
        
        # Make sure the vertex ID given in the ClockwiseField matches one of the two given vertices:
        if (self.ClockwiseFrom != self.V1 and self.ClockwiseFrom != self.V2):
            print ' ERROR:  CircularArc::__init__() -> The vertex ID defined as \"ClockwiseFrom\" does not match either of the vertices given for this object (object ID = \"' + str(id) + '\").'
            return
    
    
    def getBounds(self, vertex_dict):
        # Make sure that the line's vertices exist in vertex_dict:
        if (self.V1 not in vertex_dict):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V1) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V1]) is not Vertex):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V1) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V1]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        elif (self.V2 not in vertex_dict):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V2) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V2]) is not Vertex):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V2) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V2]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        
        # Get the vertex objects:
        v1 = vertex_dict[self.V1]
        v2 = vertex_dict[self.V2]
        
        # Make sure v1 and v2 are not the same point as the center:
        if (v1.X == self.X and v1.Y == self.Y):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V1) + ' has the same coordinates as the arc\'s center point (arc object ID = \"' + str(self.ID) + '\").'
            return
        elif (v2.X == self.X and v2.Y == self.Y):
            print ' ERROR:  CircularArc::getBounds() -> Vertex ' + str(self.V2) + ' has the same coordinates as the arc\'s center point (arc object ID = \"' + str(self.ID) + '\").'
            return
        
        # Get the radius of the arc:
        radius = self.getRadius(v1)
        
        # Get the angle of the arc:
        [theta_start, theta_end] = self.getVertexAngles(v1, v2)
        
        # Convert the thetas to degrees (this will simplify bound checking, since a point will be found at each degree increment):
        theta_start = int(math.ceil(math.degrees(theta_start)))
        theta_end = int(math.floor(math.degrees(theta_end)))
        if (theta_start >= theta_end):
            print ' NOTICE:  CircularArc::getBounds() -> A very small arc angle (about 1 degree or less) was found (object ID = ' + str(self.ID) + ').  Using only end points.'
            
            # Find bounds using only the end points:
            return([min(v1.X, v2.X), max(v1.X, v2.X), min(v1.Y, v2.Y), max(v1.Y, v2.Y)])
        else:
            minx = None
            maxx = None
            miny = None
            maxy = None
            for i in range(theta_start, theta_end, 1):
                # Find the coordinates of the point at this angle:
                px = radius * math.cos(math.radians(i))
                py = radius * math.sin(math.radians(i))
                
                # Compare:
                if (minx is None):
                    # Initialize:
                    minx = px
                    maxx = px
                    miny = py
                    maxy = py
                else:
                    if (px < minx):
                        minx = px
                    elif (px > maxx):
                        maxx = px
                        
                    if (py < miny):
                        miny = py
                    elif (py > maxy):
                        maxy = py
            
            # Find bounds:
            bounds = [min(v1.X, v2.X, minx), max(v1.X, v2.X, maxx), min(v1.Y, v2.Y, miny), max(v1.Y, v2.Y, maxy)]
            return bounds
        
    
    def calcMachinePrice(self, vertex_dict):
        # Make sure that the line's vertices exist in vertex_dict:
        if (self.V1 not in vertex_dict):
            print ' ERROR:  CircularArc::calcMachinePrice() -> Vertex ' + str(self.V1) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V1]) is not Vertex):
            print ' ERROR:  CircularArc::calcMachinePrice() -> Vertex ' + str(self.V1) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V1]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
        elif (self.V2 not in vertex_dict):
            print ' ERROR:  CircularArc::calcMachinePrice() -> Vertex ' + str(self.V2) + ' not found in vertex_dict (object ID = \"' + str(self.ID) + '\").'
            return
        elif (type(vertex_dict[self.V2]) is not Vertex):
            print ' ERROR:  CircularArc::calcMachinePrice() -> Vertex ' + str(self.V2) + ' is not of type Vertex (object type = \"' + type(vertex_dict[self.V2]) + '\", object ID = \"' + str(self.ID) + '\").'
            return
    
        # Get the length of the line (distance between the vertices):
        v1 = vertex_dict[self.V1]
        v2 = vertex_dict[self.V2]
        length = self.calcLength(v1, v2)
        
        return length * Constants.MachineCost_persecond / (Constants.MaxSpeed * math.exp(-1.0 / float(self.getRadius(v1))))
        
    
    def getRadius(self, v):
        # Get the radius of the arc:
        return v.calcDistance(self.X, self.Y)
    
    
    def getVertexAngles(self, v1, v2):
        # Get the angle of the arc:
        theta1 = math.atan2(v1.Y - self.Y, v1.X - self.X)
        theta2 = math.atan2(v2.Y - self.Y, v2.X - self.X)
            
        if (self.ClockwiseFrom == self.V1 and theta1 > theta2):
            theta_start = theta2
            theta_end = theta1
        elif (self.ClockwiseFrom == self.V1):
            theta_start = theta1
            theta_end = theta2
        elif (theta2 > theta1):
            theta_start = theta1
            theta_end = theta2
        else:
            theta_start = theta2
            theta_end = theta1
        
        return [theta_start, theta_end]
    
    
    def calcLength(self, v1, v2):
        # Get the radius of the arc:
        radius = self.getRadius(v1)
        
        # Get the angle of the arc:
        [theta_start, theta_end] = self.getVertexAngles(v1, v2)
        
        # Convert the thetas to degrees (this will simplify bound checking, since a point will be found at each degree increment):
        theta_start_int = int(math.ceil(math.degrees(theta_start)))
        theta_end_int = int(math.floor(math.degrees(theta_end)))
        if (theta_start_int >= theta_end_int):
            print ' NOTICE:  CircularArc::calcLength() -> A very small arc angle (about 1 degree or less) was found (object ID = ' + str(self.ID) + ').  Treating as straight line.'
            
            # Return the distance using only the end points:
            return(v1.calcDistance(v2.X, v2.Y))
        else:
            dist = 0.0
            lastx = radius * math.cos(theta_start)
            lasty = radius * math.sin(theta_start)
            for i in range(theta_start_int, theta_end_int, 1):
                # Find the coordinates of the point at this angle:
                px = radius * math.cos(math.radians(i))
                py = radius * math.sin(math.radians(i))
                
                # Calculate the distance between these points:
                dist += math.sqrt((px - lastx)*(px - lastx) + (py - lasty)*(py - lasty))
                
                lastx = px
                lasty = py
            
            px = radius * math.cos(theta_end)
            py = radius * math.sin(theta_end)
            dist += math.sqrt((px - lastx)*(px - lastx) + (py - lasty)*(py - lasty))
            
            # Return the cumulative distance:
            return dist