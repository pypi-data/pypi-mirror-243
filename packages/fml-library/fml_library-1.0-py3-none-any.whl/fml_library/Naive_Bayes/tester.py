from naive_bayes import NaiveBayes
import pandas as pd
import numpy as np


def net_f1score(predictions, true_labels):

    def confusion_matrix(predictions, true_labels, label):
        
        true_positive = 0
        true_negative = 0
        false_positive = 0
        false_negative = 0

        for predicted, actual in zip(predictions, true_labels):
            if predicted == label and actual == label:
                true_positive += 1
            if predicted != label and actual != label:
                true_negative += 1
            if predicted != label and actual == label:
                false_positive += 1
            if predicted == label and actual != label:
                false_negative += 1

        confusion = {"true_positive": true_positive,
                     "true_negative": true_negative,
                     "false_positive": false_positive,
                     "false_negative": false_negative,
                     }
        
        return confusion
            

    def precision(predictions, true_labels, label):
        
        confusion = confusion_matrix(predictions, true_labels, label)

        precision_value = confusion["true_positive"] / (confusion["true_positive"] + confusion["false_positive"])

        return precision_value


    def recall(predictions, true_labels, label):
        
        confusion = confusion_matrix(predictions, true_labels, label)

        recall_value = confusion["true_positive"] / (confusion["true_positive"] + confusion["false_negative"])

        return recall_value
        

    def f1score(predictions, true_labels, label):

        precision_value = precision(predictions, true_labels, label)
        recall_value = recall(predictions, true_labels, label)
        
        f1 = 2 * precision_value * recall_value / (precision_value + recall_value)

        return f1
    

    f1s = []
    for label in np.unique(true_labels):
        f1s.append(f1score(predictions, true_labels, label))

    return f1s



def accuracy(predictions,true_labels):

    return np.sum(predictions==true_labels)/len(predictions)


def main():

    train_dataset = pd.read_csv('./Naive_Bayes/data/train_dataset.csv',index_col=0).to_numpy()
    validation_dataset = pd.read_csv('./Naive_Bayes/data/validation_dataset.csv',index_col=0).to_numpy()

    X_train = train_dataset[:,:-1]
    y_train = train_dataset[:, -1]
    X_test = validation_dataset[:, 0:-1]
    y_test = validation_dataset[:, -1]

    model = NaiveBayes(X_train, y_train)

    model.save_x_distribution(0,"gaussian")
    model.save_x_distribution(1,"gaussian")
    model.save_x_distribution(2,"bernoulli")
    model.save_x_distribution(3,"bernoulli")
    model.save_x_distribution(4,"laplace")
    model.save_x_distribution(5,"laplace")
    model.save_x_distribution(6,"exponential")
    model.save_x_distribution(7,"exponential")
    model.save_x_distribution(8,"multinomial")
    model.save_x_distribution(9,"multinomial")

    model.fit_x_estimators()


    train_predictions = model.predict(X_train)
    validation_predictions = model.predict(X_test)

    train_accuracy = accuracy(train_predictions, y_train)
    validation_accuracy = accuracy(validation_predictions, y_test)

    train_f1score = net_f1score(train_predictions, y_train)
    validation_f1score = net_f1score(validation_predictions, y_test)

    print('Training Accuracy: ', train_accuracy)
    print('Validation Accuracy: ', validation_accuracy)
    print('Training F1 Score: ', train_f1score)
    print('Validation F1 Score: ', validation_f1score)

if __name__ == "__main__":

    main()