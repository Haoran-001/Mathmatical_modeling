import math
import random
import numpy as np
import matplotlib.pyplot as plt
from typing import *

class GA():
    def __init__(self, length, count):
        self.length = length    # 染色体的长度
        self.count = count      # 种群中染色体的数量
        self.popluation = self.gen_population(length, count)    # 随机生成的初始种群

    def evolve(self, retain_rate = 0.2, random_select_rate = 0.5, mutation_rate = 0.01):
        '''
        进化, 对当前一代种群一次进行选择，交叉并产生新一代种群，然后对新一代种群进行变异
        '''
        parents = self.selection(retain_rate, random_select_rate)
        self.crossover(parents)
        self.mutation(mutation_rate)

    def gen_chromoesome(self, length) -> int:
        '''
        随机生成长度为length的染色体，每个基因的取值是0或者1
        用1个bit表示一个基因
        '''
        chromosome = 0
        for i in range(length):
            chromosome |= (1 << i) * random.randint(0, 1)

        return chromosome

    def gen_population(self, length, count) -> List:
        '''
        获取初始种群(一个含有count个长度为length的染色体列表)
        '''
        return [self.gen_chromoesome(length) for i in range(count)]

    def fitness(self, chromosome) -> float:
        '''
        计算适应度, 将染色体解码在0-9之间的数字，带入函数计算
        因为是求最大值, 所以数值越大, 适应度越高
        '''
        x = self.decode(chromosome)
        return x + 10 * math.sin(5 * x) + 7 * math.cos(4 * x)

    def selection(self, retain_rate, random_select_rate) -> List:
        '''
        选择
        先对适应度从小到大排序，选出存活的染色体
        再进行随机选择，选出适应度虽然小，但是幸存下来的个体
        '''
        # 对适应度从小到大排序
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.popluation]
        graded = [x[1] for x in sorted(graded, reverse = True)]
        # 选出适应度强的染色体
        retain_length = int(len(graded) * retain_rate)
        parents = graded[:retain_length]
        # 选出是影响不强，但是幸存的染色体
        for chromosome in graded[retain_length:]:
            if random.random() < random_select_rate:
                parents.append(chromosome)

        return parents

    def crossover(self, parents):
        '''
        染色体的交叉, 反之，生成新一代的种群
        '''
        # 新出生的孩子，最终会被加入存活下来的父母之中，形成新一代的种群
        children = []
        target_count = len(self.popluation) - len(parents)
        # 开始根据需要的量进行繁殖
        while len(children) < target_count:
            male = random.randint(0, len(parents) - 1)
            female = random.randint(0, len(parents) - 1)
            if male != female:
                # 随机选择交叉点
                cross_pos = random.randint(0, self.length)
                # 生成掩码，方便位操作
                mask = 0
                for i in range(cross_pos):
                    mask |= (1 << i)
                male = parents[male]
                female = parents[female]
                # 孩子将获得父亲在交叉点前的基因和母亲在交叉点后的基因
                child = ((male & mask) | (female & ~mask)) & ((1 << self.length) - 1)
                children.append(child)

        self.popluation = parents + children

    def mutation(self, rate):
        '''
        变异, 对种群的所有个体，随机改变某个个体中的某个基因
        '''
        for i in range(len(self.popluation)):
            if random.random() < rate:
                j = random.randint(0, self.length - 1)
                self.popluation[i] ^= 1 << j

    def decode(self, chromosome) -> float:
        '''
        解码染色体, 将二进制转换成属于[0-9]的实数
        '''
        return chromosome * 9.0 / (2 ** self.length - 1)

    def result(self) -> float:
        '''
        获得当前代的最优值, 这里取的是函数最大值时候x的值
        '''
        graded = [(self.fitness(chromosome), chromosome) for chromosome in self.popluation]
        graded = [x[1] for x in sorted(graded, reverse = True)]
        return self.decode(graded[0])

def main():
    # 染色体长度为10，种群数量为30
    ga = GA(10, 30)
    # 存储每次迭代后的结果值
    res = []
    # 迭代10次
    for i in range(10):
        ga.evolve()
        res.append((i + 1, ga.result()))

    x = np.linspace(0, 9, 10000)
    y = x + 10 * np.sin(5 * x) + 7 * np.cos(4 * x)

    plt.subplot(121)
    plt.plot(x, y)
    res_x = ga.result()
    res_y = res_x + 10 * np.sin(5 * res_x) + 7 * np.cos(4 * res_x)
    plt.scatter(res_x, res_y, c = 'red')

    plt.subplot(122)
    plt.plot([item[0] for item in res], [item[1] for item in res])

    plt.show()
    print(ga.result())

if __name__ == '__main__':
    main()