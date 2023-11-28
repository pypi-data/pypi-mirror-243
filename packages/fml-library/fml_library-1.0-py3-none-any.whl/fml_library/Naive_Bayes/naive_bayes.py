import numpy as np

class NaiveBayes:
    def __init__(self, X_train, y_train):
        # Initialize NaiveBayes class with training data
        # X_train: Features of the training data
        # y_train: Labels of the training data

        # Store training data and calculate necessary parameters
        self.X_train = X_train
        self.y_train = y_train
        self.no_of_features = len(self.X_train[0])
        self.no_of_classes = len(set(self.y_train))
        self.distribution = ["" for _ in range(self.no_of_features)]
        self.X_parameters = [[] for _ in range(self.no_of_features)]
        self.y_parameters = self.estimate_prior_y(self.y_train)
        self.individual_features = [[] for i in range(self.no_of_features)]

        # Separate individual features for later use
        for i in range(len(self.X_train)):
            for j in range(len(self.X_train[i])):
                self.individual_features[j].append(self.X_train[i][j])

    def estimate_prior_y(self, y):
        # Estimate prior probabilities for each class based on the training labels
        total_count = len(y)
        unique_count = len(set(y))
        prior_estimators = [0 for i in range(unique_count)]

        for i in range(total_count):
            prior_estimators[int(y[i])] += 1

        prior_estimators = [x / total_count for x in prior_estimators]
        return prior_estimators

    def save_x_distribution(self, feature_no, distribution):
        # Save the distribution type for a specific feature
        # feature_no: Index of the feature
        # distribution: Type of distribution ("gaussian", "bernoulli", "laplace", "exponential", "multinomial")
        self.distribution[feature_no] = distribution

    def fit_x_estimators(self):
        # Fit distribution parameters for each feature based on the saved distribution type
        for feature_no in range(self.no_of_features):
            self.find_x_distribution_parameters(feature_no)

    def find_x_distribution_parameters(self, feature_no):
        # Find distribution parameters for a specific feature and class
        # feature_no: Index of the feature

        # Determine the distribution function based on the saved distribution type
        distribution_function = None
        if self.distribution[feature_no] == "gaussian":
            distribution_function = self.estimate_gaussian
        if self.distribution[feature_no] == "bernoulli":
            distribution_function = self.estimate_bernoulli
        if self.distribution[feature_no] == "laplace":
            distribution_function = self.estimate_laplace
        if self.distribution[feature_no] == "exponential":
            distribution_function = self.estimate_exponential
        if self.distribution[feature_no] == "multinomial":
            distribution_function = self.estimate_multinomial

        if distribution_function == "":
            return

        # Estimate distribution parameters for each class
        for class_no in range(self.no_of_classes):
            self.X_parameters[feature_no].append(distribution_function(self.individual_features[feature_no],
                                                                         self.y_train, class_no))

    def predict(self, X_test):
        # Predict class labels for the given test data using Naive Bayes classifier
        # X_test: Features of the test data
        # Return a list of predicted labels
        total_count = len(X_test)
        total_class = self.no_of_classes
        pred_y = [0 for i in range(total_count)]

        for i in range(total_count):
            max_log_posterior = float('-inf')

            for class_no in range(total_class):
                # Calculate log posterior probabilities for each class
                log_posterior = np.log(self.y_parameters[class_no])

                # Sum up log probabilities for each feature
                for feature_no in range(self.no_of_features):
                    fit_function = None
                    if self.distribution[feature_no] == "gaussian":
                        fit_function = self.fit_gaussian
                    if self.distribution[feature_no] == "bernoulli":
                        fit_function = self.fit_bernoulli
                    if self.distribution[feature_no] == "laplace":
                        fit_function = self.fit_laplace
                    if self.distribution[feature_no] == "exponential":
                        fit_function = self.fit_exponential
                    if self.distribution[feature_no] == "multinomial":
                        fit_function = self.fit_multinomial

                    log_posterior += fit_function(X_test[i][feature_no], feature_no, class_no)

                # Update predicted label based on maximum log posterior
                if log_posterior > max_log_posterior:
                    max_log_posterior = log_posterior
                    pred_y[i] = class_no

        return pred_y

    # Various distribution estimation methods

    def estimate_gaussian(self, x, y, class_no):
        # Estimate Gaussian distribution parameters for a specific feature and class
        total_count = len(y)
        required_count = 0
        mean = 0
        var = 0

        # Calculate mean and variance
        for i in range(total_count):
            if y[i] == class_no:
                required_count += 1
                mean += x[i]

        mean /= required_count

        for i in range(total_count):
            if y[i] == class_no:
                var += (x[i] - mean) ** 2

        var /= required_count

        estimator = {"mean": mean, "var": var}
        return estimator

    def estimate_bernoulli(self, x, y, class_no):
        # Estimate Bernoulli distribution parameters for a specific feature and class
        total_count = len(y)
        required_count = 0
        mean = 0

        # Calculate mean
        for i in range(total_count):
            if y[i] == class_no:
                required_count += 1
                mean += x[i]

        mean /= required_count

        estimator = {"mean": mean}
        return estimator

    def estimate_laplace(self, x, y, class_no):
        # Estimate Laplace distribution parameters for a specific feature and class
        total_count = len(y)
        required_x = []
        required_count = 0
        sum_of_required_x = 0

        # Collect relevant data for Laplace distribution
        for i in range(total_count):
            if y[i] == class_no:
                required_x.append(x[i])
                sum_of_required_x += x[i]
                required_count += 1

        required_x.sort()
        left_sum = 0
        right_sum = sum_of_required_x
        mean = required_x[0]
        min_error = right_sum - required_x[0] * required_count
        b = 0

        # Find optimal parameters for Laplace distribution
        for i in range(required_count):
            curr_error = (right_sum - required_x[i] * (required_count - i)) + (required_x[i] * i - left_sum)
            if curr_error < min_error:
                min_error = curr_error
                mean = required_x[i]

            left_sum += required_x[i]
            right_sum -= required_x[i]

        for i in range(required_count):
            b += abs(required_x[i] - mean)

        b /= required_count

        estimator = {"mean": mean, "b": b}
        return estimator

    def estimate_exponential(self, x, y, class_no):
        # Estimate Exponential distribution parameters for a specific feature and class
        total_count = len(y)
        required_count = 0
        mean = 0

        # Calculate mean for Exponential distribution
        for i in range(total_count):
            if y[i] == class_no:
                required_count += 1
                mean += x[i]

        mean /= required_count

        estimator = {"lambda_value": 1 / mean}
        return estimator

    def estimate_multinomial(self, x, y, class_no):
        # Estimate Multinomial distribution parameters for a specific feature and class
        total_count = len(y)
        required_count = 0
        no_of_x_classes = int(max(x) + 1)
        mean = [0 for i in range(no_of_x_classes)]

        # Calculate mean for each class in Multinomial distribution
        for i in range(total_count):
            if y[i] == class_no:
                required_count += 1
                mean[int(x[i])] += 1

        mean = [x / required_count for x in mean]
        estimator = {"mean": mean}
        return estimator

    # Various fitting methods for different distributions

    def fit_gaussian(self, x, feature_no, class_no):
        # Fit Gaussian distribution for a specific feature and class
        mean = self.X_parameters[feature_no][class_no]['mean']
        var = self.X_parameters[feature_no][class_no]['var']

        curr_log_prob = (((x - mean) ** 2) / var + np.log(2 * np.pi * var)) * (-1 / 2)
        return curr_log_prob

    def fit_bernoulli(self, x, feature_no, class_no):
        # Fit Bernoulli distribution for a specific feature and class
        mean = self.X_parameters[feature_no][class_no]['mean']
        curr_log_prob = np.log(x * mean + (1 - x) * (1 - mean))
        return curr_log_prob

    def fit_laplace(self, x, feature_no, class_no):
        # Fit Laplace distribution for a specific feature and class
        mean = self.X_parameters[feature_no][class_no]['mean']
        b = self.X_parameters[feature_no][class_no]['b']
        curr_log_prob = ((abs(x - mean)) / b + np.log(2 * b)) * (-1)
        return curr_log_prob

    def fit_exponential(self, x, feature_no, class_no):
        # Fit Exponential distribution for a specific feature and class
        lambda_value = self.X_parameters[feature_no][class_no]['lambda_value']
        curr_log_prob = np.log(lambda_value) - lambda_value * x
        return curr_log_prob

    def fit_multinomial(self, x, feature_no, class_no):
        # Fit Multinomial distribution for a specific feature and class
        mean = self.X_parameters[feature_no][class_no]['mean']
        curr_log_prob = np.log(mean[int(x)])
        return curr_log_prob
