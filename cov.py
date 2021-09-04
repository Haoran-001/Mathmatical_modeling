import numpy as np

if __name__ == '__main__':
    # 每一行代表一个样本, 每一列代表一个维度
    sample = [[47., 30, 2], [11, 39, 17], [30, 46, 40], [24, 36, 0], [44, 8, 6],
                [38, 20, 10], [22, 46, 9], [0, 45, 30], [41, 20, 13], [22, 44, 9]]
    mysample = np.array(sample)
    # 计算每一个维度的平均值
    avgs_len = mysample.shape[1]
    avgs = np.zeros(avgs_len)

    for i in range(avgs_len):
        avgs[i] = np.mean(mysample[:, i])

    mysample_center = mysample.copy()
    for i in range(avgs_len):
        mysample_center[:, i] = mysample_center[:, i] - avgs[i]

    cov_matrix = np.zeros((avgs_len, avgs_len))

    samples_num = mysample.shape[0]
    for i in range(avgs_len):
        for j in range(avgs_len):
            cov_matrix[i, j] = 1 / (samples_num - 1) * np.sum(mysample_center[:, i] * mysample_center[:, j])

    print(cov_matrix)