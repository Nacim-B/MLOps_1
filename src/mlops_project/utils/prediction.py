import pandas as pd

from mlops_project.utils.s3_handler import S3Handler

class Predictor:
    def __init__(self, bucket: str, model_key: str, processed_data: pd.DataFrame, prediction_output_key: str, config: dict):
        self.bucket = bucket
        self.model_key = model_key
        self.df_processed = processed_data
        self.prediction_output_key = prediction_output_key
        self.config = config
        self.id_column = self.config.get("id_column", None)
        self.target = self.config.get("target")
        self.s3 = S3Handler(bucket, self.config)

    def run(self):
        # Load data and model
        model = self.s3.load_model_from_s3(self.model_key)

        # Set index if id_column is configured and exists
        if self.id_column and self.id_column in self.df_processed.columns:
            self.df_processed = self.df_processed.set_index(self.id_column)

        # Remove target if present (in test datasets for example)

        if self.target and self.target in self.df_processed.columns:
            self.df_processed = self.df_processed.drop(columns=[self.target])

        # Predict
        predictions = model.predict(self.df_processed)

        # Create output DataFrame
        output = pd.DataFrame(predictions, columns=["prediction"])

        # If index is meaningful (from id_column), preserve it in output
        if self.id_column:
            output.index.name = self.id_column  # Rename index explicitly

        # Save predictions to S3s
        self.s3.save_csv_to_s3(output.reset_index(), self.prediction_output_key)
        print(f"✅ Predictions saved to s3://{self.bucket}/{self.prediction_output_key}")

        return output