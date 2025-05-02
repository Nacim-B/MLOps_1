import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

# --- Charger les variables d'environnement ---
load_dotenv()

host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

# --- Connexion SQLAlchemy ---
conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = sqlalchemy.create_engine(conn_str)

# --- Charger les données depuis URL ---
url = "https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv"
columns = [
    "pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin",
    "bmi", "diabetes_pedigree", "age", "diabetes"
]

df = pd.read_csv(url, names=columns)

# --- Insertion dans la table pima_diabetes ---
df.to_sql("pima_diabetes", con=engine, if_exists="append", index=False)
print("✅ Données insérées dans 'pima_diabetes'")
