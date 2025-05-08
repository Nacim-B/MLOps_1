import os
import pandas as pd
import sqlalchemy
from dotenv import load_dotenv
import requests
from io import StringIO
load_dotenv()

class MySQLHandler:
    def __init__(self, config: dict,  sql_file_path: str = "config/queries.sql"):
        """
        Initialize MySQLHandler from environment variables.
        """
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT", "3306")
        self.user = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.database = os.getenv("MYSQL_DATABASE")
        self.sql_file_path = sql_file_path

        self.config = config
        self.engine = self._create_engine()

    def _create_engine(self):
        conn_str = f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        return sqlalchemy.create_engine(conn_str)

    def load_data_from_db(self, query_name: str) -> pd.DataFrame:
        """
        Loads data from the database by executing a named query from the SQL file.

        Args:
            query_name (str): The name of the SQL query to execute (defined via `-- name:`).

        Returns:
            pd.DataFrame: The result of the query as a DataFrame.
        """
        query = self._load_query(query_name)
        with self.engine.connect() as conn:
            df = pd.read_sql(sqlalchemy.text(query), conn)
        print(f"✅ Loaded data using query '{query_name}'")
        return df

    def _load_query(self, query_name: str) -> str:
        """
        Extracts a named SQL query from a .sql file using -- name: <query_name> tags.
        """
        with open(self.sql_file_path, "r") as f:
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
            raise ValueError(f"❌ Query '{query_name}' not found in {self.sql_file_path}")

        return queries[query_name]

    def test_connection(self):
        try:
            with self.engine.connect() as conn:
                conn.execute(sqlalchemy.text("SELECT 1"))
            print("✅ MySQL connection successful.")
        except Exception as e:
            print(f"❌ Connection failed: {e}")

    def reset_table(self, query_key: str, table_name: str):
        """
        Drops a specific table if it exists and recreates it using a named SQL query.

        Args:
            query_key (str): The name of the CREATE TABLE query in the SQL file (e.g. 'create_table').
            table_name (str): The exact name of the table to drop and recreate.
        """
        # Load the CREATE TABLE SQL query
        query = self._load_query(query_key)

        print(f"🔁 Resetting table '{table_name}' from query '{query_key}'...")

        with self.engine.connect() as conn:
            # Check if the table exists
            existing = conn.execute(sqlalchemy.text(f"SHOW TABLES LIKE '{table_name}'")).fetchone()
            if existing:
                conn.execute(sqlalchemy.text(f"DROP TABLE `{table_name}`"))
                print(f"🗑 Dropped existing table '{table_name}'")

            # Create the table from the SQL file
            conn.execute(sqlalchemy.text(query))
            print(f"✅ Recreated table '{table_name}' using query '{query_key}'")

    def populate_table_from_csv_url(self, table_name: str, url: str, columns: list):
        """
        Loads a CSV from a URL using S3Handler and inserts it into a MySQL table.

        Args:
            table_name (str): Target MySQL table name.
            url (str): Public CSV URL to load.
            columns (list): List of column names for the CSV.
        """

        try:
            response = requests.get(url)
            response.raise_for_status()
            print(f"✅ CSV downloaded from {url}")
            csv_content = response.text
            df = pd.read_csv(StringIO(csv_content), names=columns, sep=self.config['csv_separator'],engine="python")
        except requests.RequestException as e:
            print(f"❌ Failed to download CSV: {e}")
            raise

        # Insert into MySQL
        df.to_sql(table_name, con=self.engine, if_exists="append", index=False)
        print(f"✅ Inserted {len(df)} rows into table '{table_name}' from {url}")



