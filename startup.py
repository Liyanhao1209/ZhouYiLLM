import uvicorn

from component.DB_engine import init_db_conn
from config.server_config import *
from routers import mount_routers
from component.email_server import init_email_server


def init_web_service():
    init_db()
    run_api_server()


def run_api_server():
    init_email_server()
    app = mount_routers.create_app()

    host = WEB_SERVER['host']
    port = WEB_SERVER['port']

    uvicorn.run(app, host=host, port=port)


def init_db():
    init_db_conn()


if __name__ == '__main__':
    init_web_service()
