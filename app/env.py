from pathlib import Path

from flask_sqlalchemy import SQLAlchemy


APP_DIR = Path(__file__).absolute().parent
db = SQLAlchemy()

