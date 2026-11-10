import os
from dotenv import load_dotenv
from pathlib import Path

# LOAD ENVIRONMENT
load_dotenv()

# GET WORKING DIRECTORIES
MAIN_DIR :  str | None  = os.getenv("MAIN_DIRECTORY")
WORKING_DIR :  str | None  = os.getenv("WORKING_DIRECTORY")

if MAIN_DIR is None:
    raise ValueError("MAIN_DIRECTORY not found in .env file")

if WORKING_DIR is None:
    raise ValueError("WORKING_DIRECTORY not found in .env file")

MAIN_DIRECTORY : Path = Path(MAIN_DIR)
WORKING_DIRECTORY : Path = Path(WORKING_DIR)