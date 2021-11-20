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
corridor: walkthrough points, should not be targets
door: should be targets
    "di-base"
elevator:
    "floor"

### paths
id: randomly generated ID
from,
to: point IDs
mobility: from `mobility_types`
message: a text description of the directions

#### mobility types


