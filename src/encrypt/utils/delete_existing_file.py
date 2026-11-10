import logging
from pathlib import Path
from abc import ABC, abstractmethod 
from dataclasses import dataclass
from logger import setup_logger

class DeleteFileModel(ABC):
    file_path : Path

    @abstractmethod
    def delete_if_exists(self) -> None:
        pass

@dataclass
class DeleteFile(DeleteFileModel):
    file_path : Path
    logger : logging.Logger  = setup_logger(__name__)
   
    def delete_if_exists(self) -> None:
        template_file_name : Path = self.file_path

        if Path(template_file_name).exists():
            try:
                self.logger.info(f"Delete excel file {template_file_name}...")
                Path(template_file_name).unlink()
                self.logger.info(f"Excel file {template_file_name} deleted...")

            except PermissionError as e: 
                self.logger.error(f"Permission denied: {e}", exc_info=True )

            except FileExistsError as e: 
                self.logger.error(f"File Exists Error: {e}", exc_info=True ) 

            except NotADirectoryError as e: 
                self.logger.error(f"Invalid directory path: {e}", exc_info=True ) 
            
            except Exception as e:
                self.logger.error(f"Unknown Error : {e}", exc_info=True)