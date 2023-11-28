<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/qm_potential.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.qm_potential`






---

<a href="../../oqtant/simulator/qm_potential.py#L20"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `QMPotential`
'QMPotential' translate Oqtant 'quantum_matter' object into simulation units and uses that objects get_potential function to construct a 2D array used for the potential energy in the simulation 

<a href="../../oqtant/simulator/qm_potential.py#L48"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(quantum_matter)
```






---

#### <kbd>property</kbd> lifetime





---

#### <kbd>property</kbd> time_of_flight







---

<a href="../../oqtant/simulator/qm_potential.py#L68"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `update_potential`

```python
update_potential(time)
```

times within barrier/landscape jobs are automatically converted to simulation units in update_potential updates self.V potential_1D_x needs only be called every 100 microseconds--potential speedup step. 



**Args:**
 
 - <b>`time`</b>:   time (in simulation units) 



**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
