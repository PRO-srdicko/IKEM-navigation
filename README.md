# IKEM-navigation

## json structure

### points
id: randomly generated ID
coords: [x, y, floor]
    x: horizontal in plan
    y: vertical in plan
    floor [-2, ..., 4]
type: from `point_types`

#### points types
lobby: the main entrance
corridor: walkthrough points, should not be targets
door: should be targets
elevator,
staircase: have special properties in pathfinding

### paths
id: randomly generated ID
from,
to: point IDs
mobility: from `mobility_types`
message: a text description of the directions

#### mobility types


