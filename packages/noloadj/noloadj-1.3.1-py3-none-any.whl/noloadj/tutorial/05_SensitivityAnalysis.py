# SPDX-FileCopyrightText: 2021 G2Elab / MAGE
#
# SPDX-License-Identifier: Apache-2.0

from numpy.testing import *
from noloadj.analyse.simulation import computeOnce,computeJacobian,\
    computeParametric
import numpy as np

def rosenbrock(x,y):
    fobj=(1-x)*(1-x)+100*(y-x*x)**2
    ctr1=(x-1)**3-y+1
    ctr2=x+y-2
    return locals().items()


# Compute outputs
inputs = {'x': 1.0, 'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']
results = computeOnce(model=rosenbrock, inputs=inputs, outputs=outputs)
print(outputs, '=', results)


# Compute Parametric
inputs = {'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']

variable = 'x'
values = np.arange(-1.5, 1.5, 0.1)  # [-1.5, -1.4, ..., 1.5]
iter = computeParametric(rosenbrock, variable, values, inputs, outputs)

df = iter.print()
print(df)
iter.plotXY()

# Compute Gradients
inputs = {'x': 1.0, 'y': 2.0}
outputs = ['fobj', 'ctr1', 'ctr2']
dfobj,dctr1,dctr2 = computeJacobian(model=rosenbrock, inputs=inputs,
                                    outputs=outputs)
print('dfobj =', dfobj)
print('dctr1 =', dctr1)
print('dctr2 =', dctr2)

