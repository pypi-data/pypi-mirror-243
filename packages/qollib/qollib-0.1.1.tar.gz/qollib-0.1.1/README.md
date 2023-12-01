# QoLlib

A Quality of Life (QoL) library that accumulates useful tools, hacks and such.

# Usage Examples
All available methods are available from the code documentation. 
Below we only highlight specific use-cases that need a bit more attention. 

Please be also invited to have a look at the unit tests ( `/tests` folder) for further code examples.

## Processing
To run code (quasi-)parallel in multiple processes or threads the `threaded` and `simultaneous` methods 
from the `processing` package remove a lot of overhead. 

Given a method that we want to execute in parallel 
```python
def long_running_calculation(num: float) -> float:
    # omitted for readability 
    pass 
```

we can simply call:
```python
simultaneous(long_running_calculation, [42, 1337, 3.141, 5, 6, 123.456, 1e-6])
```

However, common use case is that the ordering of concurrently generated results is important. 
E.g., when processing individual rows in an image. A simple trick to achieve this is to return a `tuple` from the 
processing method.

```python
import numpy as np 

def rotate_row(data: tuple) -> tuple:
    """
    | 0          | 1             | 2
    | row number | rot mat       | row data
    dat = (row: int,     rot: np.array, stokes: np.array)
    :return: (row: int, rotated_row: np.array)
    """
    rotated = np.zeros_like(data[2]).T
    for col in range(data[2].shape[1]):
        rotated[col] = np.dot(data[1], data[2][:, col])
    return data[0], rotated
```

Once our result is in this form, we can re-establish the ordering after execution by transforming the 
result into a `dict`: 

```python
args = [(row, rot, frame[:, row]) for row in range(frame.shape[1])]
res = dict(simultaneous(rotate_row, args))
rotated = np.array([res[r] for r in range(frame.shape[1])])
```

Also, when working with classes, the executing method must be accessible from outside the instance scope. 
This is best achieved with using `@staticmethod`s. 

```python
class ExampleClass:
    # ... lots of implementation details parallelize  
    @staticmethod
    def parallelize(args):
        pass

simultaneous(ExampleClass.parallelize, args)
```

## Strings
When dealing with user input it is neat to allow users to specify shapes for numpy arrays as strings in 
the common numpy format, e.g., `[13:37, :, 42]`. To extract the `tuple` of `slices` to forward this to numpy 
we provide the `parse_shape(str)` method: 

```python
data = np.arrange(10, 10)
roi = parse_shape('[1,2:4]')
print(data[roi])
#=> [12, 13]
```