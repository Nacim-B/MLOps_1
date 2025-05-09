import os

import pandas as pd
import mlflow

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error, precision_score, recall_score, f1_score
from sklearn.metrics import mean_absolute_error, r2_score

from mlops_project.utils.s3_handler import S3Handler
from mlops_project.utils.mysql_handler import MySQLHandler
from mlops_project.utils.mlflow_handler import MLflowHandler

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

        # Initialize MLflow
        self.mysql_handler = MySQLHandler(self.config, os.getenv('MYSQL_DB_MLFLOW'))
        self.mlflow_handler = MLflowHandler(self.mysql_handler, self.config)
        self.experiment_id, self.experiment_name = self.mlflow_handler.setup_experiment()

    def run(self):
        X = self.df_processed.drop(columns=[self.target])
        y = self.df_processed[self.target]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=self.seed,
            stratify=y if self.task_type == "classification" else None
        )

        if self.s3.exists_in_s3(self.model_key):
            self._retrain_model(X_train, y_train, X_test, y_test)
        else:
            print("⚠️ Model not found in S3. Falling back to training from scratch.")
            self._train_from_scratch(X_train, y_train, X_test, y_test)

    def _retrain_model(self, X_train, y_train, X_test, y_test):
        """Retrain an existing model from S3."""
        model = self.s3.load_model_from_s3(self.model_key)

        run_params = {
            "mode": "retrain",
            "model_type": type(model).__name__,
            "features": list(X_train.columns),
            "dataset_rows": len(X_train) + len(X_test),
            "train_rows": len(X_train),
            "test_rows": len(X_test)
        }

        self._train_model(model, X_train, y_train, X_test, y_test, run_params)

    def _train_from_scratch(self, X_train, y_train, X_test, y_test):
        """Train a new model from scratch."""
        if self.task_type == "classification":
            model = RandomForestClassifier(n_estimators=100, random_state=self.seed)
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=self.seed)

        run_params = {
            "mode": "from_scratch",
            "model_type": type(model).__name__,
            "n_estimators": 100,
            "random_state": self.seed,
            "features": list(X_train.columns),
            "dataset_rows": len(X_train) + len(X_test),
            "train_rows": len(X_train),
            "test_rows": len(X_test)
        }

        self._train_model(model, X_train, y_train, X_test, y_test, run_params)

    def _train_model(self, model, X_train, y_train, X_test, y_test, run_params):
        """
        Train and evaluate a model while logging to MLflow.

        Args:
            model: Model to train
            X_train: Training features
            y_train: Training target
            X_test: Test features
            y_test: Test target
            run_params: Dictionary of parameters to log
        """
        with mlflow.start_run(run_name=run_params.pop("mode", "training")):
            # Log run parameters
            for param_name, param_value in run_params.items():
                mlflow.log_param(param_name, param_value)

            # Set mode tag
            mlflow.set_tag("mode", run_params.get("mode", "training"))

            # Train model
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            # Log metrics
            score = self._log_metrics(y_test, y_pred)

            # Log model to MLflow
            mlflow.sklearn.log_model(
                model,
                "model",
                registered_model_name=f"{self.config['project_name']}_{self.task_type}"
            )

            # Save to S3
            self.s3.save_model_to_s3(model, self.model_key)

            print(f"✅ Model {run_params.get('mode', 'trained')}. Score: {score:.4f}")

            return model, score

    def _log_metrics(self, y_test, y_pred):
        """Log metrics to MLflow based on task type."""
        # Calculate primary metric
        if self.task_type == "classification":
            score = accuracy_score(y_test, y_pred)
            mlflow.log_metric("accuracy", score)

            # Log additional classification metrics
            try:
                mlflow.log_metric("precision", precision_score(y_test, y_pred, average='weighted'))
                mlflow.log_metric("recall", recall_score(y_test, y_pred, average='weighted'))
                mlflow.log_metric("f1", f1_score(y_test, y_pred, average='weighted'))
            except:
                pass  # For multi-class cases that might fail
        else:
            # Regression metrics
            mse = mean_squared_error(y_test, y_pred)
            mlflow.log_metric("mse", mse)
            mlflow.log_metric("rmse", mean_squared_error(y_test, y_pred, squared=False))
            mlflow.log_metric("mae", mean_absolute_error(y_test, y_pred))
            mlflow.log_metric("r2", r2_score(y_test, y_pred))

        return score

    def _calculate_primary_metric(self, y_test, y_pred):
        """Calculate the primary metric based on task type."""
        if self.task_type == "classification":
            return accuracy_score(y_test, y_pred)
        else:
            return mean_squared_error(y_test, y_pred)
