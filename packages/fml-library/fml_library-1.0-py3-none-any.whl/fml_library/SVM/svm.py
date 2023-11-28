import numpy as np

class Support_Vector_Machine:

    def __init__(self, learning_rate=0.001, lambda_param=0.01, no_of_iterations=1000, kernel=None):
        """
        Initializes the Support Vector Machine (SVM) with specified parameters.

        Parameters:
        - learning_rate: The learning rate for gradient descent.
        - lambda_param: The regularization parameter.
        - no_of_iterations: The number of iterations for training.
        - kernel: The kernel function to be used (default is linear).
        """
        self.learning_rate = learning_rate
        self.lambda_param = lambda_param
        self.no_of_iterations = no_of_iterations
        self.weights = None
        self.bias = None
        self.kernel = kernel_functions.linear

    def fit(self, X_train, y_train):
        """
        Fits the SVM model to the training data.

        Parameters:
        - X_train: The training features.
        - y_train: The training labels.
        """
        no_of_samples, no_of_features = X_train.shape

        # Initialize weights and bias
        self.weights = np.zeros(self.kernel(X_train[0]).shape[0])
        self.bias = 0

        # Training the SVM using gradient descent
        for itr in range(self.no_of_iterations):
            for i in range(no_of_samples):
                inside_boundary = y_train[i] * (np.dot(self.kernel(X_train[i]), self.weights) - self.bias) >= 1
                if inside_boundary:
                    self.weights -= self.learning_rate * (2 * self.lambda_param * self.weights)
                else:
                    self.weights -= self.learning_rate * (2 * self.lambda_param * self.weights - np.dot(self.kernel(X_train[i]), y_train[i]))
                    self.bias -= self.learning_rate * y_train[i]

    def predict(self, X_test):
        """
        Predicts the labels for the given test data.

        Parameters:
        - X_test: The test features.

        Returns:
        - y_predicted: Predicted labels for the test data.
        """
        positions = np.array([np.dot(self.kernel(x), self.weights) - self.bias for x in X_test])
        y_predicted = np.sign(positions).astype(int)
        return y_predicted

    def accuracy(self, X_test, y_test):
        """
        Computes the accuracy of the SVM on the given test data.

        Parameters:
        - X_test: The test features.
        - y_test: The true labels for the test data.

        Returns:
        - accuracy: The accuracy of the model on the test data.
        """
        y_predicted = self.predict(X_test)
        accuracy = np.sum(y_predicted == y_test) / len(y_test)
        return accuracy

class kernel_functions:

    @staticmethod
    def linear(x):
        """
        Linear kernel function.

        Parameters:
        - x: Input data.

        Returns:
        - z: Transformed data using a linear kernel.
        """
        z = []
        for val in x:
            z.append(val)
        z = np.array(z)
        return z

    @staticmethod
    def quadratic(x):
        """
        Quadratic kernel function.

        Parameters:
        - x: Input data.

        Returns:
        - z: Transformed data using a quadratic kernel.
        """
        z = []
        for val in x:
            z.append(val)
            z.append(val * val)
        z = np.array(z)
        return z

    @staticmethod
    def squares(x):
        """
        Squares kernel function.

        Parameters:
        - x: Input data.

        Returns:
        - z: Transformed data using a squares kernel.
        """
        z = []
        for val in x:
            z.append(val * val)
        z = np.array(z)
        return z
