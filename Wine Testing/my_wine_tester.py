"""
Team:
Les deux canetons
Authors:
Guillaume Thibault - 1948612
Jacob Brisson - 1954091
"""

from wine_testers import WineTester
from imblearn.over_sampling import SMOTE
from sklearn.linear_model import LogisticRegression
from sklearn.utils import shuffle
from sklearn.ensemble import VotingClassifier, RandomForestClassifier, AdaBoostClassifier


class MyWineTester(WineTester):
    def __init__(self):
        tree_b = RandomForestClassifier(bootstrap=False, ccp_alpha=0.0, class_weight='balanced',
                                        criterion='entropy', max_depth=24, n_estimators=68, random_state=0)
        log_r = LogisticRegression(
            penalty='l2', C=0.13, solver='liblinear', random_state=0)

        ens = VotingClassifier(
            [('clf1', tree_b), ('clf2', log_r)], voting='soft')

        self.ada = AdaBoostClassifier(base_estimator=ens, learning_rate=0.01,
                                      n_estimators=5, random_state=0)

    def train(self, X_train, y_train):
        """
        train the current model on train_data
        :param X_train: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :param y_train: 2D array of labels.
                each line is a different example.
                the first column is the example ID.
                the second column is the example label.
        """
        X_train = [v[1:] for v in X_train]
        y_train = [v[1] for v in y_train]

        for i, ex in enumerate(X_train):
            if ex[0] == 'white':
                X_train[i][0] = 0
            else:
                X_train[i][0] = 1

        single_values = [X_train[i] for i, v in enumerate(y_train) if v == 9]

        for i in range(2):
            for v in single_values:
                X_train.append(v)
                y_train.append(9)

        strategy = {3: 450, 4: 700, 5: 1680, 6: 2200, 7: 1120, 8: 700, 9: 350}
        smote = SMOTE(k_neighbors=5, random_state=0,
                      sampling_strategy=strategy)
        X_train, y_train = smote.fit_resample(X_train, y_train)
        X_train, y_train = shuffle(X_train, y_train, random_state=0)

        self.ada.fit(X_train, y_train)

    def predict(self, X_data):
        """
        predict the labels of the test_data with the current model
        and return a list of predictions of this form:
        [
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            [<ID>, <prediction>],
            ...
        ]
        :param X_data: 2D array of data points.
                each line is a different example.
                each column is a different feature.
                the first column is the example ID.
        :return: a 2D list of predictions with 2 columns: ID and prediction
        """
        X_data = [v[1:] for v in X_data]
        for i, ex in enumerate(X_data):
            if ex[0] == 'white':
                X_data[i][0] = 0
            else:
                X_data[i][0] = 1

        preds = self.ada.predict(X_data)
        predictions = []
        for i, v in enumerate(preds):
            predictions.append([i, v])
        return predictions
