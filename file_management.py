import person_database


class FileManagement:

    def __init__(self, filename) -> None:
        self.filename = filename

    # read file
    def read_person_file(self):
        with open(self.filename, 'r', newline='') as filereader:
            header = filereader.readline()
            person_list = []
            for row in filereader:
                row = row.strip()
                row_list = row.split(',')
                new_person = person_database.Person(row_list[0], row_list[1], row_list[2])
                person_list.append(new_person)
            return person_list

    # write file
    def write_person_file(self, person_list):
        with open(self.filename, 'w') as filewriter:
            if person_list:
                filewriter.write('nickname,gender,name \n')
                for person in person_list:
                    filewriter.write(person.nickname + ',' + person.gender + ',' + person.name + '\n')
            else:
                filewriter.write("")


import unittest


class TestFileManagement(unittest.TestCase):

    def test_read_empty_file_returns_empty_list(self):
        file_management = FileManagement()
        person_list = file_management.read_person_file()
        self.assertEqual([], person_list)

    def test_read_person_file_returns_person_list(self):
        file_management = FileManagement()
        person_list = file_management.read_person_file()
        self.assertEqual(
            [
                person_database.Person("oba", "male", "Obama"),
                person_database.Person("twins", "female", "Twins")
            ],
            person_list
        )

    def test_write_empty_person_file(self):
        file_management = FileManagement()
        file_management.write_person_file([])
        person_list = file_management.read_person_file()
        self.assertEqual([], person_list)

    def test_write_person_file(self):
        file_management = FileManagement()
        write_person = [person_database.Person("oba", "male", "Obama"),
                        person_database.Person("twins", "female", "Twins")]
        file_management.write_person_file(write_person)
        person_list = file_management.read_person_file()
        self.assertEqual(write_person, person_list)
