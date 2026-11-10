from pathlib import Path
import shutil
import logging
from logger import setup_logger

class CopyFile:
    """ 
    Handle copying files with proper error handling and logging. 
     
    Attributes: 
        current_folder: Path object representing the location of the file to be copied.
        new_folder: Path object representing the new location where the file has to be copied.
    """ 
    def __init__(self, current_folder : Path, new_folder : Path) -> None:
        """ 
        Initialize Copy File with a current path and new path.
         
        Args: 
            current_folder: String path of the file's current location.
            new_folder: String path of the file's new location.
        """ 
        self.current_folder = Path(current_folder)
        self.new_folder = Path(new_folder)
        self.logger : logging.Logger  = setup_logger(__name__)

    def copy_file(self) -> bool:
        """ 
        Copy a file from current location to new-supplied location.

        Returns: 
            bool: True if a file successfully moved, False on error.
        """ 

        if not self.new_folder.parent.exists():
            self.logger.info(f"Creating Directory : {self.new_folder.name}") 
            self.new_folder.parent.mkdir(parents=True)
            # return True

        try:
            current_folder = str(self.current_folder)
            new_folder_done = str(self.new_folder)

            shutil.copy(current_folder, new_folder_done)
            self.logger.info(f"File Name - '{self.current_folder.name}' has been copied.") 

            return True

        except PermissionError as e: 
            self.logger.error(f"Permission denied : {e}", exc_info=True )
            return False
        
        except NotADirectoryError as e: 
            self.logger.error( 
                f"Invalid directory path {self.current_folder}: {e}", 
                exc_info=True 
            ) 
                # New File Location
            self.logger.error( 
                f"Invalid directory path {self.new_folder}: {e}", 
                exc_info=True 
            ) 

            return False 
        
        except Exception as e: 
                # Current File Location
            self.logger.error( 
                f"Unexpected error creating {self.current_folder.name}: {e}", 
                exc_info=True 
            ) 
                # New File Location
            self.logger.error( 
                f"Unexpected error creating {self.new_folder.name}: {e}", 
                exc_info=True 
            ) 
            return False 
        
