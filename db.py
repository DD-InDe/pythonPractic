import json
import sys


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
    def __init__(self, id, user, start, end):
        self.id = id
        self.user = user
        self.log_in = start
        self.log_out = end


users = []
services = []
logs = []

listtest = dict

database = read_info("db.json")


def upload_data(data=database):
    for item_user in data["user"]:
        user = User(id=item_user['id'], login=item_user['login'], password=item_user['password'],
                    first_name=item_user['first_name'],
                    last_name=item_user['last_name'], middle_name=item_user['middle_name'], gender=item_user['gender'],
                    role=item_user['role'], enabled=item_user['is_enabled'])
        users.append(user)
    for item_service in data["service"]:
        service = Service(id=item_service['id'], name=item_service['name'], cost=item_service['cost'])
        services.append(service)

    for item_log in data["log"]:
        for user in users:
            if user.id == item_log['user_id']:
                find_user = user
                continue
        log = Log(id=item_log['id'], user=find_user, start=item_log['time_log_in'], end=item_log['time_log_out'])
        logs.append(log)


def class_to_dict(obj):
    return obj.__dict__


def update_data():
    data = {'user': dict.fromkeys(users), 'service': dict.fromkeys(services), 'log': dict.fromkeys(logs)}
    with open("data_file.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4, default=class_to_dict, )
