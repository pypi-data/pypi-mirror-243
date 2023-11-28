#!python
#cython: language_level=3
from libc.math cimport sqrt, sin, cos


ctypedef fused tlist: # Tuple or list
    list
    tuple


cpdef bint naive_eq(list p1, list p2):
    """Perform naive check for equality, used for testing"""
    cdef int i, n
    if len(p1) != len(p2):
        return False
    else:
        n = len(p1)
        for i in range(n):
            x1, y1 = p1[i]
            x2, y2 = p2[i]
            if x1 != x2 or y1 != y2:
                return False
        return True


cpdef list affine_transform(list polygon, tlist mat):
    """Transform polygon using matrix.

    Args:
        polygon (List): Input polygon
        mat (Tuple[int, int, int, int, int, int]):
            6 elements [a, b, c, d, e, f] of the affine matrix,
            the element is considered rowwise, i.e. [[a, b, c], [d, e, f]].
    """
    cdef list new = []
    cdef double x, y, x2, y2
    for x, y in polygon:
        x2 = x * mat[0] + y * mat[1] + mat[2]
        y2 = x * mat[3] + y * mat[4] + mat[5]
        new.append((x2, y2))
    return new


cpdef list scale(list poly, double scalex, double scaley):
    """Scale polygon coordinates

    Args:
        polygon (List[Tuple[float, float]]): The input polygon.
        scalex (float): x scaling
        scaley (float): y scaling
    """
    cdef double x = 0
    cdef double y = 0
    cdef list new = []
    for x, y in poly:
        new.append((x * scalex, y * scaley))
    return new


cpdef list rotate(list poly, double radian):
    """Rotate polygon coordinates, this is NOT center rotation.
    To center rotate a polygon, translate to its center first.

    Args:
        polygon (List[Tuple[float, float]]): The input polygon.
        radian (float): Angle to rotate the polygon
    """
    cdef double s = sin(radian)
    cdef double c = cos(radian)
    cdef list new = []
    for x, y in poly:
        new.append((x * c - y * s, x * s + y * c))
    return new


cpdef list translate(list poly, double tx, double ty):
    """Scale polygon coordinates

    Args:
        polygon (List[Tuple[float, float]]): The input polygon.
        scalex (float): x scaling
        scaley (float): y scaling
    """
    cdef double x = 0
    cdef double y = 0
    cdef list new = []
    for x, y in poly:
        new.append((x + tx, y + ty))
    return new


cpdef double get_area(list poly):
    """Calculate area of a polygon. The area is signed.

    Args:
        poly:
            List of tuple representing x, y points.
            Numpy arrays of shape [P, 2] would do too.

    References:
        https://en.wikipedia.org/wiki/Polygon#Area
    """
    cdef int n = len(poly)
    cdef int i
    cdef double area, x1, y1, x2, y2
    area = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        area += x1 * y2 - x2 * y1
    area /= 2
    return area


cpdef double get_perimeter(list poly):
    """Calculate the perimeter of a polygon.

    Args:
        poly:
            List of tuple representing x, y points.
            Numpy arrays of shape [P, 2] would do too.

    References:
        https://en.wikipedia.org/wiki/Polygon#Area
    """
    cdef int i, n
    cdef double peri, x1, y1, x2, y2
    n = len(poly)
    peri = 0
    for i in range(n):
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]
        peri += ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
    return peri


cpdef list offset(list poly, double offset_value, long ccw = 1):
    # +-------------------+
    # | Deffing variables |
    # +-------------------+
    cdef double scale = 1000.0
    cdef long m = len(poly)
    cdef long n = m
    cdef long i = 0
    cdef double x1, y1, x2, y2, vx, vy
    cdef list offset_lines = []
    cdef list new_poly = []

    # +--------------------------------------------------+
    # | If the polygon is clock wise, offset is reversed |
    # +--------------------------------------------------+
    offset_value = offset_value * scale
    if ccw == 0:
        offset_value = -offset_value

    # +----------------------+
    # | Offset polygon edges |
    # +----------------------+
    for i in range(n):
        # == Line endpoints ==
        x1, y1 = poly[i]
        x2, y2 = poly[(i + 1) % n]

        # == Skip collided points ==
        if x1 == x2 and y1 == y2:
            m = m - 1
            continue

        # == Rescale to reduce double point errors ==
        x1 = x1 * scale
        x2 = x2 * scale
        y1 = y1 * scale
        y2 = y2 * scale

        # == Calculate the direction vector & normal vector ==
        vx, vy = x2 - x1, y2 - y1
        vx, vy = vy, -vx

        # == normalize the normal vector ==
        length = (vx**2 + vy**2) ** 0.5
        vx, vy = vx / length, vy / length

        # == offset endpoints along the normal to create offset lines ==
        x1 = x1 + vx * offset_value
        y1 = y1 + vy * offset_value
        x2 = x2 + vx * offset_value
        y2 = y2 + vy * offset_value
        offset_lines.append((x1, y1, x2, y2))

    # +--------------------------------------------------------------+
    # | Find intersections                                           |
    # | New poly vertices are the intersection of the offset lines   |
    # | https://en.wikipedia.org/wiki/Line%E2%80%93line_intersection |
    # +--------------------------------------------------------------+
    cdef double deno
    for i in range(m):
        (x1, y1, x2, y2) = offset_lines[i]
        (x3, y3, x4, y4) = offset_lines[(i + 1) % m]
        deno = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
        if deno == 0:
            continue
        x = ((x1 * y2 - y1 * x2) * (x3 - x4) - (x1 - x2) * (x3 * y4 - x4 * y3)) / deno
        y = ((x1 * y2 - y1 * x2) * (y3 - y4) - (y1 - y2) * (x3 * y4 - x4 * y3)) / deno
        new_poly.append((x / scale, y / scale))

    return new_poly
