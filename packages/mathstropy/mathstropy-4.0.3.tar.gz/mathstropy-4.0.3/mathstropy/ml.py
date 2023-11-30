import os
import pickle

import numpy as np
from sklearn.tree import DecisionTreeClassifier


def decision_tree_model_training(training_data, max_depth=4, random_state=42):
    """
    This function trains model using decision tree algorithm.

    Parameters:
    - training_data(pd.DataFrame): Dataframe with training data
    - max_depth: max depth of tree
    - random_state: random seed

    Returns:
    - dict: merged dictionaries
    """
    # Modeling
    X = training_data.drop("label", axis=1)
    y = training_data["label"]
    model = DecisionTreeClassifier(max_depth=max_depth, random_state=random_state)
    model.fit(X, y)

    return model


def save_model(model, model_path):
    try:
        if os.path.exists(model_path):
            os.remove(model_path)
        file1 = open(model_path, "wb")
        pickle.dump(model, file1)
        file1.close()
    except IOError:
        print("Failed to save the trained model")


def load_model(model_path):
    try:
        if not os.path.exists(model_path):
            raise Exception("Model file not found")
        else:
            with open(model_path, "rb") as file:
                model = pickle.load(file)
            return model

    except IOError:
        print("Failed to load the trained model")


def get_label_from_filename(image_filename):
    """
    This function extracts the label from filename that has the following format:
    <label>_<idx>.jpg

    Parameters:
    - image_filename(str): file name of image

    Returns:
    - dict: dictionary with label
    """

    l = image_filename.split("_")[0]

    # cut out "white" from the filename
    if "white" in l:
        l = l.split("-white")[0]

    return {"label": l}


def model_predict(model, features):
    """
    This function uses a model to make a prediction.

    Parameters:
    - model(DecisionTreeClassifier): model to use for predictions.
    - features(dict): dictionary with the features.

    Return:
    - str: prediction
    """
    data = {}
    for (
        key,
        value,
    ) in features.items():
        data[key] = [value]
    return model.predict(pd.DataFrame(data))[0]
