import numpy as np


class KNN:
    def __init__(self,k=3,distance_metric="Euclidean",custom_distance=None):
        if not isinstance(k, int) or k <= 0:
            raise ValueError("k must be a positive integer.")
        if distance_metric not in ['Euclidean', 'Manhattan'] and custom_distance is None:
            raise ValueError("Invalid distance metric! Available distance metrics are 'Euclidean' and 'Manhattan' and you can provide your own distance function too.")
        self.k=k
        self.x_train = None
        self.y_train = None
        self.distance_metric=distance_metric
        self.custom_distance = custom_distance
    
    def fit(self, X_train, Y_train):
        if not isinstance(X_train, np.ndarray) or not isinstance(Y_train, np.ndarray):
            raise ValueError("The training data must be NumPy arrays!")
        if X_train.shape[0] != len(Y_train):
            raise ValueError("The number of datapoints in the input training data must be equal to the number of datapoints in the output training data!")
        if X_train.shape[1] == 0:
            raise ValueError("The training dataset must have at least one Dimension!")
        self.x_train=X_train
        self.y_train=Y_train
        
    def predict(self,X_test):
        if self.x_train is None or self.y_train is None:
            raise ValueError("Call the fit function on the training dataset before calling on the predict function!")
        if not isinstance(X_test, np.ndarray):
            raise ValueError("The test data must be a NumPy array!")
        if X_test.shape[1] != self.x_train.shape[1]:
            raise ValueError("The number of features in X_test must match the number of features in X_train!")
        y_pred=[self._predict(x) for x in X_test]
        return y_pred
    
    def _predict(self,x):
        
        distances = [self.distance(x, x_train) for x_train in self.x_train]
        k_indices=np.argsort(distances)[:self.k]
        k_nearest_labels = [self.y_train[i] for i in k_indices]
        unique_labels, counts = np.unique(k_nearest_labels, return_counts=True)
        majority_class = unique_labels[np.argmax(counts)]

        return majority_class
        
    def distance(self,x1,x2):
        if not isinstance(x1, np.ndarray) or not isinstance(x2, np.ndarray):
            raise ValueError("Input vectors must be NumPy arrays.")
        if x1.shape != x2.shape:
            raise ValueError("Input vectors must have the same shape.")
        
        if self.custom_distance is not None:
            return self.custom_distance(x1, x2)
        
        if self.distance_metric=='Euclidean':
            return np.sqrt(np.sum((x1-x2)**2))
        else:
            return np.sum(np.abs(x1-x2))


