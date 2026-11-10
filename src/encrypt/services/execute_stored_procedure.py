import logging
import pyodbc
from abc import ABC, abstractmethod 
from dataclasses import dataclass
from logger import setup_logger
from utils.database_connection import DatabaseConnection


class BaseModel(ABC):
    server_name: str
    database_name: str
    stored_proc_schema: str
    stored_proc_name: str

    @abstractmethod
    def run_stored_procedure(self, *args) -> None:
        pass


@dataclass
class RunStoredProcedure(BaseModel):
    server_name: str
    database_name: str
    stored_proc_schema: str
    stored_proc_name: str
    
    def main(self, *args) -> None:
        self.logger: logging.Logger = setup_logger(__name__)

        self.logger.info("Connect to the database...")
        self.db_connection: pyodbc.Connection = (
            DatabaseConnection(
                server_name=self.server_name,
                database_name=self.database_name
            ).database_connection()
        )

        self.logger.info("Execute Stored Procedure...")
        self.run_stored_procedure(*args)

    def run_stored_procedure(self, *args) -> None:
        try:
            # No parameters
            if not args:
                sql_query = f"EXEC [{self.stored_proc_schema}].[{self.stored_proc_name}]"
                self._run_stored_procedure(sql_query, None)
                return

            # Parameters provided
            params = args
            placeholder_list = ", ".join("?" for _ in params)
            sql_query = f"EXEC [{self.stored_proc_schema}].[{self.stored_proc_name}] {placeholder_list}"
            self._run_stored_procedure(sql_query, params)

        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def _run_stored_procedure(self, sql_query: str, params) -> None:
        try:
            if self.db_connection is not None:
                self.logger.info("Run stored procedure...")

                with self.db_connection.cursor() as cursor:
                    if params:
                        self.logger.info(f"Executing stored procedure [{self.stored_proc_schema}].[{self.stored_proc_name}]")
                        cursor.execute(sql_query, params)
                    else:
                        self.logger.info(f"Executing stored procedure [{self.stored_proc_schema}].[{self.stored_proc_name}]")
                        cursor.execute(sql_query)
                    
                    row = cursor.fetchone()
                    if row and getattr(row, "Success", 0) == 1:
                        self.logger.info("Executing procedure succeeded.")

        except pyodbc.Error as e:
            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise

        except Exception as e:
            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise