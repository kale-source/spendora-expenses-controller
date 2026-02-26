from datetime import datetime

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from sqlalchemy.engine import URL


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables.

    IMPORTANT: This configuration uses separate database connection parameters
    instead of a single DATABASE_URL string. This provides better flexibility
    and security when managing database connections.
    """
    model_config = SettingsConfigDict(
        env_file='.env',
        env_file_encoding='utf-8',
        case_sensitive=True,
        extra='ignore'
    )
    # PATTERN CONFIGURATIONS
    APP_NAME: str = Field(default="Spendora", env="APP_NAME")
    APP_VERSION: str = Field(default="1.0.0", description="Application version")
    DATE_TIME: str = Field(
        default_factory=lambda: datetime.now().strftime(
            "%Y-%m-%d'T'%H:%M:%S.%f")[:-3]
    )
    DEBUG: bool = Field(default=False, env="DEBUG_MODE")
    ENVIRONMENT: str = Field(
        default="development", description="Environment (development, production, test)")
    ASYNC_MODE: bool = Field( default=True, description="liga/desliga async engine")
        
    # Database Configuration - Using separate parameters (NOT DATABASE_URL)
    DB_USER: str = Field(default="postgres", description="Database user")
    DB_PASSWORD: str = Field(default="postgrespwd", description="Database password")
    DB_HOST: str = Field(default="localhost", description="Database host")
    DB_PORT: int = Field(default=5432, description="Database port")
    DB_NAME: str = Field(default="appdb", description="Database name")
    DB_NAME_TEST: str = Field(default="appdb_test", description="Test database name")
    DATABASE_ECHO: bool = Field(default=False, description="Echo SQL queries")
    DB_SCHEMA: str = Field(default="analysis", description="Schema/DB_SCHEMA name")


    def get_database_url(self, async_driver: bool = True, use_test_db: bool = False) -> URL:
        """
        Build database URL from separate parameters.

        Args:
            async_driver: If True, uses asyncpg driver. If False, uses psycopg2.
            use_test_db: If True, uses test database name instead of main database.

        Returns:
            URL: SQLAlchemy URL object for database connection
        """
        driver = "postgresql+asyncpg" if async_driver else "postgresql+psycopg2"
        database = self.DB_NAME_TEST if use_test_db else self.DB_NAME

        return URL.create(
            drivername=driver,
            username=self.DB_USER,
            password=self.DB_PASSWORD,
            host=self.DB_HOST,
            port=self.DB_PORT,
            database=database
        )

# Global settings instance
settings = Settings()
