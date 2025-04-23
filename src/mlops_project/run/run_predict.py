import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.prediction import Predictor


def main():
    load_dotenv()
    config = load_config("../config/dev.yaml")
    project_name = config["project_name"]

    bucket = os.getenv("S3_BUCKET_NAME")
    filename = os.getenv("CSV_FILENAME")

    csv_processed_key = f"datasets/{filename}_processed.csv"
    prediction_output_key = f"predictions/{project_name}_preds.csv"
    model_key = f"models/{project_name}_model.pkl"

    predictor = Predictor(
        bucket=bucket,
        model_key=model_key,
        csv_processed_key=csv_processed_key,
        prediction_output_key=prediction_output_key,
        config=config
    )
    predictor.run()


if __name__ == "__main__":
    main()
