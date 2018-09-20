from project.api.people import PersonModel, \
                                PersonSchema


def empty_database():
    PersonModel.objects().delete()


def create_test_user(username="tb",
                     firstname="ted",
                     lastname="bear",
                     address="23 blodstaf",
                     password="greaterthaneight"):
        personSchema = PersonSchema()
        p, errors = personSchema.load({"username": username,
                                       "firstname": firstname,
                                       "lastname": lastname,
                                       "employeenumber": "1",
                                       "address": address,
                                       "password": password})
        p.save()
        return p


def create_test_users():
    create_test_user(username='tb')
    create_test_user(username='bh')
