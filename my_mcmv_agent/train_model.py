"""Script to train a simple decision tree model."""
import pickle
from sklearn.tree import DecisionTreeClassifier
import numpy as np


def main():
    # Synthetic data: renda, perfil_code, valor_venal
    X = np.array([
        [2000, 1, 80000],
        [3000, 2, 120000],
        [1500, 1, 60000],
        [5000, 3, 200000],
        [2500, 2, 90000],
        [1800, 0, 70000],
    ])
    y = np.array([1, 1, 0, 0, 1, 0])
    clf = DecisionTreeClassifier(max_depth=3)
    clf.fit(X, y)
    with open("model.pkl", "wb") as f:
        pickle.dump(clf, f)
    print("Modelo treinado e salvo em model.pkl")


if __name__ == "__main__":
    main()
