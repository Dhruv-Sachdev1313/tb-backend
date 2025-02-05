import os
import dotenv

dotenv.load_dotenv()


class Config:
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", "postgresql://user:password@localhost/tick_data")
    SQLALCHEMY_TRACK_MODIFICATIONS = False