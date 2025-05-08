import pandas as pd
import mlflow
import os
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
from mlflow.tracking import MlflowClient

from mlops_project.utils.s3_handler import S3Handler

class ModelTrainer:
    def __init__(self, bucket: str, df_processed: pd.DataFrame, model_key: str, config: dict):
        self.bucket = bucket
        self.df_processed = df_processed
        self.model_key = model_key
        self.config = config
        self.task_type = self.config["type"]
        self.target = self.config["target"]
        self.seed = self.config.get("seed", 42)
        self.s3 = S3Handler(bucket, self.config)

        self._setup_mlflow()

    def run(self):

        X = self.df_processed.drop(columns=[self.target])
        y = self.df_processed[self.target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.seed,
            stratify=y if self.task_type == "classification" else None
        )

        if self.s3.exists_in_s3(self.model_key):
            self.retrain_model(X_train, y_train, X_test, y_test)
        else:
            print("⚠️ Model not found in S3. Falling back to training from scratch.")
            self.train_from_scratch(X_train, y_train, X_test, y_test)


    def retrain_model(self, X_train, y_train, X_test, y_test):
        model = self.s3.load_model_from_s3(self.model_key)
        with mlflow.start_run(run_name="retrain_model"):
            mlflow.log_param("mode", "retrain")
            mlflow.log_param("model_type", type(model).__name__)
            self._model_training(model, X_train, y_train, X_test, y_test)

    def train_from_scratch(self, X_train, y_train, X_test, y_test):
        if self.task_type == "classification":
            model = RandomForestClassifier(n_estimators=100, random_state=self.seed)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=self.seed)

        with mlflow.start_run(run_name="train_from_scratch"):
            mlflow.log_param("mode", "from_scratch")
            mlflow.log_param("model_type", type(model).__name__)
            mlflow.log_param("n_estimators", 100)
            self._model_training(model, X_train, y_train, X_test, y_test)


    def _model_training(self, model, X_train, y_train, X_test, y_test):
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = self._metric()(y_test, y_pred)

        mlflow.log_metric("score", score)
        mlflow.sklearn.log_model(model, "model")

        print(f"🆕 Model score (from scratch): {score:.4f}")
        self.s3.save_model_to_s3(model, self.model_key)

    def _metric(self):
        return accuracy_score if self.task_type == "classification" else mean_squared_error

    def _setup_mlflow(self):
        """
        Configure MLflow tracking and artifact storage using S3.
        Ensures the experiment exists and is linked to the correct artifact location.
        """
        mlflow.set_tracking_uri("file:./mlruns")
        experiment_name = f"{self.config['project_name']}_experiment"
        artifact_uri = f"s3://{self.bucket}/mlruns"

        client = MlflowClient()
        experiment = client.get_experiment_by_name(experiment_name)

        if experiment is None:
            print(f"🔧 Creating MLflow experiment '{experiment_name}' at '{artifact_uri}'")
            experiment_id = client.create_experiment(
                name=experiment_name,
                artifact_location=artifact_uri
            )
        else:
            print(f"📁 MLflow experiment '{experiment_name}' already exists.")
            experiment_id = experiment.experiment_id

        mlflow.set_experiment(experiment_name)
