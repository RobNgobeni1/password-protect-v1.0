from pathlib import Path
import shutil
import logging
from logger import setup_logger

class ManageFolder:
    """
    Handle directory creation and deleting with proper error handling and logging.

    Attributes:
        folder_path: Path object representing the folder to create/delete
    """

    def __init__(self, folder_path: Path) -> None:
        """
        Initialize ManageFolder with a path.

        Args:
            folder_path: String path to the folder
        """
        self.folder_path = Path(folder_path)
        self.logger : logging.Logger  = setup_logger(__name__)

    def create_directory(self) -> bool:
        """
        Create a directory if it doesn't exist.

        Returns:
            bool: True if created successfully or already exists, False on error
        """

        if self.folder_path.exists():
            self.logger.warning(f"Directory already exists: {self.folder_path}")
            return True

        try:
            self.logger.info(f"Creating directory: {self.folder_path}")
            self.folder_path.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"Created Folder : {self.folder_path}")
            return True

        except PermissionError as e:
            self.logger.error(
                f"Permission denied creating {self.folder_path}: {e}",
                exc_info=True
            )
            return False

        except NotADirectoryError as e:
            self.logger.error(
                f"Invalid directory path {self.folder_path}: {e}",
                exc_info=True
            )
            return False

        except Exception as e:
            self.logger.error(
                f"Unexpected error creating {self.folder_path}: {e}",
                exc_info=True
            )
            return False

    def drop_folder(self) -> bool:
        """
        Deleting an existing Directory.

        Returns:
            bool: True if created successfully deleted, False on error
        """

        if Path(self.folder_path).exists():
            try:
                shutil.rmtree(self.folder_path)
                self.logger.info(f"Folder {self.folder_path} deleted.")
                return True

            except NotADirectoryError as e:
                self.logger.error(
                    f"Invalid directory path {self.folder_path}: {e}",
                    exc_info=True
                )
                return False

            except PermissionError as e:
                self.logger.error(
                    f"Permission denied Deleting {self.folder_path}: {e}",
                    exc_info=True
                )
                return False

            except OSError as e:
                self.logger.error(
                    f"OS Error - {e}.",
                    exc_info=True
                )
                return False
        else:
            self.logger.error(
                f"Folder does not exists.",
                exc_info=True
            )
            return False