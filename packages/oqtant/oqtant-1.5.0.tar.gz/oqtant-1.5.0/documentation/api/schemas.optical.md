<!-- markdownlint-disable -->

<a href="../../oqtant/schemas/optical.py#L0"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

# <kbd>module</kbd> `schemas.optical`





---

<a href="../../oqtant/schemas/optical.py#L34"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>function</kbd> `gaussian`

```python
gaussian(
    xs: 'ndarray',
    amp: 'float' = 1.0,
    center: 'float' = 0.0,
    sigma: 'float' = 1.0,
    offset: 'float' = 0.0
) → ndarray
```

Method that evaluates a standard gaussian form over the given input points 



**Args:**
 
 - <b>`xs`</b> (numpy.ndarray):  Positions where the gaussian should be evaluated 
 - <b>`amp`</b> (float, optional):  Gaussian amplitude 
 - <b>`center`</b> (float, optional):  Gaussian center 
 - <b>`sigma`</b> (float, optional):  Gaussian width 
 - <b>`offset`</b> (float, optional):  Gaussian dc offset 



**Returns:**
 
 - <b>`np.ndarray`</b>:  Gaussian function evaluated over the input points 


---

<a href="../../oqtant/schemas/optical.py#L56"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Projected`
A class that captures the features, and limitations, of optical objects implemented by the Oqtant hardware projection system. 




---

<a href="../../oqtant/schemas/optical.py#L152"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_actual_potential`

```python
get_actual_potential(
    get_ideal_potential: 'Callable[[float], list]',
    time: 'float' = 0.0,
    positions: 'list' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to calculate the "actual" potential energy vs position for optical objects/fields as realized by the Oqtant projection system. Includes effects, and first-order corrections for, finite time updates and finite optical resolution/optical objects being projected as sums of gaussians and energetic clipping of optical potentials at 100 kHz 



**Args:**
 
 - <b>`get_ideal_potential`</b> (Callable[[float], list]):  Object method for request/ideal potential 
 - <b>`time`</b> (float, optional):  Time to evaluate ideal potential 
 - <b>`positions`</b> (list[float], optional):  Positions to evaluate the actual potential at 



**Returns:**
 
 - <b>`list[float]`</b>:  Expected actual potential energy at the request positions 

---

<a href="../../oqtant/schemas/optical.py#L87"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_corrected_time`

```python
get_corrected_time(time: 'float') → float
```

Method to calculate the effective time realized by the projection system, which only updates optical features periodically 



**Args:**
 
 - <b>`time`</b> (float):  Time, in ms, to be corrected 



**Returns:**
 
 - <b>`float`</b>:  The corrected time 

---

<a href="../../oqtant/schemas/optical.py#L70"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_corrected_times`

```python
get_corrected_times(times: 'list[float]') → list[float]
```

Method to calculate the effective times realized by the projection system, which only updates optical features periodically 



**Args:**
 
 - <b>`times`</b> (list[float]):  Time, in ms, to be corrected 



**Returns:**
 
 - <b>`list[float]`</b>:  The corrected times 

---

<a href="../../oqtant/schemas/optical.py#L102"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_projection_weights`

```python
get_projection_weights(
    get_ideal_potential: 'Callable[[float], list]',
    time: 'float' = 0
) → list[float]
```

Method to calculate weights for each horizontal "spot" projected onto the atom ensemble to attempt to achieve the passed optical object's "ideal" potential energy profile. Implements first-order corrections for anamolous contributions from nearby spots, inter-integer barrier centers, etc 



**Args:**
 
 - <b>`get_ideal_potential`</b> (Callable[[float], list]):  Method for the optical object or any class  that supports optical objects that calculates the specified "ideal" or "requested"  potential energy profile 
 - <b>`time`</b> (float, optional):  Time at which to correct 



**Returns:**
 
 - <b>`list[float]`</b>:  Calculated (optical intensity) contribution for each projected spot  (diffraction frequency) used by the projection systems 


---

<a href="../../oqtant/schemas/optical.py#L186"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Snapshot`
A class that represents a painted optical landscape/potential at a single point in (manipulation stage) time 


---

#### <kbd>property</kbd> model_computed_fields

Get the computed fields of this model instance. 



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects. 

---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 



---

<a href="../../oqtant/schemas/optical.py#L218"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(landscape: 'Landscape') → Snapshot
```

Method to create a Snapshot object from an existing jobs input 



**Args:**
 
 - <b>`landscape`</b> (bert_schemas.job.Landscape):  The input values 



**Returns:**
 
 - <b>`Snapshot`</b>:  A new Snapshot object created using the input data 

---

<a href="../../oqtant/schemas/optical.py#L230"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ideal_potential`

```python
get_ideal_potential(
    time=0.0,
    positions: 'list' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to get the ideal potential energy at the specified positions 



**Args:**
 
 - <b>`positions`</b> (list, optional):  List of positions in microns 



**Returns:**
 
 - <b>`list[float]`</b>:  Potential energies, in kHz, at the specified positions 

---

<a href="../../oqtant/schemas/optical.py#L249"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_potential`

```python
get_potential(positions: 'list[float]') → list[float]
```

Method to calculate the optical potential associated with a Landscape object, taking into account the actual implementation of the Oqtant projection system, at the given time 



**Args:**
 
 - <b>`positions`</b> (list[float]):  Positions, in microns, where the potential should be evaluated 



**Returns:**
 
 - <b>`list[float]`</b>:  Potential energies, in kHz, at the specified positions 

---

<a href="../../oqtant/schemas/optical.py#L191"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    time: 'float' = 0,
    positions: 'list' = [-10, 10],
    potentials: 'list' = [0, 0],
    interpolation: 'InterpolationType' = 'LINEAR'
) → Snapshot
```

Method to create a new Snapshot object 



**Args:**
 
 - <b>`time`</b> (float, optional):  Time associated with the snapshot 
 - <b>`positions`</b> (list, optional):  Position list for the snapshot 
 - <b>`potentials`</b> (list, optional):  Potential energies corresponding to the list of positions 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  How to connect the object's  (positions, potentials) data in space. 



**Returns:**
 
 - <b>`Snapshot`</b>:  a new Snapshot object 

---

<a href="../../oqtant/schemas/optical.py#L264"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_potential`

```python
show_potential(
    xlimits: 'list[float]' = [-61.0, 61],
    ylimits: 'list[float]' = [-1.0, 101],
    include_ideal: 'bool' = False
) → None
```

Method to plot the potential energy as a function of position for a Landscape object at the given times 



**Args:**
 
 - <b>`xlimits`</b> (list[float], optional):  Plot limits for x axis 
 - <b>`ylimits`</b> (list[float], optional):  Plot limits for y axis 
 - <b>`include_ideal`</b> (bool, optional):  Flag for including target potential in plot 


---

<a href="../../oqtant/schemas/optical.py#L308"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Landscape`
Class that represents a dynamic painted-potential optical landscape constructed from individual (instantaneous time) Snapshots 


---

#### <kbd>property</kbd> model_computed_fields

Get the computed fields of this model instance. 



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects. 

---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 

---

#### <kbd>property</kbd> snapshots

Property to get a list of Snapshot objects associated to a Landscape object 



**Returns:**
 
 - <b>`list[Snapshot]`</b>:  List of Snapshot objects 



---

<a href="../../oqtant/schemas/optical.py#L341"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(landscape: 'OpticalLandscape') → Landscape
```

Method to create a Landscape object from an existing jobs input 



**Args:**
 
 - <b>`landscape`</b> (job_schema.OpticalLandscape):  The input values 



**Returns:**
 
 - <b>`Landscape`</b>:  A new Landscape object 

---

<a href="../../oqtant/schemas/optical.py#L363"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ideal_potential`

```python
get_ideal_potential(
    time: 'float',
    positions: 'list[float]' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to calculate ideal object potential energy at the specified time and positions 



**Args:**
 
 - <b>`time`</b> (float):  Time, in ms, at which the potential energy is calculated 
 - <b>`positions`</b> (list[float], optional):  Positions at which the potential energy is calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  Potential energies, in kHz, at specified time and positions 

---

<a href="../../oqtant/schemas/optical.py#L394"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_potential`

```python
get_potential(
    time: 'float',
    positions: 'list' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to calculate the optical potential associated with a Landscape object, taking into account the actual implementation of the Oqtant projection system, at the given time 



**Args:**
 
 - <b>`time`</b> (float):  Time, in ms, at which to sample the potential energy 
 - <b>`positions`</b> (list[float], optional):  Positions, in microns, where the potential should be evaluated 



**Returns:**
 
 - <b>`list[float]`</b>:  Potential energies, in kHz, at the requested positions and time 

---

<a href="../../oqtant/schemas/optical.py#L313"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    snapshots: 'list[Snapshot]' = [Snapshot(time_ms=0.0, potentials_khz=[0.0, 0.0], positions_um=[-10.0, 10.0], spatial_interpolation=<InterpolationType.LINEAR: 'LINEAR'>), Snapshot(time_ms=2.0, potentials_khz=[0.0, 0.0], positions_um=[-10.0, 10.0], spatial_interpolation=<InterpolationType.LINEAR: 'LINEAR'>)]
) → Landscape
```

Method to create a new Landscape object 



**Args:**
 
 - <b>`snapshots`</b> (list[Snapshot], optional):  A list of Snapshot objects 



**Returns:**
 
 - <b>`Landscape`</b>:  A new Landscape object 

---

<a href="../../oqtant/schemas/optical.py#L412"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_potential`

```python
show_potential(
    times: 'list' = [0.0],
    xlimits: 'list' = [-61.0, 61],
    ylimits: 'list' = [-1.0, 101],
    include_ideal: 'bool' = False
)
```

Method to plot the potential energy as a function of position for a Landscape object at the given times 



**Args:**
 
 - <b>`times`</b> (list[float], optional):  Times, in ms, at which to evaluate and plot the potential 
 - <b>`xlimits`</b> (list[float], optional):  Plot limits for x axis 
 - <b>`ylimits`</b> (list[float], optional):  Plot limits for y axis 
 - <b>`include_ideal`</b> (bool, optional):  Flag for including target potential in plot 


---

<a href="../../oqtant/schemas/optical.py#L457"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

## <kbd>class</kbd> `Barrier`
Class that represents a painted optical barrier. 


---

#### <kbd>property</kbd> birth

Property to get the (manipulation stage) time that the Barrier object will be created 



**Returns:**
 
 - <b>`float`</b>:  The time, in ms, at which the barrier will start being projected 

---

#### <kbd>property</kbd> death

Property to get the (manipulation stage) time that the Barrier object will cease to exist 



**Returns:**
 
 - <b>`float`</b>:  The time, in ms, at which the barrier will stop being projected 

---

#### <kbd>property</kbd> lifetime

Property to get the lifetime value of a Barrier object 



**Returns:**
 
 - <b>`float`</b>:  The amount of time, in ms, that the barrier will exist 

---

#### <kbd>property</kbd> model_computed_fields

Get the computed fields of this model instance. 



**Returns:**
  A dictionary of computed field names and their corresponding `ComputedFieldInfo` objects. 

---

#### <kbd>property</kbd> model_extra

Get extra fields set during validation. 



**Returns:**
  A dictionary of extra fields, or `None` if `config.extra` is not set to `"allow"`. 

---

#### <kbd>property</kbd> model_fields_set

Returns the set of fields that have been set on this model instance. 



**Returns:**
  A set of strings representing the fields that have been set,  i.e. that were not filled from defaults. 



---

<a href="../../oqtant/schemas/optical.py#L545"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `evolve`

```python
evolve(
    duration: 'float',
    position: 'float' = None,
    height: 'float' = None,
    width: 'float' = None
) → None
```

Method to evolve the position, height, and/or width of a Barrier object over a duration 



**Args:**
 
 - <b>`duration`</b> (float):  The time, in ms, over which evolution should take place 
 - <b>`position`</b> (float | None, optional):  The position, in microns, to evolve to 
 - <b>`height`</b> (float | None, optional):  The height, in kHz, to evolve to 
 - <b>`width`</b> (float | None, optional):  The width, in microns, to evolve to 

---

<a href="../../oqtant/schemas/optical.py#L506"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `from_input`

```python
from_input(barrier: 'Barrier') → Barrier
```

Method to create a Barrier object using the input values of a job 



**Args:**
 
 - <b>`barrier`</b> (job_schema.Barrier):  The input values 



**Returns:**
 
 - <b>`Barrier`</b>:  A new Barrier object created using the input data 

---

<a href="../../oqtant/schemas/optical.py#L625"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_height`

```python
get_height(time: 'float') → float
```

Method to get the Barrier object height at the specified time 



**Args:**
 
 - <b>`time`</b> (float):  The time, in ms, at which the height is calculated 



**Returns:**
 
 - <b>`float`</b>:  The barrier height at the specified time 

---

<a href="../../oqtant/schemas/optical.py#L609"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_heights`

```python
get_heights(times: 'list[float]') → list[float]
```

Method to calculate the Barrier object heights at the specified list of times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the heights are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The barrier heights at the specified times 

---

<a href="../../oqtant/schemas/optical.py#L663"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_ideal_potential`

```python
get_ideal_potential(
    time: 'float' = 0.0,
    positions: 'list[float]' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to calculate the ideal Barrier object potential energy at the given positions and at the specified time without taking into account finite projection system resolution to update time of projected light 



**Args:**
 
 - <b>`time`</b> (float, optional):  The time, in ms, at which the potential is calculated 
 - <b>`positions`</b> (list[float], optional):  The positions, in microns, at which the potential  energies are evaluated 



**Returns:**
 
 - <b>`list[float]`</b>:  The potential energies, in kHz, at the specified positions 

---

<a href="../../oqtant/schemas/optical.py#L598"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_position`

```python
get_position(time: 'float') → float
```

Method to calculate the Barrier object position at the specified (manipulation stage) time 



**Args:**
 
 - <b>`time`</b> (float):  The time, in ms, at which the position is calculated 



**Returns:**
 
 - <b>`float`</b>:  The position, in microns, at the specified time 

---

<a href="../../oqtant/schemas/optical.py#L582"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_positions`

```python
get_positions(times: 'list[float]') → list[float]
```

Method to calculate the Barrier object position at the specified (manipulation stage) times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which positions are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The positions, in microns, at the specified times 

---

<a href="../../oqtant/schemas/optical.py#L692"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_potential`

```python
get_potential(
    time: 'float',
    positions: 'list[float]' = array([-60., -59., -58., -57., -56., -55., -54., -53., -52., -51., -50.,
       -49., -48., -47., -46., -45., -44., -43., -42., -41., -40., -39.,
       -38., -37., -36., -35., -34., -33., -32., -31., -30., -29., -28.,
       -27., -26., -25., -24., -23., -22., -21., -20., -19., -18., -17.,
       -16., -15., -14., -13., -12., -11., -10.,  -9.,  -8.,  -7.,  -6.,
        -5.,  -4.,  -3.,  -2.,  -1.,   0.,   1.,   2.,   3.,   4.,   5.,
         6.,   7.,   8.,   9.,  10.,  11.,  12.,  13.,  14.,  15.,  16.,
        17.,  18.,  19.,  20.,  21.,  22.,  23.,  24.,  25.,  26.,  27.,
        28.,  29.,  30.,  31.,  32.,  33.,  34.,  35.,  36.,  37.,  38.,
        39.,  40.,  41.,  42.,  43.,  44.,  45.,  46.,  47.,  48.,  49.,
        50.,  51.,  52.,  53.,  54.,  55.,  56.,  57.,  58.,  59.,  60.])
) → list[float]
```

Method to calculate the optical potential associated with a Barrier object, taking into account the actual implementation of the Oqtant projection system 



**Args:**
 
 - <b>`time`</b> (float):  The time, in ms, at which the potential should be evaluated 
 - <b>`positions`</b> (list[float], optional):  The positions, in microns, at which the potential should be evaluated 



**Returns:**
 
 - <b>`list[float]`</b>:  The potential energies, in kHz, at the specified positions 

---

<a href="../../oqtant/schemas/optical.py#L652"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_width`

```python
get_width(time: 'float') → float
```

Method to calculate the Barrier object width at the specified time 



**Args:**
 
 - <b>`times`</b> (float):  The time, in ms, at which the height is calculated 



**Returns:**
 
 - <b>`float`</b>:  The barrier width at the specified time 

---

<a href="../../oqtant/schemas/optical.py#L636"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `get_widths`

```python
get_widths(times: 'list[float]') → list[float]
```

Method to calculate the Barrier object widths at the specified times 



**Args:**
 
 - <b>`times`</b> (list[float]):  The times, in ms, at which the heights are calculated 



**Returns:**
 
 - <b>`list[float]`</b>:  The barrier widths at the specified times 

---

<a href="../../oqtant/schemas/optical.py#L571"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `is_active`

```python
is_active(time: 'float') → bool
```

Method to determine if a Barrier object is active (exists) at the specified time 



**Args:**
 
 - <b>`time`</b> (float):  The time, in ms, at which the query is evaluated 



**Returns:**
 
 - <b>`bool`</b>:  Flag indicating if the barrier exists or not at the specified time 

---

<a href="../../oqtant/schemas/optical.py#L460"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>classmethod</kbd> `new`

```python
new(
    position: 'float' = 0,
    height: 'float' = 0,
    width: 'float' = 1,
    birth: 'float' = 0,
    lifetime: 'float' = 0,
    shape: 'ShapeType' = <ShapeType.GAUSSIAN: 'GAUSSIAN'>,
    interpolation: 'InterpolationType' = <InterpolationType.LINEAR: 'LINEAR'>
) → Barrier
```

Method to create a new Barrier object 



**Args:**
 
 - <b>`position`</b> (float, optional):  Position for the barrier 
 - <b>`height`</b> (float, optional):  Height for the barrier 
 - <b>`width`</b> (float, optional):  Width for the barrier 
 - <b>`birth`</b> (float, optional):  The time, in ms, at which the barrier will start being projected 
 - <b>`lifetime`</b> (float, optional):  Lifetime of the barrier 
 - <b>`shape`</b> (bert_schemas.job.ShapeType, optional):  Shape of the barrier 
 - <b>`interpolation`</b> (bert_schemas.job.InterpolationType, optional):  Interpolation type of the barrier 



**Returns:**
 
 - <b>`Barrier`</b>:  A new Barrier object 

---

<a href="../../oqtant/schemas/optical.py#L709"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_dynamics`

```python
show_dynamics() → None
```

Method to plot the position, width and height of a Barrier object over time 

---

<a href="../../oqtant/schemas/optical.py#L756"><img align="right" style="float:right;" src="https://img.shields.io/badge/-source-cccccc?style=flat-square"></a>

### <kbd>method</kbd> `show_potential`

```python
show_potential(
    times: 'list[float]' = [0.0],
    xlimits: 'list[float]' = [-61.0, 61],
    ylimits: 'list[float]' = [-1.0, 101],
    include_ideal: 'bool' = False
) → None
```

Method to plot the potential energy as a function of position for a Barrier object 



**Args:**
 
 - <b>`times`</b> (list[float], optional):  The times, in ms, at which the potential is evaluated 
 - <b>`xlimits`</b> (list[float], optional):  Plot limits for x axis 
 - <b>`ylimits`</b> (list[float], optional):  Plot limits for y axis 
 - <b>`include_ideal`</b> (bool, optional):  Flag for including target potential in plot 




---

_This file was automatically generated via [lazydocs](https://github.com/ml-tooling/lazydocs)._
