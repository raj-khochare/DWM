#PAGE RANK (python)
import numpy as np
class PageRank:
    def __init__(self, damping=0.85, max_iters=100, tol=1e-6):
        self.damping = damping
        self.max_iters = max_iters
        self.tol = tol
    def fit(self, adjacency_matrix):
        n = len(adjacency_matrix)
        M = np.zeros((n, n))
        for i in range(n):
            if adjacency_matrix[i].sum() == 0:
                M[i] = np.ones(n) / n
            else:
                M[i] = adjacency_matrix[i] / adjacency_matrix[i].sum()

        pr = np.ones(n) / n

        for _ in range(self.max_iters):
            new_pr = (1 - self.damping) / n + self.damping * np.dot(M.T, pr)

            if np.linalg.norm(new_pr - pr, 1) < self.tol:
                break
            pr = new_pr
        return pr
adjacency_matrix = np.array([
    [0, 1, 1],
    [0, 0, 1],
    [1, 0, 0]
])

pagerank = PageRank()
scores = pagerank.fit(adjacency_matrix)

print("PageRank Scores:")
for i, score in enumerate(scores):
    print(f"Page {i}: {score:.4f}")
