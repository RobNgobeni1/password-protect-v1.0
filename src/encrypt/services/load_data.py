import logging, pyodbc, config
from abc import ABC, abstractmethod 
from dataclasses import dataclass
from logger import setup_logger
from utils.database_connection import DatabaseConnection
from services.execute_stored_procedure import RunStoredProcedure

class LoadDataBaseModel(ABC):
    server_name: str
    database_name: str
    table_schema: str
    table_name: str
    encrypted_column : list 
    upload_column_names : list 
    number_columns : list

    @abstractmethod
    def load_db_data(self, *args) -> bool:
        pass

@dataclass
class LoadData(LoadDataBaseModel):
    process_id: str
    queue_id : str
    server_name: str
    database_name: str
    table_schema: str
    table_name: str
    encrypted_column : list 
    upload_column_names : list 
    number_columns : list
    logger: logging.Logger = setup_logger(__name__)

    def main(self, *args) -> bool | None:

        self.logger.info("Connect to the database...")
        self.db_connection: pyodbc.Connection = (
            DatabaseConnection(
                self.server_name,
                self.database_name
            ).database_connection()
        )
        return self.load_db_data(*args)
        # self.load_db_data(*args)

    def load_db_data(self, *args) -> bool:
        try:
            # No parameters
            if not args:
                self.logger.error("Columns data not supplied...")
                raise 

            # Parameters provided
            else:
                self.logger.debug("Check if there are columns to be encrypted...")
                
                    # Pushing Data - encrypted
                # place_holder : list = []
                # for col in self.upload_column_names:
                #         # check if encrypted
                #     if col in self.encrypted_column:
                #             # numbers 
                #         if col in self.number_columns:
                #             place_holder.append(f"EncryptByKey(Key_GUID('SymmetricKey1'),CONVERT(VARBINARY(MAX), CONVERT(NVARCHAR(MAX), CAST(? as DECIMAL(18,6)))))")

                #             # text
                #         else:
                #             place_holder.append(f"EncryptByKey(Key_GUID('SymmetricKey1'),CONVERT(VARBINARY(MAX), CONVERT(NVARCHAR(MAX), CAST(? as VARCHAR(MAX)))))")
                            
                #     else:
                #         # normal columns
                #             # numbers 
                #         if col in self.number_columns:
                #             place_holder.append(f"CONVERT(NVARCHAR(MAX), CAST(? as DECIMAL(18,6)))")

                #             # text
                #         else:
                #             place_holder.append(f"CONVERT(NVARCHAR(MAX), CAST(? as VARCHAR(MAX)))")

                place_holder : list = self.column_placeholder_handling()
                placeholder_list = ", ".join([columns for columns in place_holder])
                columns_for_insert = ", ".join(_ for _ in self.upload_column_names)
                arguments = [args[0] if len(args) == 1 else arg for arg in args]
                INSERT_SCRIPT = (f"INSERT INTO [{self.table_schema}].[{self.table_name}] "f"({columns_for_insert}) VALUES ({placeholder_list})")
                return self._load_db_data(INSERT_SCRIPT, arguments)

        except Exception as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # error_message : str = str(e)
            # run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, run_status, error_message)

            #     # Update Run Status 
            # _update_queue_status_schema : str =  config.UPDATE_UPLOAD_QUEUE_SP_SCHEMA 
            # _update_queue_status_name : str = config.UPDATE_UPLOAD_QUEUE_SP_NAME
            # self.logger.info(f"Update Run status for for Process Id : {self.process_id}; Queue Id : {self.queue_id} to Uploaded")
            # self._update_queue_id(self.server_name, self.database_name, _update_queue_status_schema, _update_queue_status_name, str(self.queue_id), "Failed", error_message, self.process_id)

            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def column_placeholder_handling(self) -> list:
        try:

            # Pushing Data - encrypted
            place_holder : list = []
            for col in self.upload_column_names:

                    # check if encrypted
                if col in self.encrypted_column:
                        # numbers 
                    if col in self.number_columns:
                        place_holder.append(f"EncryptByKey(Key_GUID('SymmetricKey1'),CONVERT(VARBINARY(MAX), CONVERT(NVARCHAR(MAX), CAST(? as DECIMAL(18,6)))))")

                        # text
                    else:
                        place_holder.append(f"EncryptByKey(Key_GUID('SymmetricKey1'),CONVERT(VARBINARY(MAX), CONVERT(NVARCHAR(MAX), CAST(? as VARCHAR(MAX)))))")
                        
                else:
                    # normal columns
                        # numbers 
                    if col in self.number_columns:
                        # place_holder.append(f"CONVERT(NVARCHAR(MAX), CAST(? as DECIMAL(18,6)))")
                        place_holder.append(f"?")

                        # text
                    else:
                        # place_holder.append(f"CONVERT(NVARCHAR(MAX), CAST(? as VARCHAR(MAX)))")
                        place_holder.append(f"?")

            return place_holder

        except Exception as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # error_message : str = str(e)
            # run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, run_status, error_message)

            #     # Update Run Status 
            # _update_queue_status_schema : str =  config.UPDATE_UPLOAD_QUEUE_SP_SCHEMA 
            # _update_queue_status_name : str = config.UPDATE_UPLOAD_QUEUE_SP_NAME
            # self.logger.info(f"Update Run status for for Process Id : {self.process_id}; Queue Id : {self.queue_id} to Uploaded")
            # self._update_queue_id(self.server_name, self.database_name, _update_queue_status_schema, _update_queue_status_name, str(self.queue_id), "Failed", error_message, self.process_id)

            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def _load_db_data(self, sql_query: str, params) -> bool :
        try:

            if self.db_connection is not None:
                self.logger.info(f"Loading Data into table {self.table_schema} - {self.table_name}...")
                
                with self.db_connection.cursor() as cursor:
                    
                    # Open encryption key
                    cursor.execute("OPEN SYMMETRIC KEY SymmetricKey1 DECRYPTION BY CERTIFICATE ColumnLevelEncryptionCert;")

                    # Run insert
                    if len(params) == 1:
                        # print(sql_query)
                        # print([arg for arg in params[0]])
                        
                        self.logger.info(f"Load Data into database...")
                        # cursor.fast_executemany = True # Fast Execution 
                        cursor.executemany(sql_query, [arg for arg in params[0]])
                        cursor.commit()

                    else:
                        # print(sql_query)
                        # print([arg for arg in params])

                        self.logger.info(f"Load Data into database...")
                        # cursor.fast_executemany = True # Fast Execution 
                        cursor.executemany(sql_query, [arg for arg in params])
                        cursor.commit()

                    # close encryption key 
                    cursor.execute("CLOSE SYMMETRIC KEY SymmetricKey1;")
                return True 
            
            else:
                return False
        

        except pyodbc.Error as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # error_message : str = str(e)
            # run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, run_status, error_message)

            #     # Update Run Status 
            # _update_queue_status_schema : str =  config.UPDATE_UPLOAD_QUEUE_SP_SCHEMA 
            # _update_queue_status_name : str = config.UPDATE_UPLOAD_QUEUE_SP_NAME
            # self.logger.info(f"Update Run status for for Process Id : {self.process_id}; Queue Id : {self.queue_id} to Uploaded")
            # self._update_queue_id(self.server_name, self.database_name, _update_queue_status_schema, _update_queue_status_name, str(self.queue_id), "Failed", error_message, self.process_id)

            self.logger.error(f"Connection Error : {e}", exc_info=True)
            raise

        except Exception as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # error_message : str = str(e)
            # run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, run_status, error_message)

            #     # Update Run Status 
            # _update_queue_status_schema : str =  config.UPDATE_UPLOAD_QUEUE_SP_SCHEMA 
            # _update_queue_status_name : str = config.UPDATE_UPLOAD_QUEUE_SP_NAME
            # self.logger.info(f"Update Run status for for Process Id : {self.process_id}; Queue Id : {self.queue_id} to Uploaded")
            # self._update_queue_id(self.server_name, self.database_name, _update_queue_status_schema, _update_queue_status_name, str(self.queue_id), "Failed", error_message, self.process_id)

            self.logger.error(f"Unknown Error : {e}", exc_info=True)
            raise

    def _update_queue_id(self, server_name : str, database_name : str, sp_schema : str, sp_name : str, queue_id : str , run_status : str, error_message : str, process_id ) -> None : 
        try:
            if queue_id !='': 
                # Update row ids
                self.logger.info(f"Update Queue Id  {queue_id} to status {run_status}...")
                RunStoredProcedure(server_name, database_name, sp_schema, sp_name).main(queue_id, run_status, error_message)

        except ValueError as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # _error_message : str = str(e)
            # _run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, _run_status, _error_message)
            self.logger.error(f"Value Error : {e}", exc_info=True)

        except Exception as e:
            # _server_name : str = config.AGL_SERVER
            # _database_name : str = config.AGL_DATABASE
            # error_sp_schema : str = config.FAILED_PROCESS_SP_SCHEMA
            # error_sp_name : str = config.FAILED_PROCESS_SP_NAME
            # _error_message : str = str(e)
            # _run_status : str = "Failed"
            # RunStoredProcedure(_server_name, _database_name, error_sp_schema, error_sp_name).main(self.process_id, _run_status, _error_message)
            self.logger.error(f"Unknown Error : {e}", exc_info=True)