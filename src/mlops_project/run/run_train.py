import os
from dotenv import load_dotenv
from mlops_project.config.config_loader import load_config
from mlops_project.utils.model_training import ModelTrainer

def main():
    load_dotenv()
    config = load_config("../config/dev.yaml")

    csv_processed_key = f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv"
    model_key = f"models/{config['project_name']}_model.pkl"

    trainer = ModelTrainer(
        bucket=os.getenv("S3_BUCKET_NAME"),
        csv_processed_key=csv_processed_key,
        model_key=model_key,
        config=config
    )
    trainer.run()

if __name__ == "__main__":
    main()