import logging, pyodbc
import pandas as pd
from abc import ABC, abstractmethod 
from dataclasses import dataclass, field
from logger import setup_logger
from utils.database_connection import DatabaseConnection

class GetDataBaseModel(ABC):
    server_name : str
    database_name : str
    stored_procedure_schema : str
    stored_procedure_name : str

    @abstractmethod
    def get_data_as_dataframe(self, *args, **kwargs) -> pd.DataFrame :
        pass

@dataclass
class GetData(GetDataBaseModel):
    server_name : str
    database_name : str
    stored_procedure_schema : str
    stored_procedure_name : str

        # internal variables
    db_connection : pyodbc.Connection | None = field(default=None, init=False)
    logger: logging.Logger = field(default_factory = lambda: setup_logger(__name__))

    def main(self, *args) -> None :
        self.logger.info("Connect to the database...")
        self.db_connection = DatabaseConnection(server_name=self.server_name, database_name=self.database_name).database_connection() # connect to the database
 
    def get_data_as_dataframe(self, *args) -> pd.DataFrame :
        self.logger.info("Create a database connection...")
        self.main()
        try:
            # No parameters
            if not args:
                sql_query = f"EXEC [{self.stored_procedure_schema}].[{self.stored_procedure_name}]"
                return self._get_data_as_dataframe(sql_query, None)

            # Parameters provided
            params = args
            placeholder_list = ", ".join("?" for _ in params)
            sql_query = f"EXEC [{self.stored_procedure_schema}].[{self.stored_procedure_name}] {placeholder_list}"
            return self._get_data_as_dataframe(sql_query, params)

        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def _get_data_as_dataframe(self, sql_query: str, params) -> pd.DataFrame :
        try:
            
            if self.db_connection is not None:
                self.logger.info("Get data as dataframe...")

                with self.db_connection.cursor() as cursor:
                    if params:
                        self.logger.info(f"Executing stored procedure [{self.stored_procedure_schema}].[{self.stored_procedure_name}]")
                        cursor.execute(sql_query, params)
                    else:
                        self.logger.info(f"Executing stored procedure [{self.stored_procedure_schema}].[{self.stored_procedure_name}]")
                        cursor.execute(sql_query)

                    self.logger.info(f"get results from query and form DataFrame")
                    rows = cursor.fetchall()
                    column_list = [col[0] for col in cursor.description]
                    return pd.DataFrame([tuple(row) for row in rows], columns=column_list)

            else:
                self.logger.error("No database Connection...", exc_info=True)
                raise
        
        except pyodbc.Error as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise
        
        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise
