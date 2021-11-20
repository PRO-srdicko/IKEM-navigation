import numpy as np
from copy import copy

angles = {
    range(-180, -160): "behind you",
    range(-160, -120): "sharp left",
    range(-120, -60): "left",
    range(-60, -20): "slight left",
    range(-20, 20): "in front of you",
    range(20, 60): "slight right",
    range(60, 120): "right",
    range(120, 160): "sharp right",
    range(160, 181): "behind you"
}  

def angle_to_text(angle, locale='en'):
    for angle_range in angles:
        if angle in angle_range:
            return angles[angle_range]

# points = load_points()

points = {0: {'id': 0, 'coords': [0, 0, 2], 'type': 0}, 10: {'id': 10, 'coords': [
    0, 10, 2], 'type': 1}, 11: {'id': 11, 'coords': [10, 10, 2], 'type': 2}}


def to_next_anchor(paths):
    for i, path in enumerate(paths):
        # turns are anchor points
        if path["angle"] > 20 or path["angle"] < -20:
            return paths[:i+1]
        # named corridor points are anchor points
        if points[path["to"]]["type"] == 0 and len(points[path["to"]]["description"]) > 0:
            return paths[:i+1]
        # named doors are anchor points
        if points[path["to"]]["type"] == 0 and len(points[path["to"]]["description"]) > 0:
            return paths[:i+1]
        # elevators are anchor points
        if points[path["to"]]["type"] == 2:
            return paths[:i+1]


def resolve_turn_anchor(paths):
    instruction = ""
    if len(paths[-1]["description"]) > 0:
        return f'Head {angle_to_text(paths[-1]["angle"])} towards {paths[-1]["description"]}'


def compute_angle(path1, path2):
    v1 = compute_vector(path1)
    v2 = compute_vector(path2)
    return np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))


def compute_vector(path):
    vector = np.array(points[path["to"]]['coords'][:2]) - \
        np.array(points[path["from"]]['coords'][:2])
    return vector


def construct_instructions(paths):
    instructions = []

    for i, path in enumerate(paths):
        instruction = ""
        if i == 0:
            instruction = f"From {path['from']}"
        m = path["message"]
        if len(m) > 0:
            if i > 0:
                a = compute_angle(paths[i-1], paths[i])
                if a < -20:
                    instruction = f'Continue left to {m}'
                elif a > 20:
                    instruction = f'Continue right to {m}'
                else:
                    instruction = f"Continue to {m}"
        instructions.append(instruction)

    return instructions


if __name__ == "__main__":
    paths = [
        {
            "id": 0,
            "from": 0,
            "from_type": 0,
            "to": 10,
            "to_type": 1,
            "angle": 90,
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

    print(construct_instructions(paths))
