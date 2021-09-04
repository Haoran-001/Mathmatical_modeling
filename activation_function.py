import numpy as np
from matplotlib import pyplot as plt

def sigma(beta, x): 
    return 1.0 / (1 + np.e ** (-beta * x))

x = np.arange(-10, 10, 0.01)
tanh = (np.e ** x - np.e ** (-x)) / (np.e ** x + np.e ** (-x))



y1 = x * sigma(1, x)
y2 = y1 + sigma(1, x) * (1 - y1)
# y2 = x * sigma(5, x)
# y3 = x * sigma(10, x)
# y4 = x * sigma(0.2, x)
plt.title('swish activation and its derivative')
plt.xlabel('x')
plt.ylabel('y')
swish_graph, = plt.plot(x, y1, 'b-')
swish_diff_graph, = plt.plot(x, y2, 'g--')

plt.legend(handles = [swish_graph, swish_diff_graph], labels = ['Swish', 'Swish\'s derivative'], loc = 'best')
# plt.plot(x, y2, 'r-')
# plt.plot(x, y3, 'g-')

# plt.plot(x, y4, 'y-')
plt.grid()

plt.show()
