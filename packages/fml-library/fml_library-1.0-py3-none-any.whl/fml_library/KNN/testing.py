from KNN import KNN
from Utility_functions import TrainTestSplit,Accuracy,MeanSquaredError
import numpy as np
from sklearn.datasets import load_iris,fetch_california_housing
import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score,mean_squared_error
from sklearn.linear_model import LogisticRegression,LinearRegression



iris_df = pd.read_csv('KNN\iris.csv')  # Read Iris dataset from iris.csv
X = iris_df[['sepal_length', 'sepal_width', 'petal_length', 'petal_width']].values

# Encode the target variable 'species' into numerical labels
class_mapping = {'Iris-setosa': 0, 'Iris-versicolor': 1, 'Iris-virginica': 2}
y = iris_df['species'].map(class_mapping).values

#knn = KNN(k=3, distance_metric='Manhattan')
#knn = KNN(k=3,  custom_distance=cosine_distance)
knn = KNN(k=3)
splitter=TrainTestSplit(test_size=0.5, random_state=42)
X_train, X_test, y_train, y_test = splitter.split(X, y)
def cosine_distance(x1, x2):
    return np.dot(x1, x2) / (np.linalg.norm(x1) * np.linalg.norm(x2))

knn.fit(X_train, y_train)

sklearn_knn = KNeighborsClassifier(n_neighbors=3)
sklearn_knn.fit(X_train, y_train)
y_pred_sklearn = sklearn_knn.predict(X_test)

y_pred = knn.predict(X_test)
accu=Accuracy()
accuracy_custom = accu.accuracy_score(y_test, y_pred)
accuracy_sklearn = accu.accuracy_score(y_test, y_pred_sklearn)

print(f"KNN Accuracy Custom: {accuracy_custom}")
print(f"KNN Accuracy SKlearn: {accuracy_sklearn}")