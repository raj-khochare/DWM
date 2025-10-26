#k means 
import random
import math

class KMeans:
    def __init__(self, k=2, max_iters=100):
        self.k = k
        self.max_iters = max_iters
        self.centroids = []

    def euclidean_distance(self, point1, point2):
        return math.sqrt(sum((x - y) ** 2 for x, y in zip(point1, point2)))

    def fit(self, X):
        self.centroids = random.sample(X, self.k)

        for _ in range(self.max_iters):
            clusters = [[] for _ in range(self.k)]

            for point in X:
                distances = [self.euclidean_distance(point, centroid) for centroid in self.centroids]
                cluster_idx = distances.index(min(distances))
                clusters[cluster_idx].append(point)

            new_centroids = []
            for cluster in clusters:
                if cluster:
                    new_centroids.append([sum(dim) / len(cluster) for dim in zip(*cluster)])
                else:
                    new_centroids.append(random.choice(X))

            self.centroids = new_centroids

    def predict(self, X):
        labels = []
        for point in X:
            distances = [self.euclidean_distance(point, centroid) for centroid in self.centroids]
            labels.append(distances.index(min(distances)))
        return labels


X = [
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0],
    [8.0, 2.0],
    [10.0, 2.0]
]

kmeans = KMeans(k=2)
kmeans.fit(X)

print("Final Centroids:", kmeans.centroids)
labels = kmeans.predict(X)
for point, label in zip(X, labels):
    print(f"Point {point} → Cluster {label}")
