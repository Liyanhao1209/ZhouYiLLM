import uvicorn

from config.server_config import *
from routers import mount_routers


def run_api_server():
    app = mount_routers.create_app()

    host = WEB_SERVER['host']
    port = WEB_SERVER['port']

    uvicorn.run(app, host=host, port=port)


if __name__ == '__main__':
    run_api_server()
