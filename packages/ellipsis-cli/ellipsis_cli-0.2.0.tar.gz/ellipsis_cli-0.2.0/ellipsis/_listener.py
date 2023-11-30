import click

import uvicorn

from ellipsis.src.listener.cloud_dev_env_listener import CloudDevEnvListener
from ellipsis.src.models.workspaces.constants import LISTENER_PORT

@click.command()
@click.argument('directory')
def main(directory: str):
    listener = CloudDevEnvListener(directory, auth_token=None)
    app = listener.create_fastapi_app()
    uvicorn.run(app, port=LISTENER_PORT, log_level="debug")

if __name__ == '__main__':
    main()
