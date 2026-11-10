import logging
from abc import ABC, abstractmethod 
from dataclasses import dataclass
from logger import setup_logger

class StringModel(ABC):
    server_name : str
    database_name : str

    @abstractmethod
    def connection_string(self) -> str:
        pass

@dataclass
class SqlServer(StringModel):
    server_name : str
    database_name : str
    logger : logging.Logger  = setup_logger(__name__)

    def connection_string(self) -> str:
        try: 
            self.logger.info("generating connection string for SQL Server drivers...")
            driver_name : str = "SQL Server"
            # connection_str = str(f"DRIVER={{{driver_name}}};SERVER={self.server_name};DATABASE={self.database_name};Trusted_Connection=yes;UseFMTONLY=Yes;")
            connection_str = str(
                f"DRIVER={driver_name};"
                f"SERVER={self.server_name};"
                f"DATABASE={self.database_name};"
                "Trusted_Connection=yes;"
                "UseFMTONLY=Yes;"
            )
            return connection_str

        except ConnectionError as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise
        
        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

@dataclass
class OdbcDrivers(StringModel):
    server_name : str
    database_name : str
    logger : logging.Logger  = setup_logger(__name__)

    def connection_string(self) -> str:
        try: 
            self.logger.info("generating connection string for ODBC Driver 17 for SQL Server drivers...")
            driver_name : str = "ODBC Driver 17 for SQL Server"
            # connection_str = str(f"DRIVER={{{driver_name}}};SERVER={self.server_name};DATABASE={self.database_name};Trusted_Connection=yes;UseFMTONLY=Yes;")

            connection_str = str(
                f"DRIVER={driver_name};"
                f"SERVER={self.server_name};"
                f"DATABASE={self.database_name};"
                "Trusted_Connection=yes;"
                "UseFMTONLY=Yes;"
                 )

            return connection_str

        except ConnectionError as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise
        
        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise