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
from project.api.people import People, Person, PersonSchema, PersonModel


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
def empty_database():
    PersonModel.objects().delete()


@cli.command()
def create_test_users():
        peopleSchema = PersonSchema(many=True)
        p, errors = peopleSchema.load([{"firstname": "ted",
                                        "lastname": "bear",
                                        "employeenumber": "1",
                                        "address": "23 blodsfsdf"},
                                       {"firstname": "bob",
                                        "lastname": "holmes",
                                        "employeenumber": "2",
                                        "address": "77 verulam road"}])
        PersonModel.objects.insert(p)
        return p

if __name__ == '__main__':
    cli()