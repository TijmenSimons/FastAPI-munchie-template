"""
Boot up the application with extra settings

Usage:
    python main.py

Options:
    --env : ["local", "dev", "prod"]
    --debug : bool
"""

import os

import click
import uvicorn

from core.config import config


@click.command()
@click.option(
    "--env",
    type=click.Choice(["local", "dev", "prod"], case_sensitive=False),
    default="local",
)
@click.option(
    "--debug",
    type=click.BOOL,
    is_flag=True,
    default=False,
)
def main(env: str = None, debug: bool = None):
    """
    Boot up the application.

    Args:
        env (str): The environment to run the application in, can be one of "local", "dev", or "prod".
        debug (bool): Whether or not to run the application in debug mode.

    Returns:
        None
    """
    os.environ["ENV"] = env
    os.environ["DEBUG"] = str(debug)
    uvicorn.run(
        app="app.server:app",
        host=config.APP_HOST,
        port=config.APP_PORT,
        reload=config.ENV != "production",
        workers=1,
    )


if __name__ == "__main__":
    main()
