import os
import sqlalchemy
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()


host = os.getenv("MYSQL_HOST")
port = os.getenv("MYSQL_PORT", "3306")
user = os.getenv("MYSQL_USERNAME")
password = os.getenv("MYSQL_PASSWORD")
database = os.getenv("MYSQL_DATABASE")

# Connexion à MySQL SANS spécifier de base
conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}"
engine = sqlalchemy.create_engine(conn_str)

# Création de la base si elle n'existe pas
create_db_query = f"CREATE DATABASE IF NOT EXISTS {database}"

with engine.connect() as conn:
    conn.execute(sqlalchemy.text(create_db_query))
    print(f"✅ Database '{database}' created or already exists.")
