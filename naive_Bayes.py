#Naive Bayes
import math
from collections import defaultdict

class NaiveBayes:
    def __init__(self):  # Fixed constructor
        self.feature_counts = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
        self.class_counts = defaultdict(int)
        self.total_samples = 0

    def train(self, X, y):
        for i in range(len(X)):
            label = y[i]
            self.class_counts[label] += 1
            self.total_samples += 1

            for j in range(len(X[i])):
                feature = f"feature{j}"
                value = X[i][j]
                self.feature_counts[label][feature][value] += 1

    def predict(self, x):
        best_prob = float("-inf")
        best_class = None

        for label in self.class_counts:
            # Prior probability (log)
            log_prob = math.log(self.class_counts[label] / self.total_samples)

            # Likelihoods
            for j in range(len(x)):
                feature = f"feature{j}"
                value = x[j]

                feature_count = self.feature_counts[label][feature].get(value, 0)
                total_feature_count = sum(self.feature_counts[label][feature].values())
                vocab_size = len(self.feature_counts[label][feature])

                # Laplace smoothing
                prob = (feature_count + 1) / (total_feature_count + vocab_size)
                log_prob += math.log(prob)

            if log_prob > best_prob:
                best_prob = log_prob
                best_class = label

        return best_class


# Example data
X = [
    ["Sunny", "Hot"],
    ["Sunny", "Mild"],
    ["Overcast", "Hot"],
    ["Rainy", "Mild"],
    ["Rainy", "Cool"],
    ["Overcast", "Cool"],
    ["Sunny", "Cool"],
    ["Rainy", "Hot"]
]
y = ["No", "No", "Yes", "Yes", "Yes", "Yes", "No", "Yes"]

nb = NaiveBayes()
nb.train(X, y)

test = ["Sunny", "Cool"]
print("Predicted Class:", nb.predict(test))

