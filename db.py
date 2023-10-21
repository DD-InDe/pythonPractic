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
    def __init__(self, id, user, address, date, check_sum, check_services):
        self.id = id
        self.user = user
        self.address = address
        self.date = date
        self.services = check_services
        self.sum = check_sum

    def get_info(self):
        all_services = ''
        for service in self.services:
            all_services = f'{all_services},{service.id}'
        all_services = all_services.replace(',', '', 1)
        return f'{self.id}|{self.user.id}|{self.address}|{self.date}|{self.sum}|{all_services}'


users = []
services = []
logs = []
checks = []

database = read_info("db.json")


def upload_data(data):
    users.clear()
    services.clear()
    logs.clear()
    checks.clear()

    # загрузка пользователей
    for item_user in data["user"]:
        user = User(id=item_user['id'], login=item_user['login'], password=item_user['password'],
                    first_name=item_user['first_name'],
                    last_name=item_user['last_name'], middle_name=item_user['middle_name'], gender=item_user['gender'],
                    role=item_user['role'], enabled=item_user['is_enabled'])
        users.append(user)
    # загрузка услуг
    for item_service in data["service"]:
        service = Service(id=item_service['id'], name=item_service['name'], cost=item_service['cost'])
        services.append(service)
    # загрузка логов
    logs_file = open('logs.txt', 'r')
    for line in logs_file:
        log = Log(line.split('|')[0], line.split('|')[1], line.split('|')[2].replace('\n', ''))
        logs.append(log)
    logs_file.close()
    # загрузка чеков
    checks_file = open('checks.txt', 'r', encoding="utf-8")
    for line in checks_file:
        temp = line.split('|')
        check_id = temp[0]
        for user in users:
            if user.id == int(temp[1]):
                check_user = user
        check_service = []
        check_address = temp[2]
        check_date = temp[3]
        check_sum = temp[4]
        list_services = temp[5].split(',')
        for serv in list_services:
            for service in services:
                if service.id == int(serv):
                    check_service.append(service)
        check = Check(id=check_id, user=check_user, address=check_address, date=check_date, check_sum=check_sum,
                      check_services=check_service)
        checks.append(check)
    checks_file.close()


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
    # сохранение пользователей и услуг
    data = {'user': users_get_dict(), 'service': service_get_dict()}
    with open("db.json", "w", encoding="utf-8") as write_file:
        json.dump(data, write_file, ensure_ascii=False, indent=4, default=get_dict)
    # сохранение логов
    log_file = open("logs.txt", "w")
    for log in logs:
        log_file.write(log.get_info() + '\n')
    log_file.close()
    # сохранение чеков
    check_file = open("checks.txt", 'w', encoding="utf-8")
    for check in checks:
        check_file.write(check.get_info() + '\n')
    check_file.close()
