import db
import sys
from prettytable import PrettyTable
from operator import attrgetter
import create_log


def update_checks():
    write_file = open("checks.txt", 'w')
    for check in db.checks:
        write_file.write(check.get_info() + '\n')
    write_file.close()


def load_checks():
    checks_file = open('checks.txt', 'r')
    for line in checks_file:
        temp = line.split('|')
        check_id = temp[0]
        for user in db.users:
            if user.id == int(temp[1]):
                check_user = user
        check_service = []
        list_services = temp[2].split(',')
        for serv in list_services:
            for service in db.services:
                if service.id == int(serv):
                    check_service.append(service)
        check = db.Check(id=check_id, user=check_user, services=check_service)
        db.checks.append(check)


def check_managment():
    def view_services():
        service_table = PrettyTable()
        service_table.field_names = ["id", "Название", "Стоимость"]
        for service in db.services:
            service_table.add_row([service.id, service.name, service.cost])
        print(service_table)

    def create_checks():
        view_services()

        all_services = []
        check_user = create_log.logged_user

        def new_dialog():
            def check_service():
                for service in db.services:
                    if service.id == id_service:
                        return True
                print("Услуга с таким id не существует!")
                return False

            def get_service():
                for service in db.services:
                    if service.id == id_service:
                        return service

            check_id = db.checks[len(db.checks) - 1].id
            print("Добавить услугу?\n"
                  "1 - Да\n"
                  "2 - Нет\n")
            answer = input()
            if answer == '1':
                service_valid = False
                while not service_valid:
                    id_service = int(input("Введите id услуги, которую хотите добавить:"))
                    service_valid = check_service()
                service = get_service()
                all_services.append(service)
                new_dialog()
            if answer == '2':
                check_services = []
                [check_services.append(x) for x in all_services if x not in check_services]
                new_check = db.Check(check_id, check_user, check_services)
                db.checks.append(new_check)
                update_checks()

        new_dialog()

    def view_checks():
        check_table = PrettyTable()
        check_table.field_names = ["id", "ФИО сотрудника", "Услуги"]
        for check in db.checks:
            all_services = ''
            for service in check.services:
                all_services = f'{all_services}, {service.name}'
            all_services = all_services.replace(',','',1)
            check_table.add_row([check.id, check.user.get_fullname(), all_services])
        print(check_table)

    print("\tУправление чеками\n")

    def dialog():
        print("1 - Просмотреть чеки\n"
              "2 - Создать чек\n"
              "0 - Выйти")
        result = input()
        if result == '1':
            view_checks()
            dialog()
        elif result == '2':
            create_checks()
            dialog()
        elif result == '0':
            return
        else:
            dialog()

    dialog()

# def doc_create():



# блок меню пользователя
def user_menu():
    load_checks()
    print("\tМеню пользователя\n")

    def dialog():
        print("1 - Управление чеками\n"
              "2 - Создать документ\n"
              "0 - Выйти")
        result = input()
        if result == '1':
            check_managment()
            dialog()
        elif result == '0':
            return
        else:
            dialog()

    dialog()
