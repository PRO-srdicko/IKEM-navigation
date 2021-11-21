# IKEM-navigation

# Running the solver

The python code is only prepared as a library and for a test output you can run `python solver.py`. The module requires `numpy` installed.

## json structure

### points
id: automatically generated ID
coords: [x, y, floor]
    x: horizontal in plan
    y: vertical in plan, [0, 0] is top left corner
    floor [-2, ..., 5]
type: from `point_types`
description: free human-understandable text

#### points types
0: corridor: walkthrough points, should not be targets
1: door: should be targets
2: elevator: used to connect floors

### paths
id: randomly generated ID
from,
to: points
mobility: from `mobility_types` (unused for now)
description: a text description of the directions

#### mobility types
    "mobility_types": [
        "no_restrictions",
        "steep_incline",
        "stairs"
    ],

