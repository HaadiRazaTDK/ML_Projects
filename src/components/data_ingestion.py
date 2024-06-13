import os
import sys
from pathlib import Path
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.exception import CustomException
from src.logger import logging

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

# Ensure the src directory is in the path
sys.path.append(str(Path(__file__).resolve().parent.parent))

@dataclass
class DataIngestionConfig:
    train_data_path: str = str(Path('artifacts/train.csv'))
    test_data_path: str = str(Path('artifacts/test.csv'))
    raw_data_path: str = str(Path('artifacts/data.csv'))

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):
        logging.info("Entered the data ingestion method or component")
        try:
            # Use Pathlib to ensure correct path handling
            data_file = Path(r'notebook\data\StudentsPerformance.csv')
            df = pd.read_csv(data_file)
            logging.info('Read the dataset as dataframe')

            # Ensure the artifacts directory exists
            artifacts_dir = Path(self.ingestion_config.train_data_path).parent
            logging.info(f"Creating directory if it doesn't exist: {artifacts_dir}")
            artifacts_dir.mkdir(parents=True, exist_ok=True)
            logging.info(f"Directory created or already exists: {artifacts_dir}")

            # Save the raw data
            df.to_csv(self.ingestion_config.raw_data_path, index=False, header=True)
            logging.info(f"Raw data saved at: {self.ingestion_config.raw_data_path}")

            logging.info("Train test split initiated")
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)

            # Save the train data
            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            logging.info(f"Train data saved at: {self.ingestion_config.train_data_path}")

            # Save the test data
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)
            logging.info(f"Test data saved at: {self.ingestion_config.test_data_path}")

            logging.info("Ingestion of the data is completed")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise CustomException(e, sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()

    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)