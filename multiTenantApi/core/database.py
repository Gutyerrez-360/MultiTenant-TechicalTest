from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# global variables
from multiTenantApi.config.config import ENV


DATABASE_URL = (
    f"postgresql+psycopg2://{ENV['DB_USER']}:{ENV['DB_PASSWORD']}"
    f"@{ENV['DB_HOST']}:{ENV['DB_PORT']}/{ENV['DB_NAME']}"
)

engine = create_engine(DATABASE_URL, future=True)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    autocommit=False,
    future=True,
)