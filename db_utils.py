import yaml
from sqlalchemy import create_engine
import pandas as pd
from typing import Dict, Any
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Configuration
BASE_DIR = Path(__file__).resolve().parent
CREDENTIALS_FILE = BASE_DIR / 'credentials.yaml'
CSV_OUTPUT_FILE = BASE_DIR / 'loan_payments.csv'

class RDSDatabaseConnector:
    """
    A class for connecting to and interacting with an RDS database.

    This class provides methods to establish a connection to a PostgreSQL database
    on Amazon RDS, fetch data from tables, and perform operations like saving to
    and loading from CSV files.

    Attributes:
        host (str): The host address of the RDS instance.
        database (str): The name of the database to connect to.
        user (str): The username for database authentication.
        password (str): The password for database authentication.
        port (str): The port number for the database connection.
        engine (sqlalchemy.engine.base.Engine): SQLAlchemy engine for database operations.
    """

    def __init__(self, credentials: Dict[str, str]) -> None:
        """
        Initialize the RDSDatabaseConnector with database connection parameters.

        Args:
            credentials (Dict[str, str]): A dictionary containing the database credentials.
                Expected keys: RDS_HOST, RDS_DATABASE, RDS_USER, RDS_PASSWORD, RDS_PORT.

        Raises:
            KeyError: If any required credential is missing from the dictionary.
        """
        try:
            self.host: str = credentials['RDS_HOST']
            self.database: str = credentials['RDS_DATABASE']
            self.user: str = credentials['RDS_USER']
            self.password: str = credentials['RDS_PASSWORD']
            self.port: str = credentials['RDS_PORT']
            self.engine = self._create_engine()
        except KeyError as e:
            logging.error(f"Missing credential: {e}")
            raise

    def _create_engine(self) -> Any:
        """
        Initialize a SQLAlchemy engine using the provided credentials.

        Returns:
            sqlalchemy.engine.base.Engine: A SQLAlchemy engine object.

        Raises:
            Exception: If engine creation fails.
        """
        try:
            connection_string = f"postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
            return create_engine(connection_string)
        except Exception as e:
            logging.error(f"Failed to create database engine: {e}")
            raise

    def fetch_table_data(self, table_name: str) -> pd.DataFrame:
        """
        Load data from the specified table in the database.

        Args:
            table_name (str): The name of the table to query.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the table data.

        Raises:
            Exception: If data fetching fails.
        """
        try:
            query = f"SELECT * FROM {table_name}"
            return pd.read_sql(query, self.engine)
        except Exception as e:
            logging.error(f"Failed to fetch data from table {table_name}: {e}")
            raise

    @staticmethod
    def save_dataframe_to_csv(dataframe: pd.DataFrame, file_path: Path) -> None:
        """
        Save the DataFrame to a CSV file.

        Args:
            dataframe (pd.DataFrame): The Pandas DataFrame to save.
            file_path (Path): The file path where the CSV file will be saved.

        Raises:
            Exception: If saving the DataFrame to CSV fails.
        """
        try:
            dataframe.to_csv(file_path, index=False)
            logging.info(f"Data saved to {file_path}")
        except Exception as e:
            logging.error(f"Failed to save DataFrame to CSV: {e}")
            raise

    @staticmethod
    def load_dataframe_from_csv(file_path: Path) -> pd.DataFrame:
        """
        Load data from a CSV file into a Pandas DataFrame.

        Args:
            file_path (Path): The file path of the CSV file.

        Returns:
            pd.DataFrame: A Pandas DataFrame containing the data from the CSV file.

        Raises:
            Exception: If loading the DataFrame from CSV fails.
        """
        try:
            dataframe = pd.read_csv(file_path)
            logging.info(f"Data loaded from {file_path}. Shape: {dataframe.shape}")
            return dataframe
        except Exception as e:
            logging.error(f"Failed to load DataFrame from CSV: {e}")
            raise

def load_credentials(file_path: Path) -> Dict[str, str]:
    """
    Load the database credentials from a YAML file.

    Args:
        file_path (Path): The path to the YAML file containing the credentials.

    Returns:
        Dict[str, str]: A dictionary with the credentials.

    Raises:
        Exception: If loading credentials from the YAML file fails.
    """
    try:
        with open(file_path, 'r') as file:
            return yaml.safe_load(file)
    except Exception as e:
        logging.error(f"Failed to load credentials from {file_path}: {e}")
        raise

def main() -> None:
    """
    Main execution function to demonstrate the RDSDatabaseConnector usage.

    This function performs the following steps:
    1. Load database credentials
    2. Initialize the database connecto2r
    3. Fetch data from the 'loan_payments' table
    4. Save the fetched data to a CSV file
    5. Load the data back from the CSV file
    """
    try:
        # Load credentials and initialize database connector
        credentials = load_credentials(CREDENTIALS_FILE)
        db_connector = RDSDatabaseConnector(credentials)
        
        # Fetch data from the 'loan_payments' table
        loan_payments_data = db_connector.fetch_table_data('loan_payments')
        
        # Save fetched data to CSV
        RDSDatabaseConnector.save_dataframe_to_csv(loan_payments_data, CSV_OUTPUT_FILE)
        
        # Load data from CSV and display a sample
        loaded_data = RDSDatabaseConnector.load_dataframe_from_csv(CSV_OUTPUT_FILE)
        logging.info(f"Loaded data sample:\n{loaded_data.head()}")
    except Exception as e:
        logging.error(f"An error occurred in the main execution: {e}")

if __name__ == "__main__":
    main()