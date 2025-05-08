from mlops_project.utils.mysql_handler import MySQLHandler
from mlops_project.config.config_loader import load_config

def main():
    config = load_config("./dev.yaml")
    mysql = MySQLHandler(config, "./queries.sql")

    # Reset the table using the named query
    mysql.reset_table(query_key="create_table", table_name="pima_diabetes")

    # Populate the table
    mysql.populate_table_from_csv_url(
        table_name="pima_diabetes",
        url="https://raw.githubusercontent.com/jbrownlee/Datasets/master/pima-indians-diabetes.data.csv",
        columns=[
            "pregnancies", "glucose", "blood_pressure", "skin_thickness", "insulin",
            "bmi", "diabetes_pedigree", "age", "diabetes"
        ]
    )

if __name__ == "__main__":
    main()
