"""
A library providing a few Math related utility functions for the 3D space.
"""
from math import acos, pi, sqrt
from typing import Sequence

# Type alias
IntOrFloat = int | float


def add(
    *vectors: tuple[IntOrFloat, IntOrFloat, IntOrFloat]
) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
    """Performs the addition of any given number of 3D vectors

    Args:
        *vectors ([tuple[IntOrFloat, IntOrFloat, IntOrFloat]]): variable number
            of 3D vectors designated by their Cartesian coordinates

    Raises:
        ValueError: If fewer than two vectors are provided.

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the vector sum
    """
    if len(vectors) < 2:
        raise ValueError("at least two 3D vectors were expected")

    zipped_by_coords = zip(*vectors)
    sum_by_coords = [sum(coords) for coords in zipped_by_coords]
    return tuple(sum_by_coords)


def scale(
    s: IntOrFloat, v: tuple[IntOrFloat, IntOrFloat, IntOrFloat]
) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
    """Performs the scalar product

    Args:
        s (IntOrFloat): the scalar
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the vector given its
            Cartesian coordinates

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the vector that result from
            multiplying the vector by the scalar.
    """
    return tuple(s * coord_component for coord_component in v)


def subtract(
    v, w: tuple[IntOrFloat, IntOrFloat, IntOrFloat]
) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
    """Calculates the result of subtracting the 3D vector w from the vector v.
    In other words, it returns the displacement vector from w to v.

    Args:
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the vector to subtract
            from, designated by its Cartesian coordinates.
        w (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the vector to be
            subtracted, designated by its Cartesian coordinates.)

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the displacement vector.
        That is the vector that result from subtracting w from v.
    """
    return tuple([v_c - w_c for v_c, w_c in zip(v, w)])


def length(v: tuple[IntOrFloat, IntOrFloat, IntOrFloat]) -> float:
    """Calculates the length of a 3D vector designated by its Cartesian
    coordinates.

    Args:
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the vector whose length
            is to be calculated, designated by its Cartesian coordinates.

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the length of the vector.
    """
    return sqrt(sum([coord**2 for coord in v]))


def dot(
    u: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
    v: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
) -> float:
    """Calculates the dot product of the given 3D vectors, given their Cartesian
    coordinates.

    Args:
        u (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the first vector
            designated byt its Cartesian coordinates.
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the second vector
            designated byt its Cartesian coordinates.

    Returns:
        float: the result of the dot product of u and v.
    """
    return sum((coord_u * coord_v) for coord_u, coord_v in zip(u, v))


def angle_between(
    u: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
    v: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
) -> float:
    """Calculates the angle between the given vectors

    Args:
        u (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the first vector
            designated byt its Cartesian coordinates.
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the second vector
            designated byt its Cartesian coordinates.

    Returns:
        float: the angle between u and v expressed in radians.
    """
    return acos(dot(u, v) / (length(u) * length(v)))


def to_radians(angle_deg: float) -> float:
    """Returns the radians value for an angle expressed in degrees.

    Args:
        angle_deg (float): the value of the angle express in degrees.

    Returns:
        float: the equivalent angle expressed in radians.
    """
    return angle_deg * pi / 180


def to_degrees(angle_rad: float) -> float:
    """Returns the degrees value for an angle expressed in radians.

    Args:
        angle_rad (float): the value of the angle express in radians.

    Returns:
        float: the equivalent angle expressed in degrees.
    """
    return angle_rad * 180 / pi


def cross(
    u: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
    v: tuple[IntOrFloat, IntOrFloat, IntOrFloat],
) -> tuple[IntOrFloat, IntOrFloat, IntOrFloat]:
    """Calculates the cross product of the given 3D vectors, given their
    Cartesian coordinates.

    Args:
        u (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the first vector
            designated byt its Cartesian coordinates.
        v (tuple[IntOrFloat, IntOrFloat, IntOrFloat]): the second vector
            designated byt its Cartesian coordinates.

    Returns:
        tuple[IntOrFloat, IntOrFloat, IntOrFloat]: the result of the cross
        product of u and v.
    """
    ux, uy, uz = u
    vx, vy, vz = v
    return (uy * vz - uz * vy, uz * vx - ux * vz, ux * vy - uy * vx)


def linear_combination(
    scalars: Sequence[float],
    *vectors: tuple[IntOrFloat, IntOrFloat, IntOrFloat]
):
    """Returns the linear combination of applying each of the scalars to the
    corresponding vectors in sequence. For example
    linear_combination([1, 2, 3], (1, 1, 1), (2, 2, 2), (3, 3, 3)) will return
    the vector (14, 14, 14).
    """
    if len(scalars) != len(vectors):
        raise ValueError("The same number of scalars and vectors are required")
    return add(*[scale(s, v) for s, v in list(zip(scalars, vectors))])


def unit(v: tuple[IntOrFloat, IntOrFloat, IntOrFloat]):
    """Returns a vector whose length is one that is oriented in the same
    direction as the one given."""
    return scale(1.0 / length(v), v)
