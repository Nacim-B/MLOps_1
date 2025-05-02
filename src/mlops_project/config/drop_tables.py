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

# Connexion SQLAlchemy
conn_str = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
engine = sqlalchemy.create_engine(conn_str)


def drop_all_tables():
    with engine.connect() as conn:
        # Récupérer la liste des tables
        result = conn.execute(sqlalchemy.text("SHOW TABLES;"))
        tables = [row[0] for row in result.fetchall()]

        if not tables:
            print("ℹ️ Aucune table à supprimer.")
            return

        print(f"🧨 Suppression des tables : {tables}")

        # Désactiver les contraintes pour permettre la suppression
        conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 0;"))
        for table in tables:
            conn.execute(sqlalchemy.text(f"DROP TABLE IF EXISTS `{table}`;"))
            print(f"✅ Table supprimée : {table}")
        conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 1;"))
        print("🎉 Toutes les tables ont été supprimées.")


if __name__ == "__main__":
    drop_all_tables()
