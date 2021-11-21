import json, math, sys

def loadMap(name):    
    f = open (name, "r")
    openedMap = json.loads(f.read())
    return openedMap

def getDistance (points, p1, p2):
    a = (points[str(p1)]["coords"][0], points[str(p1)]["coords"][0])
    b = (points[str(p2)]["coords"][0], points[str(p2)]["coords"][0])
    x = a[0] - b[0]
    y = a[1] - b[1]
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
    solved = False
    while not solved:
        if len(halda) == 0:
            break
        halda.sort(key=takeSecond, reverse=True)
        zpracuj, budik = halda.pop()
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
                if score[b] == 0:
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
            minimum = sys.maxsize
            minimumPoint = -1
            minimumLine = -1
            for x in paths.keys():
                if int(paths[str(x)]["from"]) == zpracuj or int(paths[str(x)]["to"]) == zpracuj:
                    if paths[str(x)]["from"] == zpracuj:
                        b = paths[str(x)]["to"]
                    else:
                        b = paths[str(x)]["from"]
                    if score[b] > 0 and score[b] < minimum:
                        minimum = distance
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

mapPath = "map_2.json"
loadedMap = loadMap(mapPath)

findPath(loadedMap, 5, 27)

exit()

for x in range(150):
    findPath(loadedMap, 5, x)
