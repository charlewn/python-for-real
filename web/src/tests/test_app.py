import os
import sys
import pytest

"""Initialize the testing environment

Creates an app for testing that has the configuration flag ``TESTING`` set to
``True``.

"""

PACKAGE_PARENT = '../'

SCRIPT_DIR = os.path.dirname(os.path.realpath(os.path.join(os.getcwd(), os.path.expanduser(__file__))))
# print(os.path.join(SCRIPT_DIR, PACKAGE_PARENT))
sys.path.append(os.path.normpath(os.path.join(SCRIPT_DIR, PACKAGE_PARENT)))

# from core import app


@pytest.fixture
def client():
    """Configures the app for testing

    Sets app config variable ``TESTING`` to ``True``

    :return: App for testing
    """

    #app.config['TESTING'] = True
    client = app.test_client()

    yield client

@pytest.fixture()
def client(app):
    return app.test_client()

landing = client.get("/")
html = landing.data.decode()
print(html)