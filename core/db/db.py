from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.exc import SQLAlchemyError
import logging as log

DATABASE_URL = "sqlite+aiosqlite:///./events.db"

log.info(f"Initializing database connection: {DATABASE_URL}")

try:
    engine = create_async_engine(DATABASE_URL, echo=True)
    AsyncSessionLocal = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)
    Base = declarative_base()
    log.info("Database engine and session factory created successfully")
except Exception as e:
    log.error(f"Failed to initialize database: {e}")
    raise

async def get_db():
    """
    Database session dependency for FastAPI routes.
    Yields a database session and handles cleanup and errors.
    """
    log.debug("Creating new database session")
    async with AsyncSessionLocal() as session:
        try:
            yield session
            log.debug("Database session completed successfully")
        except SQLAlchemyError as e:
            log.error(f"Database error occurred: {e}")
            await session.rollback()
            log.warning("Database session rolled back due to error")
            raise
        except Exception as e:
            log.error(f"Unexpected error in database session: {e}")
            await session.rollback()
            raise
        finally:
            log.debug("Closing database session")
