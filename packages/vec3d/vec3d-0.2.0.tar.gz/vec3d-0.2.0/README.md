# Vector3D library
> Helper library with Math and graphing related functions for vectors in the 3D space

## Usage

Install the library by typing:

```bash
python -m pip install vec3d
```

Once installed, you'll have access to the Maths and graphing package:

```python
from vec3d.graph import (
    Arrow3D,
    Colors3D,
    Points3D,
    draw3d,
)

from vec3d.math import cross, subtract

u = (3, -2, 2)
v = (2, 4, 3)

draw3d(
    Arrow3D(u, color=Colors3D.RED),
    Arrow3D(v, color=Colors3D.CYAN),
    Arrow3D(cross(u, v), color=Colors3D.PURPLE),
    Points3D(u, color=Colors3D.RED),
    Points3D(v, color=Colors3D.CYAN),
    Points3D(cross(u, v), color=Colors3D.PURPLE),
    elev=15
)
```

## See Also

See also [vec2d](https://pypi.org/project/vec2d/) for a similar library for vectors on the 2D plane.


## Acknowledgements

This library is a small refactoring of https://github.com/orlandpm/Math-for-Programmers library.
