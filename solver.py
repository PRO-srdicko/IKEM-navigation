import json, math, sys
import numpy as np

from construct_instructions import construct_instructions

def loadMap(name):    
    f = open (name, "r", encoding='utf-8')
    openedMap = json.loads(f.read())
    return openedMap

def getDistance (points, p1, p2):
    x = points[str(p1)]["coords"][0] - points[str(p2)]["coords"][0]
    y = points[str(p1)]["coords"][1] - points[str(p2)]["coords"][1]
    s = x*x+y*y
    if (s <= 0): return -1
    return math.sqrt(s)

def takeSecond(elem):
    return elem[1]

def findPath(loadedMap, start, end):
    print("Pathfinding from", start, "to", end)
    points = loadedMap["points"]
    paths = loadedMap["lines"]

    halda = [[start, 0]]
    score = [0] * len(points)
    score[start] = 1
    solved = False
    while not solved:
        if len(halda) == 0:
            break
        halda.sort(key=takeSecond, reverse=True)
        zpracuj, budik = halda.pop()
        #print(zpracuj, budik)
        if (zpracuj == end):
            solved = True
            break
        
        for x in paths.keys():
            if int(paths[str(x)]["from"]) == zpracuj or int(paths[str(x)]["to"]) == zpracuj:
                #print(paths[str(x)])
                if paths[str(x)]["from"] == zpracuj:
                    b = paths[str(x)]["to"]
                else:
                    b = paths[str(x)]["from"]
                if score[b] == 0 and zpracuj != b:
                    distance = int(10*getDistance(points, zpracuj, b))
                    if (distance > 0):
                        halda.append([b, budik + distance])
                        score[b] = budik + distance
    print("Solved:", solved, "     Lenght", score[end])

    if solved:
        found = False
        zpracuj = end
        pathPoints = [end]
        pathLines = []
        while not found:
            #input()
            #print(zpracuj)
            minimum = sys.maxsize
            minimumPoint = -1
            minimumLine = -1
            for x in paths.keys():
                if int(paths[str(x)]["from"]) == zpracuj or int(paths[str(x)]["to"]) == zpracuj:
                    if paths[str(x)]["from"] == zpracuj:
                        b = paths[str(x)]["to"]
                    else:
                        b = paths[str(x)]["from"]
                    #print(b, score[b])
                    if score[b] > 0 and score[b] < minimum and zpracuj != b:
                        minimum = score[b]
                        minimumPoint = b
                        minimumLine = x
            if minimumPoint == -1 or minimumLine == -1:
                break

            pathPoints.append(minimumPoint)
            pathLines.append(minimumLine)

            if minimumPoint == start:
                found = True
            else:
                zpracuj = minimumPoint

        if found:
            pathPoints.reverse()
            pathLines.reverse()

        print("Path:", found)
        print("PathPoints:", pathPoints)
        print("PathLines:", pathLines)

        return pathPoints, pathLines

def lines_to_paths(map, point_ids, line_ids):
    paths = []
    line = map["lines"][line_ids[0]]
    from_point = map['points'][str(point_ids[0])]
    if from_point.get('description') is None:
        from_point['description'] = from_point['d']
    to_point = map['points'][str(point_ids[1])]
    if to_point.get('description') is None:
        to_point['description'] = to_point['d']
    paths.append({
        "id": line['id'],
        'from': from_point,
        'to': to_point,
        'angle': None,
        'length': getDistance(map['points'], from_point['id'], to_point['id']),
        'description': line['d1'] if from_point['id'] < to_point['id'] else line['d2']
    })
    for i, line_id in enumerate(line_ids[1:]):
        prev_line = line
        line = map["lines"][line_id]
        from_point = to_point
        to_point = map['points'][str(point_ids[i+2])]
        if to_point.get('description') is None:
            to_point['description'] = to_point['d']
        paths.append({
            "id": line['id'],
            'from': from_point,
            'to': to_point,
            'angle': compute_angle(prev_line, line, map['points']),
            'length': getDistance(map['points'], from_point['id'], to_point['id']),
            'description': line['d1'] if from_point['id'] < to_point['id'] else line['d2']
        })

    return paths


def compute_angle(line1, line2, points):
    v1 = compute_vector(line1, points)
    v2 = compute_vector(line2, points)
    return np.degrees(np.arctan2(v2[1], v2[0]) - np.arctan2(v1[1], v1[0]))


def compute_vector(line, points):
    vector = np.array(points[str(line["to"])]['coords'][:2]) - \
        np.array(points[str(line["from"])]['coords'][:2])
    return vector

if __name__ == '__main__':
    mapPath = "map_3.json"
    loadedMap = loadMap(mapPath)

    point_ids, line_ids = findPath(loadedMap, 36, 27)

    paths = lines_to_paths(loadedMap, point_ids, line_ids)
    print(paths)

    instructions = construct_instructions(paths)
    print(instructions)

