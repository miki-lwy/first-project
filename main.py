import http.server
import json
import urllib.request


class Person:
    def __init__(self, nickname, gender, name):
        self.nickname = nickname
        self.gender = gender
        self.name = name



fruit_database = [
    "banana",
    "apple",
    "pear"
]

person_database = []

# initialization
with open('example_file.csv', 'r', newline='') as filereader:
    header = filereader.readline()
    for row in filereader:
        row = row.strip()
        row_list = row.split(',')
        new_person = Person(row_list[0], row_list[1], row_list[2])
        person_database.append(new_person)





class MyHandlerForHTTP(http.server.BaseHTTPRequestHandler):
    def do_POST(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        parsed_body = urllib.request.unquote(post_body.decode("utf-8")).split('&')
        person_dict = {}
        for element in parsed_body:
            parsed_element = element.split('=')
            person_dict[parsed_element[0]] = parsed_element[1]
        new_person = Person(person_dict['nickname'], person_dict['gender'], person_dict['name'])
        person_database.append(new_person)
        with open('example_file.csv', 'w') as filewriter:
            filewriter.write('nickname,gender,name \n')
            for person in person_database:
                filewriter.write(person.nickname + ',' + person.gender + ',' + person.name + '\n')

    def do_PUT(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        content_len = int(self.headers.get('content-length', 0))
        put_body = self.rfile.read(content_len)
        json_body = json.loads(put_body)
        amend_person = Person(json_body['nickname'], json_body['gender'], json_body['name'])
        found = False
        for person in person_database:
            nickname_to_find = self.extract_nickname()
            if person.nickname == nickname_to_find:
                found = True
                person_database.remove(person)
                person_database.append(amend_person)
                with open('example_file.csv', 'w') as filewriter:
                    filewriter.write('nickname,gender,name \n')
                    for person in person_database:
                        filewriter.write(person.nickname + ',' + person.gender + ',' + person.name + '\n')

        if not found:
            self.wfile.write(bytes('<p> Cannot find this person </p>', 'UTF-8'))

    def extract_nickname(self):
        return self.path.replace('/friends/', '')

    def do_DELETE(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        found = False
        for person in person_database:
            nickname_to_find = self.extract_nickname()
            if person.nickname == nickname_to_find:
                found = True
                person_database.remove(person)
                with open('example_file.csv', 'w') as filewriter:
                    filewriter.write('nickname,gender,name \n')
                    for person in person_database:
                        filewriter.write(person.nickname + ',' + person.gender + ',' + person.name + '\n')

        if not found:
            self.wfile.write(bytes('<p> Cannot find this person </p>', 'UTF-8'))



    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(bytes('<!DOCTYPE html><html><head><style> \
        table, th, td \
        { \
            border: 1px solid black; \
        } \
        </style></head><body>', 'UTF-8'))

        if self.path == '/fruits':
            self.wfile.write(bytes('<h1> Here are your fruits: </h1>', 'UTF-8'))
            for fruit in fruit_database:
                self.wfile.write(bytes('<h1>name: </h1>' + fruit, 'UTF-8'))

        if self.path == '/friends':
            self.wfile.write(bytes('<h1> Here are your friends: </h1>', 'UTF-8'))
            self.wfile.write(bytes('<table style="width:100%">', 'UTF-8'))
            self.wfile.write(bytes('<tr> <th>Nickname</th> <th>Name</th> <th>Gender</th></tr>', 'UTF-8'))
            for person in person_database:
                self.wfile.write(bytes('<tr>'
                                       '<td>'
                                       '<a href="http://localhost:8088/friends/' + person.nickname + '">' + person.nickname + '</a>'
                                       '</td> '
                                       '<td>' + person.name + '</td>'
                                       '<td>' + person.gender + '</td>'
                                       '</tr>', 'UTF-8'))

            self.wfile.write(bytes('</table>', 'UTF-8'))
            self.wfile.write(bytes('<form  action="/friends" method="post">', 'UTF-8'))
            self.wfile.write(bytes('<p> Nickname </p>', 'UTF-8'))
            self.wfile.write(bytes('<input type="text" name="nickname" value="">', 'UTF-8'))
            self.wfile.write(bytes('<p> Name </p>', 'UTF-8'))
            self.wfile.write(bytes('<input type="text" name="name" value="">', 'UTF-8'))
            self.wfile.write(bytes('<p> Gender</p>', 'UTF-8'))
            self.wfile.write(bytes('<input type="text" name="gender" value="">', 'UTF-8'))
            self.wfile.write(bytes('<input type="submit" value="Submit">', 'UTF-8'))
            self.wfile.write(bytes('</form>', 'UTF-8'))


        if self.path.startswith('/friends/'):
            nickname_to_find = self.extract_nickname()
            found = False
            for person in person_database:
                if person.nickname == nickname_to_find:
                    found = True
                    self.wfile.write(bytes('<h1> ' + person.nickname + '\'s details: </h1>', 'UTF-8'))
                    self.wfile.write(bytes('<dl><dt>Gender: </dt> <dd>' + person.gender + '</dd>', 'UTF-8'))
                    self.wfile.write(bytes('<dt>Name: </dt> <dd>' + person.name + '</dd></dl>', 'UTF-8'))
            if not found:
                self.wfile.write(bytes('<p> I don\'t know this person </p>', 'UTF-8'))

        self.wfile.write(bytes('</body></html>', 'UTF-8'))


httpd = http.server.HTTPServer(('127.0.0.1', 8088), MyHandlerForHTTP)
httpd.serve_forever()
