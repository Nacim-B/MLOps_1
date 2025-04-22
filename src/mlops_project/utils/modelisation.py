import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error

from mlops_project.utils.s3_handler import S3Handler

class ModelTrainer:
    def __init__(self, bucket: str, csv_processed_key: str, model_key: str, config: dict):
        self.bucket = bucket
        self.csv_processed_key = csv_processed_key
        self.model_key = model_key
        self.config = config
        self.task_type = config["type"]
        self.target = config["target"]
        self.id_column = config.get("id_column", None)
        self.seed = config.get("seed", 42)
        self.retrain_only = config.get("retrain_only", False)
        self.s3 = S3Handler(bucket)

    def run(self):
        df = self.s3.load_csv_from_s3(self.csv_processed_key)

        if self.id_column and self.id_column in df.columns:
            df = df.set_index(self.id_column)

        X = df.drop(columns=[self.target])
        y = df[self.target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.seed,
            stratify=y if self.task_type == "classification" else None
        )

        if self.retrain_only:
            self.retrain_model(X_train, y_train, X_test, y_test)
        else:
            self.train_from_scratch(X_train, y_train, X_test, y_test)

    def retrain_model(self, X_train, y_train, X_test, y_test):
        model = self.s3.load_model_from_s3(self.model_key)
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = self._metric()(y_test, y_pred)
        print(f"🔁 Retrained model score: {score:.4f}")
        self.s3.save_model_to_s3(model, self.model_key)

    def train_from_scratch(self, X_train, y_train, X_test, y_test):
        if self.task_type == "classification":
            model = RandomForestClassifier(n_estimators=100, random_state=self.seed)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=self.seed)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = self._metric()(y_test, y_pred)
        print(f"🆕 Model score (from scratch): {score:.4f}")
        self.s3.save_model_to_s3(model, self.model_key)

    def _metric(self):
        return accuracy_score if self.task_type == "classification" else mean_squared_error
