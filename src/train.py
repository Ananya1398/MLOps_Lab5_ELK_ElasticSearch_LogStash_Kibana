from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import f1_score, confusion_matrix
import numpy as np
import joblib

from data import load_data, split_data
from logger_config import get_logger

logger = get_logger("training", "health_training.log")


def fit_model(X_train, y_train, X_test, y_test):
    logger.info("Starting health model training...")
    logger.info(f"Training samples: {len(X_train)}")
    logger.info(f"Testing samples: {len(X_test)}")

    model = DecisionTreeClassifier(max_depth=3, random_state=12)
    model.fit(X_train, y_train)

    logger.info("Model training completed.")

    preds = model.predict(X_test)
    f1 = f1_score(y_test, preds, average="weighted")
    conf = confusion_matrix(y_test, preds)

    logger.info(f"F1 Score: {f1:.2f}")

    tp = np.diag(conf)
    tn = np.sum(conf) - (np.sum(conf, axis=0) + np.sum(conf, axis=1) - tp)
    fp = np.sum(conf, axis=0) - tp
    fn = np.sum(conf, axis=1) - tp

    logger.info(f"False Positive: {fp}")
    logger.info(f"False Negative: {fn}")
    logger.info(f"False Positive Rate: {(fp / (fp + tn)).tolist()}")
    logger.info(f"False Negative Rate: {(fn / (fn + tp)).tolist()}")

    joblib.dump(model, "../model/health_model.pkl")

if __name__ == "__main__":
    X, y, names = load_data()
    X_train, X_test, y_train, y_test = split_data(X, y)
    fit_model(X_train, y_train, X_test, y_test)
