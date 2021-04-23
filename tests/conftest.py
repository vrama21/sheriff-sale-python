import os
import tempfile

import pytest

from app import create_app, db


@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    # create a temporary file to isolate the database for each test
    db_fd, db_path = tempfile.mkstemp()
    # create the app with common test config
    app = create_app()
    app.config['TESTING'] = True
    app.config['DATABASE'] = db_path

    # create the database and load test data
    # with app.app_context():
    #     print(app.config)

    yield app

    # close and remove the temporary database
    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """A test runner for the app's Click commands."""
    return app.test_cli_runner()


class AuthActions(object):
    def __init__(self, client):
        self._client = client


@pytest.fixture
def auth(client):
    return AuthActions(client)
