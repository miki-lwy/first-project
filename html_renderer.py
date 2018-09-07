import person_database
from mako.template import Template


def render_person_details(writer, person):
    my_template = Template(filename="template/user_details.txt")
    person_details_output = my_template.render(nickname=person.nickname, gender=person.gender, name=person.name)
    writer.write(bytes(person_details_output, 'UTF-8'))


def render_person_form(writer):
    my_template = Template(filename="template/person_form.txt")
    form_output = my_template.render()
    writer.write(bytes(form_output, 'UTF-8'))


import unittest


class MockWriter:
    def __init__(self):
        self.content = bytes('', 'UTF-8')

    def write(self, content):
        self.content += content


class TestHTMLRenderer(unittest.TestCase):

    def test_render_person_details(self):
        writer = MockWriter()
        person = person_database.Person("nickname", "gender", "name")
        render_person_details(writer, person)
        self.assertEqual(bytes("<h1> nickname's details: </h1>\n<dl><dt>gender: </dt> <dd>female</dd>\n<dt>Name: "
                               "</dt> <dd>name</dd></dl>", 'UTF-8'), writer.content)

    def test_render_person_form(self):
        writer = MockWriter()
        render_person_form(writer)
        self.assertEqual("<form  action=\"/friends\" method=\"post\">\n<p> Nickname </p>\n<input type=\"text\" "
                         "name=\"nickname\" value=\"\">\n<p> Name </p>\n<input type=\"text\" name=\"name\" "
                         "value=\"\">\n<p> "
                         "Gender</p>\n<input type=\"text\" name=\"gender\" value=\"\">\n<input type=\"submit\" "
                         "value=\"Submit\">\n</form>", writer.content.decode("utf-8"))
