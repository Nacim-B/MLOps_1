from dotenv import load_dotenv
from mlops_project.utils.data_loader import DataLoader
from mlops_project.config.config_loader import load_config

def download_raw_csv():
    config = load_config("../config/dev.yaml")
    load_dotenv()

    data_loader = DataLoader(config)
    data_loader.run()

if __name__ == "__main__":
    download_raw_csv()
