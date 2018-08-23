class PersonDatabase:
    def __init__(self):
        self.list = []

    def create(self, person):
        if self.find(person.nickname) is None:
            self.list.append(person)
            return True
        return False

    def delete(self, nickname):
        found = self.find(nickname)
        if found is not None:
            self.list.remove(found)

    def find(self, nickname):
        for element in self.list:
            if nickname == element.nickname:
                return element
        return None

    def update(self, updated_person):
        self.delete(updated_person.nickname)
        self.create(updated_person)


class Person:
    def __eq__(self, o: object) -> bool:
        if isinstance(o, Person):
            return self.nickname == o.nickname and self.name == o.name and self.gender == o.gender
        return NotImplemented

    def __init__(self, nickname, gender, name):
        self.nickname = nickname
        self.gender = gender
        self.name = name

    def __repr__(self):
        return self.nickname + " " + self.name + " " + self.gender



import unittest


class TestPersonDatabase(unittest.TestCase):

    def test_find_empty_database_returns_None(self):
        database = PersonDatabase()
        find_person = database.find("miki")
        self.assertEqual(None, find_person)

    def test_find_with_existing_person_returns_person(self):
        database = PersonDatabase()
        person = Person("miki", "female", "leung wing yan")
        database.create(person)
        find_person = database.find("miki")
        self.assertEqual(person, find_person)

    def test_delete_existing_person(self):
        database = PersonDatabase()
        person = Person("miki", "female", "leung wing yan")
        database.create(person)
        database.delete("miki")

        find_person = database.find("miki")
        self.assertEqual(None, find_person)

    def test_successful_create_return_true(self):
        database = PersonDatabase()
        person = Person("miki", "female", "leung wing yan")
        creation_status = database.create(person)
        self.assertEqual(True, creation_status)

    def test_fail_create_return_false(self):
        database = PersonDatabase()
        person = Person("miki", "female", "leung wing yan")
        creation_status = database.create(person)
        creation_status = database.create(person)
        self.assertEqual(False, creation_status)

    def test_update_existing_person(self):
        database = PersonDatabase()
        person = Person("miki", "female", "leung wing yan")
        database.create(person)
        updated_person = Person("miki", "male", "leung wing yan")
        database.update(updated_person)
        find_person = database.find("miki")
        self.assertEqual(updated_person, find_person)

    def test_update_non_existing_person_create_person(self):
        database = PersonDatabase()
        updated_person = Person("miki", "male", "leung wing yan")
        database.update(updated_person)
        find_person = database.find("miki")
        self.assertEqual(updated_person, find_person)
