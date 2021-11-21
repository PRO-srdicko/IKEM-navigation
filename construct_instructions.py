import numpy as np
from copy import copy


angles = {
    # Take a "" turn
    'turn': {
    range(-180, -160): "very sharp left",
    range(-160, -120): "sharp left",
    range(-120, -60): "left",
    range(-60, -20): "slight left",
    range(-20, 20): "in front of you",
    range(20, 60): "slight right",
    range(60, 120): "right",
    range(120, 160): "sharp right",
    range(160, 180): "very sharp right",
    },
    # Look ""
    'look': {
    range(-180, -160): "behind you on your left",
    range(-160, -120): "sharp left",
    range(-120, -60): "left",
    range(-60, -20): "slight left",
    range(-20, 20): "in front of you",
    range(20, 60): "slight right",
    range(60, 120): "right",
    range(120, 160): "sharp right",
    range(160, 180): "behind you on your right",
    }
}


def angle_to_text(angle, type='turn'):
    for angle_range in angles[type]:
        if np.floor(angle) in angle_range:
            print(angle_range)
            print(angles[type][angle_range])
            return angles[type][angle_range]

# points = load_points()
# [] to {id: point}
# add list of all neighbours (ids)

# Validate
# Each door has at least 1 corridor neihbour
# If door has more than 1 Corridor neihbour, paths to Cs, must have Descriptions
# No x->x lines 


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
    instruction = f"Look {angle_to_text(path['angle'], 'look')} and"
    if len(path["description"]) > 0:
        instruction += f" towards {path['description']}"
    instruction += " you'll find"
    if len(path['to']['description']) > 0:
        instruction += f" {path['to']['description']}."
    else:
        instruction += " your destination."
    return instruction


def resolve_first(path):
    """
    Examples:
    From the main entrace start by heading towards 'Blok B'.
    Start by having the door behind you.
    """
    instruction = ""
    from_point = path['from']
    to_point = path["to"]
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

    m_from_anchor = 0
    for i, path in enumerate(paths):
        if not is_anchor(path['to']) and not is_turn(path):
            m_from_anchor += path['length'] / 500
            continue
        m_from_anchor = 0
        instruction = ""
        from_point = path['from']
        to_point = path["to"]
        if m_from_anchor < 5:
            instruction += "Almost immediately" if np.random.rand() > 0.5 else "Right away"
        else:
            instruction += f"After about {m_from_anchor} meters"
        if is_turn(path):
            instruction += f" take a {angle_to_text(path['angle'], 'turn')} turn"
        else:
            instruction += f" continue"
        if len(path['description']) > 0:
            instruction += f" through {path['description']}"
        else:
            instruction += ""
        if is_anchor(to_point):
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
        else:
            instruction += "."
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
    pass
