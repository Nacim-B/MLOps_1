import os
import mlflow
from mlflow.tracking import MlflowClient


class MLflowHandler:
    """
    MLflow configuration manager that leverages the existing MySQLHandler.
    This class handles MLflow setup, experiment creation, and tracking configuration.
    """

    def __init__(self, mysql_handler, config : dict):
        """
        Initialize MLflow with MySQL backend and S3 artifact storage.

        Args:
            mysql_handler: An instance of MySQLHandler for MySQL connections
        """
        self.mysql_handler = mysql_handler
        self.s3_bucket = os.getenv('S3_BUCKET_NAME')
        self.config = config

        user = mysql_handler.user
        password = mysql_handler.password
        host = mysql_handler.host
        port = mysql_handler.port
        database = mysql_handler.database


        # Construction sécurisée de l'URL
        self.backend_store_uri = f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"

        print(f"Backend store URI: mysql+pymysql://{user}:******@{host}:{port}/{database}")

        # Define artifact location in S3
        self.artifact_uri = f"s3://{self.s3_bucket}/mlruns"

        # Set the tracking URI for this session
        try:
            mlflow.set_tracking_uri(self.backend_store_uri)
            print(f"✅ MLflow tracking URI set to MySQL database")
        except Exception as e:
            print(f"❌ Error setting MLflow tracking URI: {e}")
            print(f"✅ Fallback: MLflow tracking URI set to local SQLite database")

        # Initialize client
        self.client = MlflowClient(tracking_uri=self.backend_store_uri)


    def setup_experiment(self):
        """
        Set up an MLflow experiment for the project.


        Returns:
            tuple: (experiment_id, experiment_name)
        """
        experiment_name = f"{self.config['project_name']}_experiment"

        # Check if experiment exists
        experiment = self.client.get_experiment_by_name(experiment_name)

        if experiment is None:
            try:
                # Create experiment with artifact location in S3
                experiment_id = self.client.create_experiment(
                    name=experiment_name,
                    artifact_location=self.artifact_uri
                )
                print(f"✅ Created MLflow experiment '{experiment_name}' with ID: {experiment_id}")
            except Exception as e:
                print(f"❌ Failed to create MLflow experiment: {str(e)}")
                print("Using default experiment instead.")
                experiment_id = "0"  # Default experiment ID
        else:
            experiment_id = experiment.experiment_id
            print(f"📁 Using existing MLflow experiment '{experiment_name}' (ID: {experiment_id})")

        # Set the active experiment
        mlflow.set_experiment(experiment_name)

        return experiment_id, experiment_name
