import click
from click.decorators import command
from flask.cli import AppGroup, with_appcontext

from . import db

cli = AppGroup('cli')


@cli.command(name="create_tables")
def create_tables():
    db.create_all()


@cli.command(name="drop_tables")
def drop_tables():
    db.drop_all()