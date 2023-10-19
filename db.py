import json
import sys
import datetime


def read_info(file_name):
    with open(file_name, 'r', encoding="utf-8") as file:
        return json.load(file)


class User:
    def __init__(self, id, login, password, first_name, last_name, middle_name, gender, role, enabled):
        self.id = id
        self.login = login
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.middle_name = middle_name
        self.gender = gender
        self.role = role
        self.is_enabled = enabled

    def get_fullname(self):
        return (f"{self.last_name} {self.first_name} {self.middle_name}")


class Service:
    def __init__(self, id, name, cost):
        self.id = id
        self.name = name
        self.cost = cost


class Log:
    def __init__(self, id, start, end):
        self.id = id
        self.time_log_in = start
        self.time_log_out = end

    def get_info(self):
        time_start = datetime.datetime.strptime(self.time_log_in, '%d/%m/%Y %H:%M:%S')
        time_end = datetime.datetime.strptime(self.time_log_out, '%d/%m/%Y %H:%M:%S')
        time_start = time_start.strftime('%d/%m/%Y %H:%M:%S')
        time_end = time_end.strftime('%d/%m/%Y %H:%M:%S')
        return f'{self.id}|{time_start}|{time_end}'

    def get_data(self):
        temp = self.time_log_in.split(' ')
        temp = temp[0].split('/')
        return f'{temp[1]}/{temp[0]}'

    def get_session_time(self):
        time_start = datetime.datetime.strptime(self.time_log_in, '%d/%m/%Y %H:%M:%S')
        time_end = datetime.datetime.strptime(self.time_log_out, '%d/%m/%Y %H:%M:%S')
        return time_end - time_start

class Check:
    def __init__(self, id, user, services):
        self.id = id
        self.user = user
        self.services = services

    def get_info(self):
        all_services = ''
        for service in self.services:
            all_services = f'{all_services},{service.id}'
        all_services = all_services.replace(',','',1)
        return f'{self.id}|{self.user.id}|{all_services}'

users = []
services = []
logs = []
checks = []

database = read_info("db.json")


def upload_data(data):
    users.clear()
    services.clear()
    logs.clear()

    for item_user in data["user"]:
        user = User(id=item_user['id'], login=item_user['login'], password=item_user['password'],
                    first_name=item_user['first_name'],
                    last_name=item_user['last_name'], middle_name=item_user['middle_name'], gender=item_user['gender'],
                    role=item_user['role'], enabled=item_user['is_enabled'])
        users.append(user)
    for item_service in data["service"]:
        service = Service(id=item_service['id'], name=item_service['name'], cost=item_service['cost'])
        services.append(service)

    logs_file = open('logs.txt', 'r')
    for line in logs_file:
        log = Log(line.split('|')[0], line.split('|')[1], line.split('|')[2].replace('\n', ''))
        logs.append(log)


def users_get_dict():
    users_dict = []
    for user in users:
        users_dict.append(user.__dict__)
    return users_dict


def service_get_dict():
    services_dict = []
    for service in services:
        services_dict.append(service.__dict__)
    return services_dict


def get_dict(obj):
    return obj.__dict__


def update_data():
    data = {'user': users_get_dict(), 'service': service_get_dict()}
    with open("db.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4, default=get_dict)
    write_file = open("logs.txt","w")
    for log in logs:
        write_file.write(log.get_info() + '\n')
    write_file.close()

'''
Новая БД создается в новом файле!
Исправить на исходник
'''

upload_data(database)