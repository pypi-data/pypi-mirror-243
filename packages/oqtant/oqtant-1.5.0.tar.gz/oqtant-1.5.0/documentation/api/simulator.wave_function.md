<!-- markdownlint-disable -->

<a href="../../oqtant/simulator/wave_function.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `simulator.wave_function`






---

<a href="../../oqtant/simulator/wave_function.py#L21"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `WaveFunction`
'WaveFunction' Defines representation for a wavefunction 

<a href="../../oqtant/simulator/wave_function.py#L26"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `__init__`

```python
__init__()
```






---

#### <kbd>property</kbd> atom_number

Returns atom number 

---

#### <kbd>property</kbd> column_densities

Returns the column densities (#/Length^2) column_zy:  the zy axes column_zx:  the zx axes profiles:  the profiles in the x and z axes 

---

#### <kbd>property</kbd> com_position

Returns the center of mass coordinates of the cloud in X direction The center of mass cannot be displaced in the radial direction by assumption Returns 1 scalar Useful for diagnostics 

---

#### <kbd>property</kbd> current

Returns the total current along the X-direction Returns a 1D array 

---

#### <kbd>property</kbd> density

Returns the density of the wave function 

---

#### <kbd>property</kbd> density_profiles

Returns the density profiles along the x and r axes.  #/Length These match the integrated column densities 

---

#### <kbd>property</kbd> flow

Returns the superfluid velocities in X and R directions Returns two 2D arrays 

---

#### <kbd>property</kbd> phase

Returns the phase of the wave function 

---

#### <kbd>property</kbd> widths

Returns the widths (\Delta r and \Delta x) in radial and x directions Returns 2 scalars 



---

<a href="../../oqtant/simulator/wave_function.py#L31"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `initial_psi`

```python
initial_psi(sigma_x=1, sigma_r=1) → ndarray
```

Defines the initial wave function of the system with controllable widths. 



**Args:**
 
 - <b>`sigma_x int`</b>:   width in the x direction 
 - <b>`sigma_r int`</b>:   width in the r direction 



**Returns:**
 
 - <b>`psi np.ndarray`</b>:   initial wave function 

---

<a href="../../oqtant/simulator/wave_function.py#L49"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `normalize`

```python
normalize(psi)
```

Normalizes the wave function to the number of atoms Applies normalization directly to self.psi 



**Args:**
 
 - <b>`psi np.ndarray`</b>:   wavefunction 



**Returns:**
 None 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
