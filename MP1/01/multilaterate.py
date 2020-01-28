import sys
import numpy as np
import math

def multilaterate(distances):
    rows=4
    cols=4
    #a matrix
    a=[[1 for i in range(cols)] for j in range(rows)]
    #b vector(distance vector)
    b=[]
    #have to do things by the row to fill the array as:
    # x y z coeff d
    for i in range(0, len(distances)):
        #x coord
        a[i].pop(1)
        a[i].insert(1, -2*distances[i][0])

        #y coord
        a[i].pop(2)
        a[i].insert(2, -2*distances[i][1])

        #z coord
        a[i].pop(3)
        a[i].insert(3, -2*distances[i][2])
        #print(a[i])

        #distance^2 - xi^2 - yi^2 -zi^2
        b.append(pow(distances[i][3],2)-pow(distances[i][0],2)-pow(distances[i][1],2)-pow(distances[i][2],2))
        #print(b[i])
    np.linalg.cond(a)
    #matrix and vectors are filled, solve for x vector           
    x = np.linalg.solve(a,b)
    #returns x y z
    q= [x[1], x[2], x[3]]
    
    return q

if __name__ == "__main__":
    
    # Retrive file name for input data
    if(len(sys.argv) == 1):
        print("Please enter data file name.")
        exit()
    
    filename = sys.argv[1]

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    distances = []
    for line in range(0, len(lines)):
        distances.append(list(map(float, lines[line].split(' '))))

    # Print out the data
    print ("The input four points and distances, in the format of [x, y, z, d], are:")

    for p in range(0, len(distances)):
        print (*distances[p]) 

    # Call the function and compute the location 
    location = multilaterate(distances)
    print 
    print ("The location of the point is: " + str(location))
