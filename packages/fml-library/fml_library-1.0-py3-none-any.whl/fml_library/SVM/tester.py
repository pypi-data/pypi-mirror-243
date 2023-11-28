import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.metrics import classification_report
from svm import Support_Vector_Machine

'''

Sklearn classification report
              precision    recall  f1-score   support

          -1       0.94      1.00      0.97        85
           1       1.00      0.90      0.95        52

    accuracy                           0.96       137
   macro avg       0.97      0.95      0.96       137
weighted avg       0.97      0.96      0.96       137

My classification report
              precision    recall  f1-score   support

          -1       0.94      1.00      0.97        85
           1       1.00      0.90      0.95        52

    accuracy                           0.96       137
   macro avg       0.97      0.95      0.96       137
weighted avg       0.97      0.96      0.96       137

Actual output
[-1  1 -1  1 -1 -1 -1 -1  1 -1 -1  1  1  1  1 -1 -1 -1 -1 -1  1 -1  1  1
 -1 -1 -1 -1  1  1  1 -1  1 -1 -1 -1  1 -1 -1 -1 -1 -1 -1  1  1 -1 -1 -1
 -1  1 -1 -1 -1 -1 -1 -1  1 -1 -1 -1 -1  1  1 -1 -1  1  1 -1 -1 -1  1  1
 -1 -1 -1  1 -1 -1 -1  1 -1 -1 -1 -1  1  1 -1  1 -1 -1 -1  1 -1 -1 -1  1
 -1 -1 -1  1 -1  1 -1 -1  1 -1  1 -1 -1  1 -1 -1  1 -1 -1 -1 -1 -1  1  1
  1  1  1 -1 -1  1 -1 -1  1 -1  1 -1 -1 -1 -1 -1  1]
Sklearn output
[-1  1 -1  1 -1 -1 -1 -1  1 -1 -1  1  1  1  1 -1 -1 -1 -1 -1  1 -1  1  1
  1  1 -1 -1  1  1  1 -1  1 -1 -1 -1  1 -1 -1 -1 -1 -1 -1  1  1 -1 -1 -1
 -1  1 -1 -1 -1 -1 -1 -1  1 -1 -1 -1 -1  1  1 -1  1  1  1 -1 -1 -1  1  1
 -1 -1 -1  1 -1 -1  1  1 -1 -1 -1 -1  1  1 -1  1 -1 -1  1  1 -1 -1 -1  1
 -1 -1 -1  1 -1  1 -1 -1  1 -1  1 -1 -1  1 -1 -1  1 -1 -1 -1 -1 -1  1  1
  1  1  1 -1 -1  1 -1 -1  1 -1  1 -1 -1 -1 -1 -1  1]
My output
[-1  1 -1  1 -1 -1 -1 -1  1 -1 -1  1  1  1  1 -1 -1 -1 -1 -1  1 -1  1  1
  1  1 -1 -1  1  1  1 -1  1 -1 -1 -1  1 -1 -1 -1 -1 -1 -1  1  1 -1 -1 -1
 -1  1 -1 -1 -1 -1 -1 -1  1 -1 -1 -1 -1  1  1 -1  1  1  1 -1 -1 -1  1  1
 -1 -1 -1  1 -1 -1  1  1 -1 -1 -1 -1  1  1 -1  1 -1 -1  1  1 -1 -1 -1  1
 -1 -1 -1  1 -1  1 -1 -1  1 -1  1 -1 -1  1 -1 -1  1 -1 -1 -1 -1 -1  1  1
  1  1  1 -1 -1  1 -1 -1  1 -1  1 -1 -1 -1 -1 -1  1]
Sklearn accuaracy
0.9635036496350365
My accuaracy
0.9635036496350365
Similarities between models
1.0

'''

def main():


    X_train, X_test, y_train, y_test = get_data()

    sklearn_model = svm.SVC(kernel='linear', gamma='auto', C=2)
    my_model = Support_Vector_Machine()


    sklearn_model.fit(X_train, y_train)
    my_model.fit(X_train, y_train)

    sklearn_prediction = sklearn_model.predict(X_test)
    my_prediction = my_model.predict(X_test)

    print("Sklearn classification report")
    print(classification_report(sklearn_prediction, y_test))
    print("My classification report")
    print(classification_report(my_prediction, y_test))

    print("Actual output")
    print(y_test)
    print("Sklearn output")
    print(sklearn_prediction)
    print("My output")
    print(my_prediction)
    print("Sklearn accuaracy")
    print(np.mean(y_test==sklearn_prediction))
    print("My accuaracy")
    print(np.mean(y_test==my_prediction))
    print("Similarities between models")
    print(np.mean(sklearn_prediction==my_prediction))

    print(sklearn_model.score(X_test, y_test))
    print(my_model.accuracy(X_test, y_test))
	


def get_data():

    cell_df = pd.read_csv('./SVM/cell_samples.csv')

    cell_df = cell_df[pd.to_numeric(cell_df['BareNuc'], errors='coerce').notnull()]
    cell_df['BareNuc'] = cell_df['BareNuc'].astype('int')

    feature_df = cell_df[['Clump', 'UnifSize', 'UnifShape', 'MargAdh', 'SingEpiSize',
       'BareNuc', 'BlandChrom', 'NormNucl', 'Mit']]

    X = np.asarray(feature_df)
    y = np.asarray(cell_df['Class'])
    y = [-1 if t == 2 else 1 for t in y]
    y = np.array(y)

    X_train, X_test, y_train, y_test = train_test_split(X, y , test_size=0.2, random_state=4)

    return X_train, X_test, y_train, y_test


if __name__ == "__main__":
    main()