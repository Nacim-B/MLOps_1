import os
from dotenv import load_dotenv

from mlops_project.config.config_loader import load_config
from mlops_project.utils.data_loader import DataLoader
from mlops_project.utils.data_processing import DataProcessor
from mlops_project.utils.modelisation import ModelTrainer

def main():
    # Load env + config
    load_dotenv()
    config = load_config("./config/dev.yaml")

    csv_raw_key = f"datasets/{os.getenv("CSV_FILENAME")}_raw.csv"
    csv_processed_key = f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv"
    model_key = f"models/{config['project_name']}_model.pkl"

    # Step 1: Download
    print("⬇️ Step 1: Downloading Data...")
    data_loader = DataLoader(config)
    data_loader.run()

    # Step 2: Preprocessing
    print("🧹 Step 2: Preprocessing data...")
    processor = DataProcessor(
        bucket=os.getenv("S3_BUCKET_NAME"),
        csv_raw_key=csv_raw_key,
        csv_processed_key=csv_processed_key,
        config=config
    )
    processor.run()

    # Step 3: Training
    print("🧠 Step 3: Training model...")
    trainer = ModelTrainer(
        bucket=os.getenv("S3_BUCKET_NAME"),
        csv_processed_key=csv_processed_key,
        model_key=model_key,
        config=config
    )
    trainer.run()

    print("✅ Train Pipeline completed successfully.")

if __name__ == "__main__":
    main()
