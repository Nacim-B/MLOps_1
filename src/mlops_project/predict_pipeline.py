import os
from dotenv import load_dotenv

from mlops_project.config.config_loader import load_config
from mlops_project.utils.s3_handler import S3Handler
from mlops_project.utils.data_processing import DataProcessor
from mlops_project.utils.prediction import Predictor

def main():
    # Load env + config
    load_dotenv()

    config = load_config("./config/dev.yaml")
    project_name = config['project_name']

    bucket = os.getenv("S3_BUCKET_NAME")
    filename = os.getenv("CSV_FILENAME")
    url = os.getenv("CSV_URL")

    raw_key = f"datasets/{filename}_raw.csv"
    csv_processed_key = f"datasets/{filename}_processed.csv"
    prediction_output_key = f"predictions/{project_name}_preds.csv"
    model_key = f"models/{project_name}_model.pkl"

    # Step 1: Download
    print("⬇️ Step 1: Downloading CSV from URL to S3...")
    s3handler = S3Handler(
        bucket=bucket,
        config=config
    )
    s3handler.upload_csv_from_url_to_s3(url, filename)

    # Step 2: Preprocessing
    print("🧹 Step 2: Preprocessing data...")
    processor = DataProcessor(
        bucket=bucket,
        raw_key=raw_key,
        csv_processed_key=csv_processed_key,
        config=config
    )
    processor.run()

    # Step 3: Training
    print("🔮 Step 3: Prediction ...")
    predictor = Predictor(
        bucket=bucket,
        model_key=model_key,
        csv_processed_key=csv_processed_key,
        prediction_output_key=prediction_output_key,
        config=config
    )
    predictor.run()

    print("✅ Predict Pipeline completed successfully.")

if __name__ == "__main__":
    main()
