import numpy as np

def h(x, y):
    return 1 / (2 * np.pi) * (np.e ** (-(x ** 2 + y ** 2) / 2)) 

if __name__ == '__main__':
    sum = 0.0
    for i in range(-1, 2, 1):
        for j in range(-1, 2, 1):
            temp = np.round(h(i, j) / 0.7792, 4)
            print('h({0}, {1}) = {2}' .format(i, j, temp))
            sum += temp
    print(sum)