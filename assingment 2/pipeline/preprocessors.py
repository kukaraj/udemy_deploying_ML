import numpy as np
import pandas as pd

from sklearn.base import BaseEstimator, TransformerMixin


# Add binary variable to indicate missing values
class MissingIndicator(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables


    def fit(self, X, y=None):
        # to accommodate sklearn pipeline functionality
        return self


    def transform(self, X):
        # add indicator
        X = X.copy()
        for feature in self.variables:
            X[feature+'_na'] = np.where(X[feature].isnull(), 1, 0)

        return X


# categorical missing value imputer
class CategoricalImputer(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # we need the fit statement to accommodate the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].fillna('Missing')

        return X



# Numerical missing value imputer
class NumericalImputer(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables


    def fit(self, X, y=None):
        # persist mode in a dictionary
        self.imputer_dict_ = {}
        
        for feature in self.variables:
            #print(X)
            self.imputer_dict_[feature] = X[feature].median()
        return self

    def transform(self, X):

        X = X.copy()
        for feature in self.variables:
            X[feature].fillna(self.imputer_dict_[feature], inplace=True)

        return X


# Extract first letter from string variable
class ExtractFirstLetter(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):
        # we need this step to fit the sklearn pipeline
        return self

    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = X[feature].str[0]

        return X

# frequent label categorical encoder
class RareLabelCategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, tol=0.05, variables=None):
        self.tol = tol
        
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):

        # persist frequent labels in dictionary
        self.encoder_dict_ = {}

        for var in self.variables:
            # the encoder will learn the most frequent categories
            t = pd.Series(X[var].value_counts() / np.float(len(X)))
            # frequent labels:
            self.encoder_dict_[var] = list(t[t >= self.tol].index)

        return self


    def transform(self, X):
        X = X.copy()
        for feature in self.variables:
            X[feature] = np.where(X[feature].isin(self.encoder_dict_[
                    feature]), X[feature], 'Rare')

        return X


# string to numbers categorical encoder
class CategoricalEncoder(BaseEstimator, TransformerMixin):

    def __init__(self, variables=None):
        if not isinstance(variables, list):
            self.variables = [variables]
        else:
            self.variables = variables

    def fit(self, X, y=None):

        # HINT: persist the dummy variables found in train set
        self.dummies = pd.get_dummies(X[self.variables], drop_first=True).columns
        
        return self

    def transform(self, X):
        # encode labels
        X = X.copy()
        # get dummies
        encoded_df = pd.get_dummies(X[self.variables], prefix=self.variables, drop_first=True)
       
        # add missing dummies if any
        missing_cols = set(self.dummies) - set(encoded_df.columns)

        # Add a missing column in test set with default value equal to 0
        if missing_cols:
            for c in missing_cols:
                encoded_df[c] = 0
            # Ensure the order of column in the test set is in the same order than in train set
            encoded_df = encoded_df[self.dummies]

        X = pd.concat([X, encoded_df], axis=1)
        # drop original variables
        X.drop(labels=self.variables, axis=1, inplace=True)

        return X
