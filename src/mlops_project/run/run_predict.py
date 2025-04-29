import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.prediction import Predictor


def main():
    load_dotenv()
    config = load_config("../config/dev.yaml")

    csv_processed_key = f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv"
    prediction_output_key = f"predictions/{config["project_name"]}_preds.csv"
    model_key = f"models/{config["project_name"]}_model.pkl"

    predictor = Predictor(
        bucket=os.getenv("S3_BUCKET_NAME"),
        model_key=model_key,
        csv_processed_key=csv_processed_key,
        prediction_output_key=prediction_output_key,
        config=config
    )
    predictor.run()


if __name__ == "__main__":
    main()
