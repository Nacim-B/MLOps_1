import os
import sys
import pandas as pd
from dotenv import load_dotenv
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.dummy import DummyClassifier, DummyRegressor
from sklearn.linear_model import LogisticRegression, LinearRegression
from sklearn.metrics import accuracy_score, mean_squared_error

# Internal imports
sys.path.append("src")
from mlops_project.utils.data_processing import DataProcessor
from mlops_project.utils.s3_handler import S3Handler
from mlops_project.config.config_loader import load_config

def main():
    # Load environment
    load_dotenv()

    # Load config values
    config = load_config("../config/dev.yaml")

    project_name = config["project_name"]
    task_type = config["type"]
    target = config["target"]
    id_column = config["id_column"]
    retrain_only = config["retrain_only"]
    seed = config.get("seed", 42)

    # Define S3 paths
    bucket = os.getenv("S3_BUCKET_NAME")
    raw_key = f"datasets/{os.getenv("CSV_FILENAME")}_raw.csv"
    processed_key = f"datasets/{os.getenv("CSV_FILENAME")}_processed.csv"
    model_key = f"models/logisticregression_final.pkl"

    # Step 1: Run preprocessing
    processor = DataProcessor(
        bucket=bucket,
        raw_key=raw_key,
        processed_key=processed_key,
        target=target,
        id_column=id_column
    )
    processor.run()

    # Step 2: Load processed data
    s3handler = S3Handler(bucket)
    df = s3handler.load_csv_from_s3(processed_key)

    # Restore index if needed
    if id_column and id_column in df.columns:
        df.set_index(id_column, inplace=True)

    X = df.drop(columns=[target])
    y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=seed,
        stratify=y if task_type == "classification" else None
    )

    # Step 3: Training
    if retrain_only:
        from mlops_project.utils.modelisation import ModelTrainer

        trainer = ModelTrainer(bucket, model_key, task_type)
        score = trainer.retrain(X_train, y_train, X_test, y_test)
        trainer.save()

    else:  # from_scratch
        if task_type == "classification":
            model = RandomForestClassifier(n_estimators=100, random_state=seed)
            metric = accuracy_score
        else:
            model = RandomForestRegressor(n_estimators=100, random_state=seed)
            metric = mean_squared_error

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        score = metric(y_test, y_pred)

        print(f"📊 {task_type.capitalize()} score (from scratch): {score:.4f}")
        s3handler.save_model_to_s3(model, model_key)

if __name__ == "__main__":
    main()