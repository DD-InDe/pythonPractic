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

    def return_class(self):
        log = Log(id=self.id, user=self.user.id, start=self.log_in, end=self.log_out)
        return log


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

def log_get_dict():
    logs_dict = []
    for log in logs:
        logs_dict.append(log.return_class().__dict__)
    return logs_dict

def get_dict(obj):
    return obj.__dict__

def update_data():
    data = {'user': users_get_dict(), 'service': service_get_dict(), 'log': log_get_dict()}
    with open("data_file.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4, default=get_dict)
