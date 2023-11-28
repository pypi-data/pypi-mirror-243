import numpy as np

class TrainTestSplit:
    def __init__(self, test_size=0.2, random_state=None):
        self.test_size = test_size
        self.random_state = random_state

    def split(self, X, y):
        if X.shape[0] != len(y):
            raise ValueError("The number of datapoints in X must be equal to the number of labels in y!")

        if self.random_state is not None:
            np.random.seed(self.random_state)

        indices = np.arange(X.shape[0])
        np.random.shuffle(indices)

        test_size = int(self.test_size * X.shape[0])
        test_indices, train_indices = indices[:test_size], indices[test_size:]

        X_train, X_test = X[train_indices], X[test_indices]
        y_train, y_test = y[train_indices], y[test_indices]

        return X_train, X_test, y_train, y_test

class Accuracy:
    @staticmethod
    def accuracy_score(y_true, y_pred):
        if len(y_true) != len(y_pred):
            raise ValueError("Input arrays must have the same length.")

        correct_predictions = np.sum(y_true == y_pred)
        total_samples = len(y_true)

        accuracy = correct_predictions / total_samples
        return accuracy
    
class MeanSquaredError:
    def __init__(self):
        pass

    @staticmethod
    def calculate(y_true, y_pred):
        if len(y_true) != len(y_pred):
            raise ValueError("Input arrays must have the same length.")
        
        squared_errors = [(true - pred) ** 2 for true, pred in zip(y_true, y_pred)]
        mean_squared_error = sum(squared_errors) / len(y_true)
        
        return mean_squared_error
    
class ConfusionMatrix:
    def __init__(self, num_classes):
        
        self.num_classes = num_classes
        self.matrix = np.zeros((num_classes, num_classes), dtype=int)

    def update(self, y_true, y_pred):
        
        for true_label, pred_label in zip(y_true, y_pred):
            self.matrix[true_label, pred_label] += 1

    def get_matrix(self):
        
        return self.matrix
    
    def calculate_recall(self, class_label):
        
        true_positive = self.matrix[class_label, class_label]
        false_negative = np.sum(self.matrix[class_label, :]) - true_positive
        recall = true_positive / (true_positive + false_negative) if (true_positive + false_negative) != 0 else 0
        return recall

    def calculate_precision(self, class_label):
        
        true_positive = self.matrix[class_label, class_label]
        false_positive = np.sum(self.matrix[:, class_label]) - true_positive
        precision = true_positive / (true_positive + false_positive) if (true_positive + false_positive) != 0 else 0
        return precision

    def calculate_f1_score(self, class_label):
        
        recall = self.calculate_recall(class_label)
        precision = self.calculate_precision(class_label)
        f1_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) != 0 else 0
        return f1_score
    
class PreProcessing:
    def __init__(self):
        self
    def scale_features(self, X):
        min_vals = np.min(X, axis=0)
        max_vals = np.max(X, axis=0)
        scaled_X = (X - min_vals) / (max_vals - min_vals)
        return scaled_X
    
    def normalize(self, X):
        means = np.mean(X, axis=0)
        stds = np.std(X, axis=0)
        normalized_X = (X - means) / stds
        return normalized_X