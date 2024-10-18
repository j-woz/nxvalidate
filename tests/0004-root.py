
import os
import numpy as np
from nexusformat.nexus import *

# Get this module name:
T = os.path.splitext(os.path.basename(__file__))[0]
F = os.getenv("DATA") + "/" + T + ".nxs"
print("filename: " + F)

with nxopen(F, "w") as root:
    root['entry']=NXentry()
