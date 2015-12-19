# This file drives the PlethoraProjectTest program.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015


from Profile import Profile
import time

# Read the json file:
jsonfile = open("D:\Desktop Stuff\Applications\Plethora test project\Proj\ExampleFiles\Rectangle.json")
#jsonfile = open("D:\Desktop Stuff\Applications\Plethora test project\Proj\ExampleFiles\ExtrudeCircularArc.json")
#jsonfile = open("D:\Desktop Stuff\Applications\Plethora test project\Proj\ExampleFiles\CutCircularArc.json")
filetxt = jsonfile.read()
jsonfile.close()

import json
parsed_json = json.loads(filetxt)

# Create the profile:
profile = Profile(parsed_json)

time.sleep(30)


#def PriceFile(filepath):
    
