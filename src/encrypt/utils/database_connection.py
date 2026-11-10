import logging, pyodbc
from abc import ABC, abstractmethod 
from dataclasses import dataclass, field
from logger import setup_logger
from utils.connection_string import SqlServer
from utils.connection_string import OdbcDrivers

class ConnectionModel(ABC):
    server_name : str
    database_name : str
    
    @abstractmethod
    def database_connection(self) -> pyodbc.Connection:
        pass

    @abstractmethod
    def close_database_connection(self) -> bool:
        pass

@dataclass
class DatabaseConnection(ConnectionModel):
    server_name : str
    database_name : str
    db_connection : pyodbc.Connection | None = field(default=None, init=False)
    logger : logging.Logger  = setup_logger(__name__)

    def database_connection(self) -> pyodbc.Connection:
        try: 
            self.logger.info("Connecting to the Database...") # connect to DB
            connection_str = SqlServer(self.server_name, self.database_name).connection_string()
            # connection_str = OdbcDrivers(self.server_name, self.database_name).connection_string()
            self.db_connection =  pyodbc.connect(connection_str)
            self.logger.info("Connected to database...")
            return self.db_connection

        except pyodbc.Error as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise
        
        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def close_database_connection(self) -> bool:
        try: 
            if self.db_connection is not None:
                self.logger.info("closing Database connection...") # connect to DB
                self.db_connection.close()
                
                self.logger.info("closed database connection ...")
                return True
            
            else:
                return False

        except pyodbc.Error as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise
        
        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise
