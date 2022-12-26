import numpy as np

if __name__ == "__main__":
    x = np.array([1,2,3,4,5,6])
    print(x)
    x = np.append(x,[7,8,9,10])
    print(x)
    print(x.size)