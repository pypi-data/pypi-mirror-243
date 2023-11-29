## Simpoly

A package for simple polygon operations.

#### Usage

Here's a quick guide on how to use the package
```python
# +-------------------------------------------+
# | Import package and define example polygon |
# +-------------------------------------------+
import simpoly
import math
polygon = [[0, 0], [0, 1], [-1, 1]]

# +---------------------------+
# | Rotate polygon by radians |
# +---------------------------+
simpoly.rotate(polygon, math.pi/2)

# +----------------------------------------+
# | Translate (x, y) coordinates by (1, 2) |
# +----------------------------------------+
simpoly.translate(polygon, 1, 2)

# +---------------------------------------+
# | Scale (x, y) coordinates by (100, 10) |
# +---------------------------------------+
simpoly.scale(polygon, 100, 10)

# +-----------------------------------------------------------+
# | Get area (signed) and perimeter of polygon                |
# | The area is positive if the polygon is counter clockwise  |
# +-----------------------------------------------------------+
area = simpoly.get_area(polygon) # signed area
simpoly.get_perimeter(polygon)

# +------------------------------------------------------------------------------+
# | Offset polygon edges by some distance.                                       |
# | Positive distance expands the polygon, negative distance shrinks it.         |
# | The 3rd parameter specify if the polygon is counter clockwise (ccw),         |
# | it is assumed that the polygon is ccw by default, if the polygon is not      |
# | ccw, the distance's sign will be change so that the behaviour is consistent. |
# | One can use get_area to check if the polygon is counter clockwise.           |
# +------------------------------------------------------------------------------+
simpoly.offset(polygon, 1, area >= 0)

# +----------------------------------------------------------------+
# | Apply affine transformation to polygon, the second argument    |
# | [a, b, c, d, e, f] is equivalent to the transformation matrix: |
# |     [ a b c ]                                                  |
# |     [ d e f ]                                                  |
# +----------------------------------------------------------------+
simpoly.affine_transform(polygon, [1, 0, 1, 0, 1, -2]) # offset by [1, -2]
```

There are also some bounding box utilities in here:
```python
import random
from pprint import pprint
from simpoly import bbox_utils

# +-------------------+
# | Generate examples |
# +-------------------+
def rand_boxes(n):
    bounding_boxes = []
    for _ in range(n):
        x_min = random.randint(0, 100)
        y_min = random.randint(0, 100)
        x_max = random.randint(x_min + 1, 200)
        y_max = random.randint(y_min + 1, 200)
        bounding_boxes.append([x_min, y_min, x_max, y_max])
    return bounding_boxes

boxes = rand_boxes(5)

# Compute IoU / Batch IoU
iou = bbox_utils.get_iou(boxes[0], boxes[1])
print("IoU(b[1], b[1])", iou)

# Compute IoU / Batch IoU
ious = bbox_utils.get_iou_matrix(boxes, boxes, symetric=True)
ious = [["%.4f" % x for x in row] for row in ious]
pprint(ious)

# Non max suppression
# Boxes must be list of list
keep = bbox_utils.nms(boxes, [1.0] * 5, iou_threshold=0.5)
print("Keep", keep)
```
