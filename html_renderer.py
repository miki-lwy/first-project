import person_database
from mako.template import Template


def render_person_details(writer, person):
    my_template = Template(filename="template/user_details.txt")
    person_details_output = my_template.render(nickname=person.nickname, gender=person.gender, name=person.name)
    writer.write(bytes(person_details_output, 'UTF-8'))


import unittest


class MockWriter:
    def __init__(self):
        self.content = ''

    def write(self, content):
        self.content = content


class TestHTMLRenderer(unittest.TestCase):

    def test_render_person_details(self):
        writer = MockWriter()
        person = person_database.Person("nickname", "gender", "name")
        render_person_details(writer, person)
        self.assertEqual(bytes("<h1> nickname's details: </h1>\n<dl><dt>gender: </dt> <dd>female</dd>\n<dt>Name: "
                               "</dt> <dd>name</dd></dl>", 'UTF-8'), writer.content)
