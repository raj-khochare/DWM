#Agglomerative Clustering (PYTHON)
import math
import itertools
class AgglomerativeClustering:
    def __init__(self, n_clusters=2):
        self.n_clusters = n_clusters
        self.clusters = []
    def euclidean_distance(self, p1, p2):
        return math.sqrt(sum((a - b) ** 2 for a, b in zip(p1, p2)))
    def fit(self, X):
        self.clusters = [[x] for x in X]
        while len(self.clusters) > self.n_clusters:
            min_distance = float("inf")
            cluster_to_merge = (None, None)
            for (i, c1), (j, c2) in itertools.combinations(enumerate(self.clusters), 2):
                distance = min(self.euclidean_distance(p1, p2) for p1 in c1 for p2 in c2)
                if distance < min_distance:
                    min_distance = distance
                    cluster_to_merge = (i, j)
            i, j = cluster_to_merge
            new_cluster = self.clusters[i] + self.clusters[j]
            self.clusters = [c for idx, c in enumerate(self.clusters) if idx not in (i, j)]
            self.clusters.append(new_cluster)
        return self.clusters
X = [
    [1.0, 2.0],
    [1.5, 1.8],
    [5.0, 8.0],
    [8.0, 8.0],
    [1.0, 0.6],
    [9.0, 11.0]
]
hc = AgglomerativeClustering(n_clusters=2)
final_clusters = hc.fit(X)
for idx, cluster in enumerate(final_clusters):
    print(f"Cluster {idx+1}: {cluster}")
