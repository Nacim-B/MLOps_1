import os
from dotenv import load_dotenv

from mlops_project.config.config_loader import load_config
from mlops_project.utils.data_loader import DataLoader
from mlops_project.utils.data_processing import DataProcessor
from mlops_project.utils.model_training import ModelTrainer

def main():
    # Load env + config
    load_dotenv()
    config = load_config("./config/dev.yaml")
    # Step 1: Download
    print("⬇️ Step 1: Downloading Data...")
    data_loader = DataLoader(config)
    df_raw = data_loader.run()

    # Step 2: Preprocessing
    print("🧹 Step 2: Preprocessing data...")
    processor = DataProcessor(
        bucket=os.getenv("S3_BUCKET_NAME"),
        raw_data=df_raw,
        config=config
    )
    df_processed = processor.run()

    # Step 3: Training
    print("🧠 Step 3: Training model...")
    trainer = ModelTrainer(
        bucket=os.getenv("S3_BUCKET_NAME"),
        df_processed=df_processed,
        model_key=f"models/{config['project_name']}_model.pkl",
        config=config
    )
    trainer.run()

    print("✅ Train Pipeline completed successfully.")

if __name__ == "__main__":
    main()
