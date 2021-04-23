from pathlib import Path
import click
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

    acceptable_responses = ['Y', 'y', 'Yes', 'yes']
    if response in acceptable_responses:
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

    print(f'You are about to run script: {script_name}...')

    response = input('Are you sure? (y/n): ')

    acceptable_responses = ['Y', 'y', 'Yes', 'yes']
    if response in acceptable_responses:
        print(f'Running script: {script_name}...')
        runpy.run_path(script_path)

        print(f'{script_name} has completed.')

        return

    print(f'Did not run script: {script_name}')

    return
