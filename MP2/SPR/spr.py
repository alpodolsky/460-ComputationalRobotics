import sys
import numpy as np
from collections import defaultdict

'''
Report reflexive vertices
'''


def findReflexiveVertices(polygons):
    vertices = []
    # Your code goes here
    # You should return a list of (x,y) values as lists, i.e.
    # vertices = [[x1,y1],[x2,y2],...]

    # look at each polygon
    for i in range(0, len(polygons)):
        # auto promote polygons made of 3 points to reflexvertices
        if(len(polygons[i]) == 3):
            for k in range(0, len(polygons[i])):
                vertices.append(polygons[i][k])
        else:
            for j in range(0, len(polygons[i])):
                # last point
                if j == len(polygons[i])-1:
                    a = np.array(polygons[i][len(polygons[i])-2])
                    b = np.array(polygons[i][j])
                    c = np.array(polygons[i][0])
                    angle = np.degrees(np.arctan2(
                        c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0]))
                    if angle < 180 and angle > 0:
                        vertices.append(polygons[i][j])
                        break
                    if angle < 0 and angle < -180:
                        vertices.append(polygons[i][j])
                        # print(angle)
                        #print (a,b,c)
                        #print("added to the list")
                        break
                    # print(angle)
                    #print (a,b,c)
                    #print("not added to the list")
                    # print()
                    break
                # everything from first point to second to last
                else:
                    a = np.array(polygons[i][j-1])
                    b = np.array(polygons[i][j])
                    c = np.array(polygons[i][j+1])
                    angle = np.degrees(np.arctan2(
                        c[1]-b[1], c[0]-b[0]) - np.arctan2(a[1]-b[1], a[0]-b[0]))
                    if angle < 180 and angle > 0:
                        vertices.append(polygons[i][j])
                        continue
                    if angle < 0 and angle < (-180):
                        vertices.append(polygons[i][j])
                        continue

    return vertices


'''
Compute the roadmap graph
'''


def computeSPRoadmap(polygons, reflexVertices):
    vertexMap = dict()
    adjacencyListMap = defaultdict(list)

    # Your code goes here
    # You should check for each pair of vertices whether the
    # edge between them should belong to the shortest path
    # roadmap.
    #
    # Your vertexMap should look like
    # {1: [5.2,6.7], 2: [9.2,2.3], ... }

    # this also needs to check if reflex points between polygons can connect
    for i in range(0, len(reflexVertices)):
        vertexMap[i+1] = reflexVertices[i]
    # and your adjacencyListMap should look like
    # {1: [[2, 5.95], [3, 4.72]], 2: [[1, 5.95], [5,3.52]], ... }
    #
    # The vertex labels used here should start from 1

    # look at each reflex vertex
    for i in range(0, len(reflexVertices)):
        # grabs current pair
        currPair = reflexVertices[i]
        print("current pair:", currPair)
        #gets to the right shape
        k=0
        while currPair not in polygons[k]:
            k+=1
        #lines up the coord
        m=0
        while polygons[k][m]!=currPair:
            m+=1
        #set up stuff relevant for searching    
        nextP = m+1
        if m == len(polygons[k])-1:
            nextP = 0
        prevP = nextP-2
        #if prev point is not in reflex then nextP one is
        if polygons[k][prevP] not in reflexVertices:
            print("prev point not reflexive")
            x1 = currPair[0]
            y1 = currPair[1]
            x2 = polygons[k][nextP][0]
            y2 = polygons[k][nextP][1]
            print(polygons[k][nextP])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            idk = 0
            while polygons[k][nextP]!= reflexVertices[idk]:
                idk+=1
            adjacencyListMap[i+1].append([idk+1, distance])
            #find the next reflex by going forwards
            count = 0
            while reflexVertices[count] not in polygons[k] or reflexVertices[count]==currPair:
                count-=1
            x1 = currPair[0]
            y1 = currPair[1]
            x2 = reflexVertices[count][0]
            y2 = reflexVertices[count][1]
            print(reflexVertices[count])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            
            adjacencyListMap[i+1].append([abs(count+1), distance])    
            #find the last reflexVertex that also belongs to that polygon
            
        #oppisite of first case
        if polygons[k][nextP] not in reflexVertices:
            print("next point not reflexive")
            #calculates the line between the two consecutive reflex's
            count = 0
            print(polygons[k][nextP])
            while polygons[k][nextP] not in reflexVertices or polygons[k][nextP]==currPair:
                if nextP==len(polygons[k])-1:
                    nextP=0
                else:
                    nextP +=1
            x1 = currPair[0]
            y1 = currPair[1]
            x2 = polygons[k][nextP][0]
            y2 = polygons[k][nextP][1]
            print(polygons[k][nextP])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            idk = 0
            while polygons[k][nextP] != reflexVertices[idk]:
                if idk == len(reflexVertices)-1:
                    idk = 0
                else:
                    idk+=1
            print(idk)
            adjacencyListMap[i+1].append([idk+1, distance])

            x1 = currPair[0]
            y1 = currPair[1]
            x2 = polygons[k][prevP][0]
            y2 = polygons[k][prevP][1]
            print(polygons[k][prevP])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            idk=0
            if(polygons[k][prevP])!=reflexVertices[idk]:
                while polygons[k][prevP] != reflexVertices[idk]:
                    idk+=1
                print(idk)
                adjacencyListMap[i+1].append([idk+1, distance])
            else:
                adjacencyListMap[i+1].append([idk+1, distance])
            continue
               
        
        #both reflexive
        if polygons[k][nextP] in reflexVertices and polygons[k][prevP] in reflexVertices:
            print("within both condition")
            x1 = currPair[0]
            y1 = currPair[1]
            x2 = polygons[k][prevP][0]
            y2 = polygons[k][prevP][1]
            print(polygons[k][prevP])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            idk = 0
            if(polygons[k][prevP])!=reflexVertices[idk]:
                while polygons[k][prevP] != reflexVertices[idk]:
                    idk+=1
                print(idk)
                adjacencyListMap[i+1].append([idk+1, distance])
            else:
                print(idk)
                adjacencyListMap[i+1].append([idk+1, distance])
            
            x1 = currPair[0]
            y1 = currPair[1]
            x2 = polygons[k][nextP][0]
            y2 = polygons[k][nextP][1]
            print(polygons[k][nextP])
            distance = np.sqrt(abs(x2 - x1)**2 + (abs(y2 - y1))**2)
            print("distance", distance)
            idk = 0
            if(polygons[k][nextP])!=reflexVertices[idk]:
                while polygons[k][nextP] != reflexVertices[idk]:
                    idk+=1
                print(idk)
                adjacencyListMap[i+1].append([idk+1, distance])
            else:
                print(idk)
                adjacencyListMap[i+1].append([idk+1, distance])
        continue
        
               

    return vertexMap, adjacencyListMap


'''
Perform uniform cost search 
'''


def uniformCostSearch(adjListMap, start, goal):
    path = []
    pathLength = 0

    # Your code goes here. As the result, the function should
    # return a list of vertex labels, e.g.
    #
    # path = [23, 15, 9, ..., 37]
    #
    # in which 23 would be the label for the start and 37 the
    # label for the goal.

    if start == goal:
        return path, pathLength

    # enter start in path
    path.append(start)
    pathLength = 0
    
    for i in range(0, len(adjListMap)):
        print(adjListMap[i])

    return path, pathLength


'''
Agument roadmap to include start and goal
'''


def updateRoadmap(polygons, vertexMap, adjListMap, x1, y1, x2, y2):
    updatedALMap = dict()
    startLabel = 0
    goalLabel = -1

    # Your code goes here. Note that for convenience, we
    # let start and goal have vertex labels 0 and -1,
    # respectively. Make sure you use these as your labels
    # for the start and goal vertices in the shortest path
    # roadmap. Note that what you do here is similar to
    # when you construct the roadmap.

    return startLabel, goalLabel, updatedALMap


if __name__ == "__main__":
    # Retrive file name for input data
    if(len(sys.argv) < 6):
        print(
            "Five arguments required: python spr.py [env-file] [x1] [y1] [x2] [y2]")
        exit()

    filename = sys.argv[1]
    x1 = float(sys.argv[2])
    y1 = float(sys.argv[3])
    x2 = float(sys.argv[4])
    y2 = float(sys.argv[5])

    # Read data and parse polygons
    lines = [line.rstrip('\n') for line in open(filename)]
    polygons = []
    for line in range(0, len(lines)):
        xys = lines[line].split(';')
        polygon = []
        for p in range(0, len(xys)):
            polygon.append([float(i) for i in xys[p].split(',')])
        polygons.append(polygon)

    # Print out the data
    print("Pologonal obstacles:")
    for p in range(0, len(polygons)):
        print(str(polygons[p]))
    print("")

    # Compute reflex vertices
    reflexVertices = findReflexiveVertices(polygons)
    print("Reflexive vertices:")
    print(str(reflexVertices))
    print("")

    # Compute the roadmap
    vertexMap, adjListMap = computeSPRoadmap(polygons, reflexVertices)
    print("Vertex map:")
    print(str(vertexMap))
    print("")
    print("Base roadmap:")
    print(dict(adjListMap))
    print("")

    # Update roadmap
    start, goal, updatedALMap = updateRoadmap(
        polygons, vertexMap, adjListMap, x1, y1, x2, y2)
    print("Updated roadmap:")
    print(dict(updatedALMap))
    print("")

    # Search for a solution
    path, length = uniformCostSearch(updatedALMap, start, goal)
    print("Final path:")
    print(str(path))
    print("Final path length:" + str(length))
