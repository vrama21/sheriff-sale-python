from flask.cli import AppGroup

from . import db

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
