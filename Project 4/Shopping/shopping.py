import csv
import sys

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")


def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # Creates the lists to store the labels and evidence of all the training data
    evidence_list = []
    label_list = []

    # Loads the file as a dictionary to easily read from it
    with open(filename) as file:
        reader = csv.DictReader(file)
        for row in reader:
            evidence = []
            evidence.append(int(row['Administrative']))
            evidence.append(float(row['Administrative_Duration']))
            evidence.append(int(row['Informational']))
            evidence.append(float(row['Informational_Duration']))
            evidence.append(int(row['ProductRelated']))
            evidence.append(float(row['ProductRelated_Duration']))
            evidence.append(float(row['BounceRates']))
            evidence.append(float(row['ExitRates']))
            evidence.append(float(row['PageValues']))
            evidence.append(float(row['SpecialDay']))
            # Creates a list used tofind the index of each month whithout the need for if-elif-else statements
            months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'June', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'] 
            evidence.append(months.index(row['Month']))
            evidence.append(int(row['OperatingSystems']))
            evidence.append(int(row['Browser']))
            evidence.append(int(row['Region']))
            evidence.append(int(row['TrafficType']))
            evidence.append(1 if row['VisitorType'] == 'Returning_Visitor' else 0)
            evidence.append(1 if row['Weekend'] == 'TRUE' else 0)

            # Adds the the evidence and label for the current data point to their respective list of values for all the data points
            evidence_list.append(evidence)
            label_list.append(1 if row['Revenue'] == 'TRUE' else 0)

    return (evidence_list, label_list)


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Creates a model based on the nearest-neighbour classifier and returns it fitted
    model = KNeighborsClassifier(1)
    return model.fit(evidence, labels)
    

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificity).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Creates variables to store values which will be used for calculation
    sensitivity = 0.0
    specificity = 0.0
    positive_total = 0
    negative_total = 0

    for label, prediction in zip(labels, predictions):
        # Updates the positive variables if the label is positive
        if label == 1:
            positive_total += 1
            if label == prediction:
                sensitivity += 1

        # Updates the negative variabes if the label is negative
        else:
            negative_total += 1
            if label == prediction:
                specificity += 1

    # Updates the variables to be divided by their respective totals for a percentage     
    sensitivity /= positive_total
    specificity /= negative_total

    return (sensitivity, specificity)



if __name__ == "__main__":
    main()
