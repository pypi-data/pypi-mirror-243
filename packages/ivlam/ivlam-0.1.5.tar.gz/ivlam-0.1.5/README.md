# Python Wrapper for ivlam

This is a python wrapper of the Fortran code of Russell's Lambert Solver.

## Install
```
pip install ivlam
```

## Usage
Initialize 
```python
from ivlam import *

infoload = ivlam.initialize(-1)
if(infoload!=0):
    print('Error in ivlam_initialize')
```

Solve the Problem
```python
r1vec=np.array([1.0,2.0,3.0])  
r2vec=np.array([2.0,-3.0,-4.0])
tof=450.0

prograde=True
direction=ivlam.getdirection(prograde,r1vec,r2vec)

dimensionV=10
v1vec,v2vec,uptonhave,inforeturnstatusn,infohalfrevstatus = ivlam.thrun(r1vec,r2vec,tof,direction,dimensionV,dimensionV)
if(inforeturnstatusn!=0):
    print('Error in ivlam_thrun')
if(infohalfrevstatus!=0):
    print('This example is very close to the nPi transfer')
print(v1vec[:,dimensionV-uptonhave:dimensionV+uptonhave+1])
print(v2vec[:,dimensionV-uptonhave:dimensionV+uptonhave+1])
```

## Reference
 [1] Russell, Ryan P., "On the Solution to Every Lambert Problem," 
        Celestial Mechanics and Dynamical Astronomy, Vol. 131, Article 50, 2019, pp. 1-33, 
        https://dx.doi.org/10.1007/s10569-019-9927-z 

 [2] Russell, Ryan P., "Complete Lambert Solver Including Second-Order Sensitivities," 
        Journal of Guidance, Control, and Dynamics, accepted 2021,
        https://doi.org/10.2514/1.G006089 