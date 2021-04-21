from pathlib import Path
import sys
import click
import importlib
import runpy

from flask.cli import AppGroup

from . import db
from .constants import SCRIPTS_DIR

cli = AppGroup('cli')


@cli.command(name='create_tables')
def create_tables():
    db.create_all()


@cli.command(name='drop_tables')
def drop_tables():
    print('You are about to drop all tables from your database')

    response = input('Are you sure? (y/n): ')
    if response == 'Y' or 'y' or 'Yes' or 'yes':
        print('Dropping all tables...')
        db.drop_all()

        return

    print('Did not drop all tables')

    return


@cli.command(name='run_script')
@click.argument('script', nargs=1)
def run_script(script: str):
    script_name = script
    if not script_name.endswith('.py'):
        script_name += '.py'

    script_path = SCRIPTS_DIR / script_name
    if not script_path.exists():
        print('Script could not be located')

        return

    runpy.run_path(script_path)
