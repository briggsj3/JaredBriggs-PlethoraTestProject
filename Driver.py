# This file drives the PlethoraProjectTest program.
#   By Jared Briggs (briggsj3@gmail.com)
#   12-18-2015


from Profile import Profile
import os
import json
import time


# Call this function to parse a JSON file and run the Profiler.
#   Accepts:  Path to a JSON-formatted file.
#   Returns:  The cost of the profile (machine cost + material cost) as string.
def CalculateProfileCost(json_path):
    print 'Parsing Profile file:  \"' + json_path + '\"...'
    
    # Get the contents of the file:
    try:
        jsonfile = open(json_path, 'r')
    except Exception, e:
        print ' ERROR:  CalculateProfileCost() -> An error was encountered ' + \
            'while attempting to open the file \"' + \
            json_path + '\" (error = \"' + str(e) + '\").'
        return -1
    
    try:
        jsontxt = jsonfile.read()
    except Exception, e:
        print ' ERROR:  CalculateProfileCost() -> An error was encountered ' + \
            'while attempting to read the file \"' + \
            json_path + '\" (error = \"' + str(e) + '\").'
        jsontxt = ''
    finally:
        jsonfile.close()
    
    if jsontxt == '':
        return -2
    
    # Convert the JSON contents of the file into a dict:
    try:
        jsondict = json.loads(jsontxt)
    except Exception, e:
        print ' ERROR:  CalculateProfileCost() -> An error was encountered ' + \
            'while attempting to convert JSON file \"' + \
            json_path + '\" (error = \"' + str(e) + '\").'
        return -3
    
    # Create the profile:
    try:
        profile = Profile(jsondict)
    except Exception, e:
        print ' ERROR:  CalculateProfileCost() -> An error was encountered ' + \
            'while attempting to create the Profile (error = \"' + str(e) + '\").'
        return -3
    
    print '...finished.'
    
    print 'Material Size Required = ' + str(profile.DimX) + ' x ' + \
        str(profile.DimY) + ' inches.'
    
    # Return a currency-style decimal:
    return profile.TotalCost
    

# Get the location of this script:
testdir = os.path.dirname(os.path.realpath(__file__))

# Run the three given tests:
print 'Total Profile Cost = $' + str(CalculateProfileCost(testdir + \
    "/ExampleFiles/Rectangle.json")) + '\n'
print 'Total Profile Cost = $' + str(CalculateProfileCost(testdir + \
    "/ExampleFiles/ExtrudeCircularArc.json")) + '\n'
print 'Total Profile Cost = $' + str(CalculateProfileCost(testdir + \
    "/ExampleFiles/CutCircularArc.json")) + '\n'

time.sleep(50)
