import unittest

import coverage

COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/config.py',
    ]
)
COV.start()

from flask.cli import FlaskGroup

from project import create_app, db
from project.tests.utils import create_test_users, create_test_skills, empty_database, load_json_test_data

app = create_app()
cli = FlaskGroup(create_app=create_app)

@cli.command()
def test():
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1

@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

@cli.command()
def empty_db():
    empty_database()


@cli.command()
def seed_db():
    create_test_users()
    create_test_skills()

@cli.command()
def load_test_data():
    load_json_test_data()

if __name__ == '__main__':
    cli()