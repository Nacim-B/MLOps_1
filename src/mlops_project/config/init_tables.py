import os
import sqlalchemy
from dotenv import load_dotenv

# Load environment variables from .env (for local usage)
load_dotenv()

# Credentials (from .env)
creds = {
    "username": os.getenv("MYSQL_USERNAME"),
    "password": os.getenv("MYSQL_PASSWORD"),
    "host": os.getenv("MYSQL_HOST"),
    "port": os.getenv("MYSQL_PORT", "3306"),
    "database": os.getenv("MYSQL_DATABASE")
}

# SQLAlchemy connection string
conn_str = f"mysql+pymysql://{creds['username']}:{creds['password']}@{creds['host']}:{creds['port']}/{creds['database']}"
engine = sqlalchemy.create_engine(conn_str)

# --- SQL query to create pima_diabetes table ---
CREATE_PIMA_TABLE = """
CREATE TABLE IF NOT EXISTS pima_diabetes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    pregnancies INT,
    glucose FLOAT,
    blood_pressure FLOAT,
    skin_thickness FLOAT,
    insulin FLOAT,
    bmi FLOAT,
    diabetes_pedigree FLOAT,
    age INT,
    diabetes INT
);
"""

def initialize_db():
    with engine.connect() as conn:
        conn.execute(sqlalchemy.text(CREATE_PIMA_TABLE))
        print("✅ Table 'pima_diabetes' created or already exists.")

if __name__ == "__main__":
    initialize_db()
