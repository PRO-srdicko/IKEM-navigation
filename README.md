# IKEM-navigation

## json structure

### points
id: randomly generated ID
coords: [x, y, floor]
    x: horizontal in plan
    y: vertical in plan, [0, 0] is top left corner
    floor [-2, ..., 4]
type: from `point_types`
description: 

#### points types
0: corridor: walkthrough points, should not be targets
1: door: should be targets
    "di-base"
2: elevator:
    "floor"

### paths
id: randomly generated ID
from,
to: point IDs
mobility: from `mobility_types`
message: a text description of the directions

#### mobility types
    "mobility_types": [
        "no_restrictions",
        "steep_incline",
        "stairs"
    ],

