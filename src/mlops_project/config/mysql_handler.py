import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv

load_dotenv()

class MySQLHandler:
    def __init__(self):
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT", "3306")
        self.user = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        self.default_sql_path= os.getenv("MYSQL_SQL_PATH", "./config/queries.sql")
        self.engine = self._create_engine()

    def _create_engine(self):
        conn_str = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return sqlalchemy.create_engine(conn_str)

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            print("✅ MySQL connection successful.")
        except Exception as e:
            print(f"❌ Connection failed: {e}")

    def drop_all_tables(self):
        with self.engine.connect() as conn:
            tables = conn.execute(sqlalchemy.text("SHOW TABLES;")).fetchall()
            table_names = [row[0] for row in tables]
            if not table_names:
                print("ℹ️ No tables found.")
                return

            conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 0;"))
            for table in table_names:
                conn.execute(sqlalchemy.text(f"DROP TABLE IF EXISTS `{table}`;"))
                print(f"🧨 Dropped table: {table}")
            conn.execute(sqlalchemy.text("SET FOREIGN_KEY_CHECKS = 1;"))
            print("✅ All tables dropped.")

    def create_table(self, table_key: str):
        query = self.load_query(table_key)
        with self.engine.connect() as conn:
            conn.execute(sqlalchemy.text(query))
        print(f"✅ Table created from key '{table_key}' in {self.default_sql_path}")

    def populate_from_url(self, table_name: str, url: str, columns: list):
        df = pd.read_csv(url, names=columns)
        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)
        print(f"✅ Inserted {len(df)} rows into '{table_name}'.")

    def read_table(self, table_name: str, limit: int = 5) -> pd.DataFrame:
        with self.engine.connect() as conn:
            query = f"SELECT * FROM {table_name} LIMIT {limit};"
            df = pd.read_sql(query, con=conn)
        print(df)
        return df

    def load_query(self, query_name: str) -> str:
        """
        Extracts a named SQL query from a .sql file using -- name: <query_name> tags.
        """
        with open(self.default_sql_path, "r") as f:
            lines = f.readlines()

        queries = {}
        current_name = None
        current_query = []

        for line in lines:
            line_strip = line.strip()
            if line_strip.startswith("-- name:"):
                if current_name and current_query:
                    queries[current_name] = "\n".join(current_query).strip()
                current_name = line_strip.split("-- name:")[1].strip()
                current_query = []
            elif current_name:
                current_query.append(line.rstrip())

        if current_name and current_query:
            queries[current_name] = "\n".join(current_query).strip()

        if query_name not in queries:
            raise ValueError(f"❌ Query '{query_name}' not found in {self.default_sql_path}")

        return queries[query_name]

    def execute_query(self, query_name: str) -> pd.DataFrame:
        query = self.load_query(query_name)
        with self.engine.connect() as conn:
            df = pd.read_sql(sqlalchemy.text(query), conn)
        print(f"✅ Executed query '{query_name}' from {self.default_sql_path}")
        return df

    def setup(self, create_keys: list):
        """
        Drop all tables and re-create them using the provided keys from SQL file.
        """
        print("🔁 Initializing database...")
        self.drop_all_tables()
        for key in create_keys:
            self.create_table(table_key=key)
        print("✅ Setup complete.")
