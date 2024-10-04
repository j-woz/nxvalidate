
# From https://github.com/nexpy/nxvalidate/issues/21#issuecomment-2392789824 (1)

import os
import numpy as np
from nexusformat.nexus import *

x = y = np.linspace(0, 2*np.pi, 101)
X,Y = np.meshgrid(y, x)
z = np.sin(X) * np.sin(Y)

root = NXroot(NXentry())
root['entry/data'] = NXdata(z,[x,y])

# Get this module name:
T = os.path.splitext(os.path.basename(__file__))[0]
F = os.getenv("DATA") + "/" + T + ".nxs"
print("filename: " + F)

root.save(F)
