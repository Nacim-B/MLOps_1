import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from mlops_project.utils.load_from_s3 import S3Loader

class DataProcessor:
    def __init__(self, bucket: str, raw_key: str, processed_key: str, target: str, id_column: str = None):
        self.bucket = bucket
        self.raw_key = raw_key
        self.processed_key = processed_key
        self.target = target
        self.id_column = id_column
        self.s3 = S3Loader(bucket)
        self.scaler = StandardScaler()
        self.df = self.s3.load_csv_from_s3(self.raw_key)

    def load_data(self):
        # Set ID column as index if applicable
        if self.id_column and self.id_column in self.df.columns:
            if self.df[self.id_column].is_unique and self.df[self.id_column].isna().sum() == 0:
                self.df.set_index(self.id_column, inplace=True)
                print(f"📎 Set '{self.id_column}' as index.")

    def clean(self):
        self.df.drop_duplicates(inplace=True)
        self.df.dropna(axis=1, how="all", inplace=True)

        # Drop constant and fully unique columns
        nunique = self.df.nunique()
        drop_cols = nunique[nunique <= 1].index.tolist() + nunique[nunique == len(self.df)].index.tolist()
        drop_cols = [col for col in drop_cols if col != self.target]
        self.df.drop(columns=drop_cols, inplace=True)
        print(f"🧹 Dropped columns: {drop_cols}")

    def handle_missing_values(self):
        # Numerical
        num_cols = self.df.select_dtypes(include=["number"]).columns.drop(self.target)
        for col in num_cols:
            median = self.df[col].median()
            self.df[col].fillna(median, inplace=True)

        # Categorical
        cat_cols = self.df.select_dtypes(include=["object", "category"]).columns
        for col in cat_cols:
            if self.df[col].isna().any():
                most_common = self.df[col].mode()[0]
                self.df[col].fillna(most_common, inplace=True)

    def transform(self):
        # Numerical standardisation
        num_cols = self.df.select_dtypes(include=["number"]).columns.drop(self.target)
        discrete_as_cat = [col for col in num_cols if self.df[col].nunique() <= 5]
        scale_cols = [col for col in num_cols if col not in discrete_as_cat]

        self.df[scale_cols] = self.scaler.fit_transform(self.df[scale_cols])

        # Categorical encoding
        cat_cols = self.df.select_dtypes(include=["object", "category"]).columns.tolist() + discrete_as_cat
        cat_cols = [col for col in cat_cols if col != self.target]

        self.df = pd.get_dummies(self.df, columns=cat_cols, drop_first=False)

    def save_processed(self):
        self.s3.save_model(self.df, self.processed_key)  # or create a save_csv method if you prefer CSV
        print(f"✅ Processed data saved to s3://{self.bucket}/{self.processed_key}")

    def run(self):
        self.load_data()
        self.clean()
        self.handle_missing_values()
        self.transform()
        self.save_processed()
