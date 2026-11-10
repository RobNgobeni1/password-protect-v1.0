from pathlib import Path
import logging
from logger import setup_logger

class FolderIterator:
    """ 
    Handle checking folder and retuning list of objects inside the folder in a list with proper error handling and logging. 
     
    Attributes: 
        folder_path: Path object representing the location of the foleder to be checked.
    """ 
    def __init__(self, current_folder : Path) -> None:
        """ 
        Initialize MoFolder Iterator with a folder path.
         
        Args: 
            current_folder: String path of the folder location.
        """ 
        self.current_folder : Path = Path(current_folder)
        self.logger : logging.Logger  = setup_logger(__name__)

    def main(self) -> list :
        try:
                
            is_this_a_folder : bool = self._verify_folder()
            does_folder_exists : bool = self._verify_if_exists()

            if is_this_a_folder and does_folder_exists:
                get_list : list = self._iterate_folder()

                return get_list
            
            else:
                return []
        
        except Exception as e:
            self.logger.error( 
                f"Unknown Exception {self.current_folder}: {e}", 
                exc_info=True 
            ) 
            raise 

    def _verify_folder(self) -> bool:
        """ 
        Verify the supplied path is a Path.

        Returns: 
            bool: True if a folder is valid.
        """ 
        try:
            self.logger.info("Verify that the folder path supplied is valid...")
            return Path(self.current_folder).is_dir()
        
        except NotADirectoryError as e: 
            self.logger.error( 
                f"Invalid directory path {self.current_folder}: {e}", 
                exc_info=True 
            ) 

            return False 
        
        except Exception as e: 
            self.logger.error( 
                f"Unexpected error {self.current_folder.name}: {e}", 
                exc_info=True 
            ) 
            raise
        

    def _verify_if_exists(self) -> bool:
        """ 
        verify if the supplied path exists.

        Returns: 
            bool: True if a folder is valid.
        """ 
        try:
            self.logger.info("Verify that the folder path supplied exists...")
            return Path(self.current_folder).exists()
        
        except NotADirectoryError as e: 
            self.logger.error( 
                f"Invalid directory path {self.current_folder}: {e}", 
                exc_info=True 
            )   
            raise
        
        except Exception as e: 
            self.logger.error( 
                f"Unexpected error {self.current_folder.name}: {e}", 
                exc_info=True 
            ) 
            raise
        
    
    def _iterate_folder(self) -> list:
        """ 
        Get the list of objects inside folder.

        Returns: 
            List of objects in folder.
        """ 
        try:
            self.logger.info("Verify that the folder path supplied exists...")

            file_list  : list  = [file for file in self.current_folder.iterdir()]
            return file_list
        
        
        except NotADirectoryError as e: 
            self.logger.error( 
                f"Invalid directory path {self.current_folder}: {e}", 
                exc_info=True 
            ) 

            raise
        
        except Exception as e: 
            self.logger.error( 
                f"Unexpected error {self.current_folder.name}: {e}", 
                exc_info=True 
            ) 
            raise