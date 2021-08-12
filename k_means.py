import numpy as np
from matplotlib import pyplot as plt
import math
import random
import pandas as pd

# randomly generate n 2dimension points
def generate_points(n: int = 100) -> list:
    points = []
    i = 0
    while (i < n):
        point_np = np.random.randint(0, 100, (1, 2))
        point_np = point_np[0]

        point = []
        point.append(point_np[0])
        point.append(point_np[1])

        if point not in points:
            points.append(point)
            i += 1

    return points

# K-Means Algorithm
class KMeans:
    def __init__(self, points: list = None, groups: int = 3, times: int = 10):
        self.points = points
        self.groups = groups
        self.times = times
        self.center_points = self.generate_k_original_center()
        self.points_group = self.generate_k_original_pointset()

    def get_euclidean_distance(self, x: list, y: list) -> int:
        distance = math.sqrt(math.pow(y[1] - x[1], 2) + math.pow(y[0] - x[0], 2))
        return distance

    def generate_k_original_center(self) -> list:
        center_points = []

        i = 0
        while (i < self.groups):
            point = np.random.randint(0, 100, (1, 2))[0]
            center_point = []
            center_point.append(point[0])
            center_point.append(point[1])
            if center_point not in center_points:
                center_points.append(center_point)
                i += 1

        return center_points

    def generate_k_original_pointset(self) -> list:
        points_groups = [[] for i in range(self.groups)]
        for one_point in self.points:
            one_point_distances = [self.get_euclidean_distance(one_point, center_point) for center_point in self.center_points]
            min_distance = min(one_point_distances)
            min_index = one_point_distances.index(min_distance)
            points_groups[min_index].append(one_point)


        return points_groups

    def iterate_n_times(self) -> list:
        index = 0
        while index < self.times:
            for i in range(len(self.center_points)):
                avg_center_point = [0, 0]
                # avg_center_point[0] = sum([x[0] for x in self.points_group[i]]) / len(self.points_group[i])
                # avg_center_point[1] = sum([x[1] for x in self.points_group[i]]) / len(self.points_group[i])
                for one_point_index in range(len(self.points_group[i])):
                    avg_center_point[0] = (one_point_index) / (one_point_index + 1) * avg_center_point[0] + self.points_group[i][one_point_index][0] / (one_point_index + 1)
                    avg_center_point[1] = (one_point_index) / (one_point_index + 1) * avg_center_point[1] + self.points_group[i][one_point_index][1] / (one_point_index + 1)
                self.center_points[i] = avg_center_point
            index += 1

            self.points_group = self.generate_k_original_pointset()

        return self.points_group

# K-Means++ Algorithm
# 初始的点不是随机选取，而是k个点之间的间隔距离尽可能大
class KMeansPlus(KMeans):
    def __init__(self, points: list = None, groups: int = 3, times: int = 10):
        KMeans.__init__(self, points, groups, times)
        self.center_points = []
        self.center_points.append(random.choice(self.points))
        for i in range(1, self.groups):
            max_distance = -1
            for one_point in self.points:
                temp_distance = sum([self.get_euclidean_distance(one_point, center_point) for center_point in self.center_points])
                if temp_distance > max_distance:
                    max_distance = temp_distance
                    cur_point = one_point
            self.center_points.append(cur_point)
            print(self.center_points)

def main():
    # orginal points
    # generate 2000 points
    points = generate_points(2000)
    plt.subplot(121)
    plt.scatter([point[0] for point in points], [point[1] for point in points])
    plt.title('original points')
    plt.xlabel('x axis')
    plt.ylabel('y axis')

    # current points after K-Means or K-Means++
    kmeans = KMeansPlus(points = points, groups= 4, times = 20)
    points_group = kmeans.iterate_n_times()

    # visualization
    points_group_np = np.asarray([np.asarray(point_group) for point_group in points_group])

    x_set = []
    y_set = []
    label_set = []
    label_i = 0
    for point_group in points_group_np:
        for elem in point_group:
            x_set.append(elem[0])
            y_set.append(elem[1])
            # add category label
            label_set.append(label_i)
        label_i += 1


    df = pd.DataFrame(dict(x_set = np.asarray(x_set), y_set = np.asarray(y_set), category = label_set))
    print(df)
    colors = {0: 'red', 1: 'green', 2: 'blue', 3: 'yellow'}
    plt.subplot(122)
    plt.scatter(df['x_set'], df['y_set'], c = df['category'].map(colors))
    plt.title('points after K-Means algorithm')
    plt.xlabel('x axis')
    plt.ylabel('y axis')
    plt.show()



if __name__ == '__main__':
    main()