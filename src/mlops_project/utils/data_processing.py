import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from mlops_project.utils.s3_handler import S3Handler

class DataProcessor:
    def __init__(self, bucket: str, raw_data: pd.DataFrame, csv_processed_key: str, config: dict):
        self.bucket = bucket
        self.df = raw_data
        self.csv_processed_key = csv_processed_key
        self.config = config
        self.target = config["target"]
        self.id_column = config.get("id_column", None)
        self.s3 = S3Handler(bucket, config)
        self.scaler = StandardScaler()

    def load_data(self):
        # Set ID column as index if applicable
        if self.id_column and self.id_column in self.df.columns:
            if self.df[self.id_column].is_unique and self.df[self.id_column].isna().sum() == 0:
                self.df = self.df.set_index(self.id_column)
                print(f"📎 Set '{self.id_column}' as index.")

    def clean(self):
        self.df = self.df.drop_duplicates()
        self.df = self.df.dropna(axis=1, how="all")

        # Get number of unique values per column
        n_unique = self.df.nunique()

        # Drop constant columns (same value for all rows)
        drop_constant = n_unique[n_unique == 1].index.tolist()

        # Drop fully unique columns that are not numeric (e.g., IDs, strings)
        non_numeric_cols = self.df.select_dtypes(exclude=["number"]).columns
        drop_unique_non_numeric = [col for col in n_unique[n_unique == len(self.df)].index if col in non_numeric_cols]

        # Combine, excluding the target
        drop_cols = [col for col in (drop_constant + drop_unique_non_numeric) if col != self.target]

        # Drop the columns
        self.df = self.df.drop(columns=drop_cols)
        print(f"🧹 Dropped columns: {drop_cols}")

    def handle_missing_values(self):
        # Numerical
        num_cols = self.df.select_dtypes(include=["number"]).columns.difference([self.target])
        for col in num_cols:
            median = self.df[col].median()
            self.df[col] = self.df[col].fillna(median)

        # Categorical
        cat_cols = self.df.select_dtypes(include=["object", "category"]).columns.difference([self.target])
        for col in cat_cols:
            if self.df[col].isna().any():
                most_common = self.df[col].mode()[0]
                self.df[col] = self.df[col].fillna(most_common)

    def transform(self):
        # Numerical standardisation
        num_cols = self.df.select_dtypes(include=["number"]).columns.difference([self.target])
        discrete_as_cat = [col for col in num_cols if self.df[col].nunique() <= 5]
        scale_cols = [col for col in num_cols if col not in discrete_as_cat]

        self.df[scale_cols] = self.scaler.fit_transform(self.df[scale_cols])

        # Categorical encoding
        cat_cols = (self.df.select_dtypes(include=["object", "category"]).columns.difference([self.target]).tolist()
                    + discrete_as_cat)
        cat_cols = [col for col in cat_cols if col != self.target]

        self.df = pd.get_dummies(self.df, columns=cat_cols, drop_first=False)

    def save_processed(self):
        self.s3.save_csv_to_s3(self.df, self.csv_processed_key)
        print(f"✅ Processed data saved to s3://{self.bucket}/{self.csv_processed_key}")

    def run(self):
        self.load_data()
        self.clean()
        self.handle_missing_values()
        self.transform()
        self.save_processed()
