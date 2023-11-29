#!python
#cython: language_level=3, boundscheck=False
cimport cython
from cpython cimport array
from cpython.array cimport array as array_t
import array

ctypedef fused num_array_t:
    list
    tuple
    array.array
    float[:]
    int[:]
    long[:]
    double[:]


cpdef float get_iou(num_array_t box1, num_array_t box2):
    """
    Calculate the Intersection over Union (IoU) between two bounding boxes.

    Args:
        box1 (List[float]): The [x1, y1, x2, y2] coordinates of the first box.
        box2 (List[float]): The [x1, y1, x2, y2] coordinates of the second box.

    Returns:
        iou (float): The IoU between the two boxes.
    """
    cdef float x1_inter = max(box1[0], box2[0])
    cdef float y1_inter = max(box1[1], box2[1])
    cdef float x2_inter = min(box1[2], box2[2])
    cdef float y2_inter = min(box1[3], box2[3])

    # Check intersection
    cdef float width_inter = max(0, x2_inter - x1_inter)
    cdef float height_inter = max(0, y2_inter - y1_inter)
    cdef float iou = 0.0
    if width_inter <= 0 or height_inter <= 0:
        return iou

    # Calculate IoU
    cdef float area_inter = width_inter * height_inter
    cdef float area_box1 = (box1[2] - box1[0]) * (box1[3] - box1[1])
    cdef float area_box2 = (box2[2] - box2[0]) * (box2[3] - box2[1])
    cdef float area_union = area_box1 + area_box2 - area_inter
    iou = area_inter / area_union
    return iou

cpdef tuple argsort(num_array_t x, bint desc = False):
    """Get sort permutation

    Args:
        x (list): Array to be sorted
        desc (bool): Sort descending

    Returns:
        args (list): List of sorting indices
    """
    # == Declarations ==
    cdef int n = len(x)
    cdef int i = 0
    cdef bint swap
    cdef list args = list(range(n))
    cdef list x_copy = [item for item in x]

    # == Loop through items ==
    for prv in range(n):
        for nxt in range(prv + 1, n):
            # == Check for swapping ==
            if desc:
                swap = x_copy[prv] < x_copy[nxt]
            else:
                swap = x_copy[prv] > x_copy[nxt]

            # == Swap elements ==
            if swap:
                args[prv], args[nxt] = args[nxt], args[prv]
                x_copy[prv], x_copy[nxt] = x_copy[nxt], x_copy[prv]
    return x_copy, args

cpdef list nms(list boxes, num_array_t scores, float iou_threshold):
    """Non max suppression"""
    # +--------------+
    # | Declarations |
    # +--------------+
    cdef int n = len(boxes)
    cdef int i, j

    # +------------------------------------------+
    # | Sort score and boxes by score descending |
    # +------------------------------------------+
    cdef int[:] indices = array.array('i', range(n))
    cdef float[:] scores_arr = array.array('f', scores)
    for i in range(n):
        for j in range(i + 1, n):
            if scores_arr[i] < scores_arr[j]:
                scores_arr[i], scores_arr[j] = scores_arr[j], scores_arr[i]
                indices[i], indices[j] = indices[j], indices[i]

    # +----------------------------------------------------------------+
    # | Suppress non-max by marking                                    |
    # | 0: keep, 1: remove, it helps not having to negate during loops |
    # | This version is faster because it allocate less, does not beat |
    # | the pytorch version though, they used some black magic         |
    # +----------------------------------------------------------------+
    cdef int[:] mark = array.array('i', [0] * n)
    cdef list box1, box2
    for i in range(n):
        # == Check removed ==
        if mark[i] == 1:
            continue

        for j in range(i + 1, n):
            # == Check removed ==
            if mark[j] == 1:
                continue

            # == Compute iou and mark for removal if needed ==
            box1 = boxes[indices[i]]
            box2 = boxes[indices[j]]
            if get_iou(box1, box2) > iou_threshold:
                mark[j] = 1

    # +------------------------------------+
    # | Filter out all the removed indices |
    # +------------------------------------+
    return [indices[i] for i in range(n) if mark[i] == 0]


def get_iou_matrix(boxes1, boxes2, bint symetric = False):
    """Compute iou matrix between two bounding set of boxes

    Args:
        boxes1 (list): list of xyxy bounding boxes.
        boxes2 (list): list of xyxy bounding boxes.
        symetric (bool): is boxes1 the same as boxes2, default false.
    """
    cdef int m = len(boxes1)
    cdef int n = len(boxes2)
    cdef int i, j
    cdef float iou
    cdef list ious = [[0 for j in range(n)] for i in range(m)]

    for i in range(m):
        # +-----------------------------------------+
        # | If symetric, do not calculate iou twice |
        # +-----------------------------------------+
        if symetric:
            j_range = range(i + 1, n)
            ious[i][i] = 1
        else:
            j_range = range(n)

        # +------------------------------+
        # | Compute iou with other boxes |
        # +------------------------------+
        for j in j_range:
            # Compute IoU
            iou = get_iou(list(boxes1[i]), list(boxes2[j]))

            # set iou, mirror if symetric
            ious[i][j] = iou
            if symetric:
                ious[j][i] = iou

    return ious

