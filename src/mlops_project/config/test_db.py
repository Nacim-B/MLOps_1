import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

# --- Config depuis .env ---
host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

# --- Connexion SQLAlchemy ---
conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = sqlalchemy.create_engine(conn_str)

# --- Test : lecture de la table 'pima_diabetes' ---
try:
    df = pd.read_sql("SELECT * FROM pima_diabetes LIMIT 5;", con=engine)
    print("✅ Connexion réussie et données récupérées :")
    print(df)
except Exception as e:
    print("❌ Erreur lors de la connexion ou de la lecture :")
    print(e)
