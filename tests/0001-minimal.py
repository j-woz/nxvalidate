
import os
import numpy as np
from nexusformat.nexus import *

# From:
# https://nexpy.github.io/nexpy/treeapi.html#module-nexusformat.nexus.tree

x = y = np.linspace(0, 2*np.pi, 101)
X,Y = np.meshgrid(y, x)
z = np.sin(X) * np.sin(Y)

root = NXroot(NXentry())
root.entry.data = NXdata(z,[x,y])

# Get this module name:
T = os.path.splitext(os.path.basename(__file__))[0]
F = os.getenv("DATA") + "/" + T + ".nxs"
print("filename: " + F)

filename = NXFile(F, "w")
filename.writefile(root)
