import numpy as np

class PCA():
    def __init__(self, matrix: np.ndarray):
        self.matrix = matrix
        self.k = k

    def get_result(self) -> np.ndarray:
        # 对每个数据的每一个分量求均值
        # 这里用每一列表示一个数据, 每一行表示一个字段
        # 求均值
        mean_matrix = np.mean(matrix, axis = 0)
        # 减去平均值
        data_adjust = self.matrix - mean_matrix
        # 计算协方差矩阵和特征值和特征向量
        # cov_matrix = np.cov(data_adjust, rowvar = 0)
        cov_matrix = 1 / data_adjust.shape[0] * np.matmul(data_adjust.T, data_adjust)
        eig_values, eig_vectors = np.linalg.eig(cov_matrix)
        # 对特征值进行排序
        eig_values_index = np.argsort(eig_values)
        # 保留前k个最大的特征值
        eig_values_index = eig_values_index[:-(1000000):-1]
        # 计算出对应的特征向量
        true_eig_vectors = eig_vectors[:, eig_values_index]
        # 选择较大特征值对应的特征向量
        max_vector_eigval = true_eig_vectors[:, 0]
        pca_result = np.matmul(max_vector_eigval, data_adjust.T)

        return pca_result

if __name__ == '__main__':
    matrix = np.array([[1, 1], [1, 3], [2, 3], [4, 4], [2, 4]])
    pca = PCA(matrix)
    print(pca.get_result())
