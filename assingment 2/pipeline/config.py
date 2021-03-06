# ====   PATHS ===================

TRAINING_DATA_FILE = "titanic.csv"
PIPELINE_NAME = 'logistic_regression.pkl'


# ======= FEATURE GROUPS =============

TARGET = 'survived'

FEATURES = ['pclass', 'age', 'sibsp', 'parch', 'fare', 'sex', 'cabin', 'embarked', 'title']

NUMERICAL_VARS = ['pclass', 'age', 'sibsp', 'parch', 'fare']

CATEGORICAL_VARS = ['sex', 'cabin', 'embarked', 'title']

CABIN = 'cabin'