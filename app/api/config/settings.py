import os
import httpx

class Settings(object):

    LOG_LEVEL=os.environ.get("LOG_LEVEL") or "INFO"
    PSQL_PASS = os.environ.get("POSTGRES_PASSWORD") or "password"
    PSQL_USER = os.environ.get("POSTGRES_USER") or "user"
    PSQL_PORT = os.environ.get("POSTGRES_PORT") or "5432"
    PSQL_DBNM = os.environ.get("POSTGRES_DB") or "petdb"
    PSQL_HOST = os.environ.get("POSTGRES_HOST")
    PSQL_SERVICE_CONSUL = "db-server"


    if not PSQL_HOST:
        try:
            consul_url = "http://localhost:8500/v1/catalog/service/{}".format(PSQL_SERVICE_CONSUL)
            response = httpx.get(consul_url, timeout=5)
            if response.status_code == 200:
                services = response.json()
                if services:
                    PSQL_HOST = services[0].get('ServiceAddress') or services[0].get('Address')
                    print(f"Discovered PostgreSQL host via Consul: {PSQL_HOST}")
        except Exception as e:
            print(f"Failed to discover PostgreSQL via Consul: {e}")
            PSQL_HOST = "localhost"


    DATABASE_URI = (
        f"postgresql://{PSQL_USER}:{PSQL_PASS}@{PSQL_HOST}:{PSQL_PORT}/{PSQL_DBNM}"
    )

    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URI") or DATABASE_URI
