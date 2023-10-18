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
        return f'{self.id}|,{self.time_log_in}|,{self.time_log_in}'

    def get_item(self, data):
        if f'{self.time_log_in:%m/%d}' == data:
            return self


users = []
services = []
logs = []

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

    # logs_file = open('logs.txt', 'r')
    # for line in logs_file:
    #     log = Log(line.split('|')[0], line.split('|')[1], line.split('|')[2])
    #     logs.append(log)


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
    with open("data_file.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, default=get_dict)

    # new_file = open('logs1.txt', 'w')
    # for log in logs:
    #     new_file.write(f'{log.get_info()}\n')
    # new_file.close()


'''
Новая БД создается в новом файле!
Исправить на исходник
'''
