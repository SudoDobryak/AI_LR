import numpy as np
import matplotlib.pyplot as plt


def loadDataSet(fileName):
    data = np.loadtxt(fileName, delimiter='\t')
    return data


def distEclud(x, y):
    return np.sqrt(np.sum((x - y) ** 2))


def randCent(dataSet, k):
    m, n = dataSet.shape

    centroids = np.zeros((k, n))
    for i in range(k):
        index = int(np.random.uniform(0, m))
        centroids[i, :] = dataSet[index, :]
    return centroids


def KMeans(dataSet, k):
    m = np.shape(dataSet)[0]
    clusterAssment = np.mat(np.zeros((m, 2)))
    clusterChange = True

    centroids = randCent(dataSet, k)
    while clusterChange:
        clusterChange = False

        for i in range(m):
            minDist = 100000.0
            minIndex = -1

            for j in range(k):
                distance = distEclud(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
            if clusterAssment[i, 0] != minIndex:
                clusterChange = True
                clusterAssment[i, :] = minIndex, minDist ** 2
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]
            centroids[j, :] = np.mean(pointsInCluster, axis=0)

    print("Congratulations,cluster complete!")
    return centroids, clusterAssment


def showCluster(dataSet, k, centroids, clusterAssment):
    m, n = dataSet.shape
    if n != 2:
        return 1

    mark = ['or', 'ob', 'og', 'ok', '^r', '+r', 'sr', 'dr', '<r', 'pr']
    if k > len(mark):
        return 1

    for i in range(m):
        markIndex = int(clusterAssment[i, 0])
        plt.plot(dataSet[i, 0], dataSet[i, 1], mark[markIndex])

    mark = ['Dr', 'Db', 'Dg', 'Dk', '^b', '+b', 'sb', 'db', '<b', 'pb']
    for i in range(k):
        plt.plot(centroids[i, 0], centroids[i, 1], mark[i])
    plt.show()


dataSet = loadDataSet("Data.txt")
k = 4
centroids, clusterAssment = KMeans(dataSet, k)
showCluster(dataSet, k, centroids, clusterAssment)
