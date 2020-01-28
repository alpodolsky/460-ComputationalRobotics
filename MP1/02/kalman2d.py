import sys
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":

    # Retrive file name for input data
    if(len(sys.argv) < 5):
        print(
            "Four arguments required: python kalman2d.py [datafile] [x1] [x2] [lambda]")
        exit()

    filename = sys.argv[1]
    x10 = float(sys.argv[2])
    x20 = float(sys.argv[3])
    scaler = float(sys.argv[4])

    # Read data
    lines = [line.rstrip('\n') for line in open(filename)]
    data = []
    for line in range(0, len(lines)):
        data.append(list(map(float, lines[line].split(' '))))

    # Print out the data
    print("The input data points in the format of 'k [u1, u2, z1, z2]', are:")
    for it in range(0, len(data)):
        print(str(it + 1) + ": ", end='')
        print(*data[it])

    # Identity matrices
    I = np.identity(2)
    print("\nMatrix I : \n", I)
    H = np.identity(2)
    print("\nMatrix a : \n", H)
    C = np.identity(2)
    print("\nMatrix a : \n", C)

    Q = [[10**-4, 2*10**-5], [2*10**-5, 10**-4]]
    print(Q)

    R = [[10**-2, 5*10**-3], [5*10**-3, 2*10**-2]]
    print(R)

    deltaT = 0
    # the for loop works just make sure you set the range till end of file
    for deltaT in range(0,len(data)):
        A = [[1, deltaT], [0, 1]]
        B = [[((1/2)*(deltaT**2))], [deltaT]]
        
        x = [[x10], [x20]]
        u = [[0],[0]]
        u.pop(0)
        u.insert(0, data[deltaT][0])

        Xkp = (A*x) + (B*u) + Q

        P0 = scaler * I

        Pkp = (A*P0*(np.transpose(A))) + Q

        num = Pkp + np.transpose(H)
        denom = (H * Pkp * np.transpose(H)) + R

        K = num/denom

        x = [[x10 + 1], [x20 + 1]]

        Z = [[0], [0]]
        for i in range(0, len(data)):
            Z[i][2].pop(2)
            Z[i][2].insert(2, data[i][2])

            Z[i][3].pop(3)
            Z[i][3].insert(3, data[i][3])

        Yk = (C * x) + Z

        Xk = Xkp + K * (Yk - (H*Xkp))

        plt.scatter(x10, Xk) 
  
 
# plot title 
plt.title('Kalman Filter') 
  
# function to show the plot 
plt.show() 
