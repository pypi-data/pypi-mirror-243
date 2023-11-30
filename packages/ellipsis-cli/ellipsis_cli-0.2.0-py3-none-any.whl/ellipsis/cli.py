import os
from subprocess import Popen
import logging
from typing import Optional
import requests

import click
import uvicorn

from ellipsis.ellipsis_api_client import EllipsisApiClient
from ellipsis.src.listener.cloud_dev_env_listener import CloudDevEnvListener
from ellipsis.src.models.workspaces.constants import HEALTH_CHECK_URL_ROUTE, LISTENER_PORT


CLI_VERSION = '0.2.0'

def create_listener_and_run(repo_dir: str, auth_token: Optional[str] = None):
    try:
        listener = CloudDevEnvListener(repo_dir, auth_token=auth_token)
        app = listener.create_fastapi_app()
        print(f"Listener started on port {LISTENER_PORT}")
        uvicorn.run(app, port=LISTENER_PORT, log_level="debug")
    except Exception as e:
        logging.error("Error starting the listener: %s", str(e))
        print(e)

@click.group()
def cli():
    pass

@cli.command()
def version():
    click.echo(f"Version {CLI_VERSION}")

@cli.command()
def ping():
    bb_client = EllipsisApiClient(os.environ.get('ELLIPSIS_API_URL', None))
    click.echo(f'Pinging {bb_client.base_url}...')
    click.echo("pong")

@click.group()
def listener():
    pass

@listener.command()
@click.argument('repo_dir')
def start(repo_dir: str):
    bb_client = EllipsisApiClient(os.environ.get('ELLIPSIS_API_URL', None))
    repo_name_split = os.environ['GITHUB_REPOSITORY'].split('/')
    assert len(repo_name_split) == 2, f'Invalid repository name: {os.environ["GITHUB_REPOSITORY"]}'
    bb_client.register_codespace(
        os.environ['CODESPACE_NAME'],
        repo_name_split[0],
        repo_name_split[1],
        os.environ['GITHUB_TOKEN'],
        os.environ['GITHUB_USER']
    )
    try:
        response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
        if response.status_code == 200:
            click.echo("Listener already running.")
            return
    except requests.exceptions.ConnectionError:
        pass
    background_process = Popen(['python3', '/usr/local/python/3.10.8/lib/python3.10/site-packages/ellipsis/_listener.py', repo_dir])
    click.echo(f"Starting listener in background process with PID {background_process.pid}...")


@listener.command()
def stop():
    raise NotImplementedError(f'Not implemented for some archietctures.')
    # try:
    #     response = requests.get(f"http://localhost:{LISTENER_PORT}{HEALTH_CHECK_URL_ROUTE}")
    #     click.echo(response.json())
    #     if response.status_code != 200:
    #         click.echo("Listener not running, nothing to stop.")
    #         return
    # except requests.exceptions.ConnectionError:
    #     click.echo("Listener not running, nothing to stop.")
    #     return
    # response_json = response.json()
    # pid = response_json['pid']
    # Popen(['kill', str(pid)])
    # click.echo(f"Killed listener with PID {pid}.")

cli.add_command(ping)
cli.add_command(version)
cli.add_command(listener)

if __name__ == '__main__':
    cli()
