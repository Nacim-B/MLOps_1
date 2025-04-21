from sklearn.metrics import accuracy_score, mean_squared_error
from mlops_project.utils.s3_handler import S3Handler

class ModelTrainer:
    def __init__(self, bucket: str, model_key: str, task_type: str):
        self.s3 = S3Handler(bucket)
        self.bucket = bucket
        self.model_key = model_key
        self.task_type = task_type
        self.metric_func = accuracy_score if task_type == "classification" else mean_squared_error
        self.model = self.s3.load_model_from_s3(model_key)

    def retrain(self, X_train, y_train, X_test, y_test):
        self.model.fit(X_train, y_train)
        y_pred = self.model.predict(X_test)
        score = self.metric_func(y_test, y_pred)
        print(f"✅ Score after retraining: {score:.4f}")
        return score

    def save(self, new_key: str = None):
        path = new_key or self.model_key
        self.s3.save_model_to_s3(self.model, path)
        print(f"💾 Model saved to s3://{self.bucket}/{path}")
