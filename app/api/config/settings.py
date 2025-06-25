import os

class Settings(object):

    LOG_LEVEL=os.environ.get("LOG_LEVEL") or "INFO"

    PSQL_PASS = os.environ.get("POSTGRES_PASSWORD") or "password"
    PSQL_USER = os.environ.get("POSTGRES_USER") or "user"
    PSQL_HOST = os.environ.get("POSTGRES_HOST") or "localhost"
    PSQL_PORT = os.environ.get("POSTGRES_PORT") or "5432"
    PSQL_DBNM = os.environ.get("POSTGRES_DB") or "petdb"
    DATABASE_URI = (
        f"postgresql://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DBNM}"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or DATABASE_URI
