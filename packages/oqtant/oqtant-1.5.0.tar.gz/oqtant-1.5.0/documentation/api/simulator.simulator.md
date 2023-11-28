<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/simulator.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.simulator`






---

<a href="../../oqtant/simulator/simulator.py#L32"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `TimeSpan`
TimeSpan(start: float, end: float) 

<a href="../../<string>"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(start: float, end: float) → None
```









---

<a href="../../oqtant/simulator/simulator.py#L38"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Simulator`
'Simulator' Defines methods for evolution and plotting of the system 

<a href="../../oqtant/simulator/simulator.py#L50"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__(wavefunction: WaveFunction, potential: QMPotential)
```






---

#### <kbd>property</kbd> it_plot

Generate an simulation analog to an in-trap image from the Oqtant hardware. 



**Args:**
 



**Returns:**
 
- it_image_pixels (list): pixels of the simulation generated IT image 
- columns (int): number of cols in simulation generated IT images 
- rows (int): number of rows in simulation generated IT images 
- pixcal (float): size of a pixel in simulation generated IT images 



---

<a href="../../oqtant/simulator/simulator.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `convert_timesteps`

```python
convert_timesteps(timesteps: list) → ndarray
```





---

<a href="../../oqtant/simulator/simulator.py#L117"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_GPE`

```python
get_GPE(psi: ndarray) → ndarray
```

Implementation of the Gross-Pitaevskii Equation w/Neumann boundary conditions at r = 0 and Dirichlet at large x and r. 

---

<a href="../../oqtant/simulator/simulator.py#L86"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_laplacian`

```python
get_laplacian(y) → ndarray
```

Implementation of the second derivatives in x and r including forward, central, and backward formulas to second order accuracy 

---

<a href="../../oqtant/simulator/simulator.py#L130"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_RK4`

```python
run_RK4(time_span: TimeSpan, ground=False, TOF=False) → None
```

Implementation of the Runge-Kutta 4th order method to evolve in time. 



**Args:**
 
 - <b>`time_span`</b>:   a list of times (in milliseconds) 
 - <b>`ground`</b>:  allows simulation of ground state and evolves in imaginary time 
 - <b>`TOF`</b>:   whether or not to switches off potentials and rescale the grids 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L73"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `run_evolution`

```python
run_evolution() → None
```

This function evolves the condensate with ground = False. It is done at positive times while the barriers are switched on. It runs for the lifetime of the quantum_matter object It starts from the end result of running get_ground_state 

---

<a href="../../oqtant/simulator/simulator.py#L59"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `set_ground_state`

```python
set_ground_state()
```

This function evolves the condensate with ground = True. It is done at negative times before the barriers are switched on. 2.5 simulation units of time is sufficient to settle down to the ground state. Potentially this could be stored as it's always the same unless the user wants to change number_of_atoms. 

---

<a href="../../oqtant/simulator/simulator.py#L388"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_column_densities`

```python
show_column_densities(timesteps, TOF=False)
```

Plots the column densities and slices of the condensate in cartesian coordinates for an input array of times. In correct coordinates to be returned to the user. 



**Args:**
 
 - <b>`timesteps`</b>:   a list of times (in milliseconds) 
 - <b>`TOF`</b>:   whether or not to rescale the grids in TOF mode 



**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L523"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_current`

```python
show_current(timesteps, TOF=False)
```

Plot the flow for a given list of timesteps two separate sub plots 



**Args:**
 
 - <b>`timesteps`</b> (list):  List of times to display 
 - <b>`TOF`</b> (bool):  True to rescale grids in TOF mode. 



**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L327"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_density_cylindrical`

```python
show_density_cylindrical(timesteps: list, TOF=False) → None
```

Plots the density profile of the condensate in cylindrical coordinates for an input array of times. Useful coordinates for diagonising issues but not to be returned to the user. 



**Args:**
 
 - <b>`timesteps`</b>:   a list of times (in milliseconds) 
 - <b>`TOF`</b>:   whether or not to switch off potentials and rescale the grids 

**Returns:**
 None 

---

<a href="../../oqtant/simulator/simulator.py#L291"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_final_result`

```python
show_final_result() → None
```

Plot the density at the end of the simulation in cylindrical coordinates. Useful coordinates for diagonising issues but not to be returned to the user. 

---

<a href="../../oqtant/simulator/simulator.py#L480"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_phase`

```python
show_phase(timesteps, TOF=False) → None
```

Plot the phase for a given list of timesteps This can only be displayed in cylindrical coordinates. It is a helpful tool still for the user.  The aspect ratio is still a bit weird. 



**Args:**
 
 - <b>`timesteps`</b> (list):  List of times to display 
 - <b>`TOF`</b> (bool):  True to rescale grids in TOF mode. 

**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
