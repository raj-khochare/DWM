#apirori ( python )
from itertools import combinations
class Apriori:
    def __init__(self, min_support=0.5, min_confidence=0.6):
        self.min_support = min_support
        self.min_confidence = min_confidence
        self.frequent_itemsets = {}
        self.rules = []

    def get_support(self, itemset, transactions):
        count = sum(1 for transaction in transactions if itemset.issubset(transaction))
        return count / len(transactions)

    def join_sets(self, prev_frequent, k):
        candidates = set()
        prev_list = list(prev_frequent)
        for i in range(len(prev_list)):
            for j in range(i + 1, len(prev_list)):
                union = prev_list[i].union(prev_list[j])
                if len(union) == k:
                    candidates.add(frozenset(union))
        return candidates

    def fit(self, transactions):
        items = set(item for transaction in transactions for item in transaction)
        current_frequent = {frozenset([item]) for item in items}

        k = 1
        while current_frequent:
            valid_frequent = set()
            for itemset in current_frequent:
                support = self.get_support(itemset, transactions)
                if support >= self.min_support:
                    valid_frequent.add(itemset)
                    self.frequent_itemsets[itemset] = support
            k += 1
            current_frequent = self.join_sets(valid_frequent, k)

        return self.frequent_itemsets

    def generate_rules(self):
        for itemset in self.frequent_itemsets:
            if len(itemset) < 2:
                continue  # Need at least 2 items for a rule

            for i in range(1, len(itemset)):
                for antecedent in combinations(itemset, i):
                    antecedent = frozenset(antecedent)
                    consequent = itemset - antecedent

                    if consequent:
                        support = self.frequent_itemsets[itemset]
                        confidence = support / self.frequent_itemsets.get(antecedent, 1e-9)
                        lift = confidence / self.frequent_itemsets.get(consequent, 1e-9)

                        if confidence >= self.min_confidence:
                            self.rules.append({
                                "antecedent": set(antecedent),
                                "consequent": set(consequent),
                                "support": round(support, 3),
                                "confidence": round(confidence, 3),
                                "lift": round(lift, 3)
                            })
        return self.rules

transactions = [
    {"milk", "bread", "butter"},
    {"bread", "butter", "jam"},
    {"milk", "bread"},
    {"milk", "bread", "butter", "jam"},
    {"bread", "butter"}
]
ap = Apriori(min_support=0.5, min_confidence=0.7)
frequent_sets = ap.fit(transactions)
rules = ap.generate_rules()

print("Frequent Itemsets:")
for itemset, support in frequent_sets.items():
    print(f"{set(itemset)} → support = {round(support, 3)}")

print("\nAssociation Rules:")
for rule in rules:
    print(f"{rule['antecedent']} → {rule['consequent']} "
          f"(support={rule['support']}, confidence={rule['confidence']}, lift={rule['lift']})")