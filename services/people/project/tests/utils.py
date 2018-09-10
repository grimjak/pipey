from project.api.people import PersonModel, \
                                PersonSchema

def empty_database():
    PersonModel.objects().delete()


def create_test_user():
        personSchema = PersonSchema()
        p, errors = personSchema.load({"username": "tb",
                                       "firstname": "ted",
                                       "lastname": "bear",
                                       "employeenumber": "1",
                                       "address": "23 blodsfsdf"})
        p.save()
        return p


def create_test_users():
        peopleSchema = PersonSchema(many=True)
        p, errors = peopleSchema.load([{"username": "tb",
                                        "firstname": "ted",
                                        "lastname": "bear",
                                        "employeenumber": "1",
                                        "address": "23 blodsfsdf"},
                                       {"username": "tb",
                                        "firstname": "bob",
                                        "lastname": "holmes",
                                        "employeenumber": "2",
                                        "address": "77 verulam road"}])
        PersonModel.objects.insert(p)
        return p
