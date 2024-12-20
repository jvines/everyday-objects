import logging
import time
from sqlalchemy import create_engine, select, text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (INFO, DEBUG, ERROR, etc.)
    format='%(asctime)s - %(levelname)s - %(message)s',  # Set log message format
)

logger = logging.getLogger(__name__)  # Create a logger for this file

SQLALCHEMY_DATABASE_URL = 'postgresql://postgres:pepe1234@postgres/everyday_objects'

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)


def wait_for_db_connection(max_retries=10, delay=10):
    """Try to connect to the DB with retries."""
    for attempt in range(max_retries):
        try:
            with engine.connect() as connection:
                # Ping the database using the connection
                connection.execute(text("SELECT 1"))
                Base.metadata.create_all(bind=engine)  # Optional: Create all tables if they don't exist
                logger.info("Database is available.")  # Log success
                return True
        except Exception as e:
            logger.warning(e)
            logger.warning(f"Attempt {attempt + 1}/{max_retries} failed. Retrying...")  # Log warning
            time.sleep(delay)
    logger.error("Max retries reached. Could not connect to the database.")  # Log error
    return False

LocalSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = LocalSession()
    try:
        yield db
    finally:
        db.close()
