
# From https://github.com/nexpy/nxvalidate/issues/21#issuecomment-2392789824 (2)

import os
import numpy as np
from nexusformat.nexus import *

x = y = np.linspace(0, 2*np.pi, 101)
X,Y = np.meshgrid(y, x)
z = np.sin(X) * np.sin(Y)

# Get this module name:
T = os.path.splitext(os.path.basename(__file__))[0]
F = os.getenv("DATA") + "/" + T + ".nxs"
print("filename: " + F)

with nxopen(F, "w") as root:
    root['entry'] = NXentry()
    root['entry/data'] = NXdata(z,[x,y])

