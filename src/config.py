from dotenv import load_dotenv
import os
from sqlmodel import create_engine

load_dotenv()

CAPTCHA_KEY = os.getenv("CAPTCHA_KEY", "")
EMAIL = os.getenv("EMAIL", "")
PASSWORD = os.getenv("PASSWORD", "")
# Database
DB_CONNECTION = os.getenv("DB_CONNECTION", "postgresql+psycopg2")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", 3306)
DB_DATABASE = os.getenv("DB_DATABASE", "")
DB_USERNAME = os.getenv("DB_USERNAME", "")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")
# Connection URL
DATABASE_URL = f"{DB_CONNECTION}://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_DATABASE}"
# ENGINE
ENGINE = create_engine(DATABASE_URL)
# Environment
ENV = os.getenv("ENV", "dev")
