import os
import sqlalchemy
import pandas as pd


class MySQLHandler:
    def __init__(self):
        self.username = os.getenv("MYSQL_USERNAME")
        self.password = os.getenv("MYSQL_PASSWORD")
        self.host = os.getenv("MYSQL_HOST")
        self.port = os.getenv("MYSQL_PORT", "3306")
        self.database = os.getenv("MYSQL_DATABASE")

        self.engine = self._create_engine()

    def _create_engine(self):
        """
        Create a SQLAlchemy engine for MySQL connection.
        """
        connection_string = (
            f"mysql+pymysql://{self.username}:{self.password}@{self.host}:{self.port}/{self.database}"
        )
        print(f"📥 Connecting to MySQL database: {self.database}")
        return sqlalchemy.create_engine(connection_string)

    def execute_query_from_file(self, query_path: str) -> pd.DataFrame:
        """
        Execute a SQL query loaded from a file and return the result as a DataFrame.
        """
        with open(query_path, "r") as file:
            query = file.read()

        print(f"📄 Executing query from {query_path}")
        return pd.read_sql_query(query, con=self.engine)

    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute a raw SQL query directly (string) and return the result as a DataFrame.
        """
        print(f"📄 Executing provided SQL query")
        return pd.read_sql_query(query, con=self.engine)
