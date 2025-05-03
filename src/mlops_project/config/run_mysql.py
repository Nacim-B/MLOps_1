import os
from dotenv import load_dotenv
from mlops_project.config.mysql_handler import MySQLHandler

load_dotenv()

def main():
    mysql = MySQLHandler()
    mysql.setup(["create_pima_diabetes"])

    columns = [
        "pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin",
        "bmi", "diabetes_pedigree", "age", "diabetes"
    ]
    mysql.populate_from_url("pima_diabetes", os.getenv("CSV_URL"), columns)

    mysql.read_table("pima_diabetes")

    df = mysql.execute_query("select_all")
    print(df.head())

if __name__ == "__main__":
    main()