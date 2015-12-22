# PlethoraTestProject
A sample project made for Plethora as part of my interviewing for employment process.


# Assumptions:
- This software was written with the intent of readability, not necessarily efficiency or elegancy.
- The minimum coordinates for both axes on the laser cutter are (0,0) (i.e., no negative coordinates).
- When checking bounds of a circular arc, only points at degree increments along the arc are checked.
- The specified padding amount is split between both sides of each dimension (i.e., the material used is 0.1 inches bigger in each dimension than the design to be cut).


## Why I chose to use Python for this Implementation:
1. Python allows rapid prototyping of a system such as this, readily supplying much of the necessary functionality (JSON parsing, etc.)
2. I wanted to be sure that Plethora employees could run my code without needing other external libraries (in C++, I use the Boost libraries for cross-platform networking, JSON parsing, threading, and other fun functionality)


# Running the PlethoraTestProject:
## To Run the Three Test Cases:
Either double-click on the `Driver.py` file.

Alternatively, in your Python terminal, you can navigate to the PlethoraTestProject directory, and run `import Driver`.

## To Build a Profile object from the PlethoraTestProject using a JSON-formatted text:
Assuming you've read a JSON-formatted file into an object called `jsontxt`,
```
import json
jsondict = json.loads(jsontxt)
from Profile import Profile
profile = Profile(jsondict)

print 'The dimensions of the profile's material = ' + str(profile.DimX) + ' x ' + str(profile.DimY) + ' inches.'
print 'The cost of the profile = $' + profile.TotalCost + '.'
```



# What I Would Do Differently if I had More Time:
- I'd implement this in C++ and use Boost to facilitate network connection (it would act as a service that would be called only when a laser-cut model was received).
- Parallelizing this would allow faster calculation of profiles with large numbers of edges (as well as a high volume of incoming profiles).
- I'd add support for other types of curves (Bezier, B-spline, etc.).
- I'd add support for raster engraving (creating designs on the surface of a workpiece without cutting all the way through).
- I'd add support for using different materials or sheets of various thicknesses.  This would affect the speed of the cutter (as well as the intensity and focus of the beam), and would then need to be taken into account.
- It would be more proper to keep currency in integer or decimal format (because it's impossible to have a fraction of a cent).  I stored the Profile.TotalCost as a string for readability (since it didn't really seem to matter for this case).
- It would be more appropriate to use the locale package to format the final cost of the profile.  That would also allow for different currency formats based on the user's geographical location.
