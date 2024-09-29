import os
from pathlib import Path

APP_DIR = Path(os.path.abspath(os.path.dirname(__file__))).parent
DATA_DIR = Path(os.path.abspath(os.path.dirname(__file__))).joinpath("data")
