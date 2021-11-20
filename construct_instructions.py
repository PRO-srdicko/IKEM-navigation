import numpy as np
from copy import copy


def compute_angle(path1, path2):
    v1 = compute_vector(path1)
    v2 = compute_vector(path2)
    return np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))


def compute_vector(path):
    vector = np.array(points[path["to"]]['coords'][:2]) - \
        np.array(points[path["from"]]['coords'][:2])
    return vector


angles = {
    range(-180, -160): "behind you",
    range(-160, -120): "sharp left",
    range(-120, -60): "left",
    range(-60, -20): "slight left",
    range(-20, 20): "in front of you",
    range(20, 60): "slight right",
    range(60, 120): "right",
    range(120, 160): "sharp right",
    range(160, 181): "behind you",
}


def angle_to_text(angle):
    for angle_range in angles:
        if angle in angle_range:
            return angles[angle_range]

# points = load_points()
# [] to {id: point}
# add list of all neighbours (ids)

# Validate
# Each door has at least 1 corridor neihbour
# If door has more than 1 Corridor neihbour, paths to Cs, must have Descriptions


points = {0: {'id': 0, 'coords': [0, 0, 2], 'type': 0, 'description': "Test"}, 10: {'id': 10, 'coords': [
    0, 10, 2], 'type': 1, 'description': "Test2"}, 11: {'id': 11, 'coords': [10, 10, 2], 'type': 2, 'description': ""}}


def is_turn(path):
    if path["angle"] is None:
        return False
    return path["angle"] > 20 or path["angle"] < -20


def is_anchor(point):
    anchor_true = (
        (point["type"] == 0 and len(point["description"]) > 0) or
        (point["type"] == 1 and len(point["description"]) > 0) or
        (point["type"] == 2)
    )
    return anchor_true


# def resolve_turn_anchor(paths):
#     instruction = ""
#     if len(points[paths[-1]["to"]]["description"]) > 0:
#         return
#     if len(paths[-1]["description"]) > 0:
#         return f'Head {angle_to_text(paths[-1]["angle"])} towards {paths[-1]["description"]}'


def resolve_last(path):
    instruction = f"Look {angle_to_text(path['angle'])} and"
    if len(path["description"]) > 0:
        instruction += f" towards {path['description']}"
    instruction += " you'll find"
    if len(points[path['to']]['description']) > 0:
        instruction += f" {points[path['to']]['description']}."
    else:
        instruction += " it."
    return instruction


def resolve_first(path):
    """
    Examples:
    From the main entrace start by heading towards 'Blok B'.
    Start by having the door behind you.
    """
    instruction = ""
    from_point = points[path['from']]
    to_point = points[path["to"]]
    if len(from_point['description']) > 0:
        instruction += f"From the {from_point['description']} start by"
    else:
        instruction += f"Start by"

    if len(path["description"]) > 0:
        instruction += f" heading towards {path['description']}"
        if len(to_point['description']) > 0:
            instruction += f" to get to {to_point['description']}."
        else:
            instruction += '.'
    else:
        # theres only 1 corridor to go to
        if to_point['type'] == 0:
            instruction += ' having the door behind you'
            if len(to_point['description']) > 0:
                instruction += f" and get to {to_point['description']}."
            else:
                instruction += '.'
        # we are in a room
        if to_point['type'] == 1:
            instruction += ' going out through door '
            if len(to_point['description']) > 0:
                instruction += f" {to_point['description']}."
            else:
                instruction += f" {to_point['number']}."
        # we go straight to elevator
        if to_point['type'] == 2:
            instruction += f" taking the elevator "
            if len(to_point['description']) > 0:
                instruction += f" {to_point['description']}."
            else:
                instruction += f" {to_point['number']}."
    return instruction


def resolve_inter(paths):
    instructions = []

    for i, path in enumerate(paths):
        if not is_anchor(path) and not is_turn(path):
            # maybe some counters should be here
            continue
        instruction = ""
        from_point = points[path['from']]
        to_point = points[path["to"]]
        if is_turn(path):
            instruction += f"Take a {angle_to_text(path['angle'])} turn"
        else:
            instruction += f"Continue"
        if len(path['description']) > 0:
            instruction += f" through {path['description']}"
        else:
            instruction += ""
        # theres a named corridor
        if to_point['type'] == 0:
            assert len(to_point['description']) > 0
            instruction += f" towards {to_point['description']}."
        # Theres a named door that is not final
        if to_point['type'] == 1:
            assert len(to_point['description']) > 0
            instruction += f" through door {to_point['description']}."
        # Theres an elevator
        if to_point['type'] == 2:
            # and we go from elevator
            if from_point['type'] == 2:
                instruction += f" with an elevator to floor {from_point['level']}."
            else:
                instruction += f" taking the elevator "
                if len(to_point['description']) > 0:
                    instruction += f" {to_point['description']}."
                else:
                    instruction += f" {to_point['number']}."
        instructions.append(instruction)

    return instructions


def instructions_to_text(instructions):
    return " ".join(instructions)


def construct_instructions(paths):
    instructions = []

    assert len(paths) > 0

    if len(paths) == 1:
        return [resolve_last(paths[0])]

    instructions.append(resolve_first(paths[0]))

    instructions.extend(resolve_inter(paths[1:-1]))

    instructions.append(resolve_last(paths[-1]))

    return instructions_to_text(instructions)


if __name__ == "__main__":
    paths = [
        {
            "id": 0,
            "from": 0,
            "from_type": 0,
            "to": 10,
            "to_type": 1,
            "angle": None,
            "length": 10,
            "mobility": 0,
            "message": "k pavilonu B"
        },
        {
            "id": 1,
            "from": 10,
            "to": 11,
            "mobility": 0,
            "message": "k pavilonu A"
        }
    ]

    print(construct_instructions(paths, points))
