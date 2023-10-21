import calendar
import datetime
import matplotlib.pyplot as plt
import numpy as np
import json
from tkinter import filedialog
import create_log
import db
from petrovich.main import Petrovich
from petrovich.enums import Case, Gender
from prettytable import PrettyTable
from operator import attrgetter


# блок управления пользователями (CRUD)
def user_managment():
    # вывод таблицы
    def users_print(users_list):
        user_table = PrettyTable()
        user_table.field_names = ["id", "Фамилия", "Имя", "Отчество", "Пол", "Роль", "Статус"]
        for user in users_list:
            user_table.add_row(
                [user.id, user.last_name, user.first_name, user.middle_name, user.gender, user.role,
                 user.is_enabled])
        print(user_table)

    # задание фильтра для вывода пользовавтелей
    def users_view():
        # выбор варианта сортировки
        def select_sort(list):
            print("Выберите вариант сортировки\n"
                  "[1] - Вывести А-Я\n"
                  "[2] - Вывести Я-А\n"
                  "[3] - Вывести по возрастанию\n"
                  "[4] - Вывести по уменьшению")

            sort_result = input()
            if sort_result == '1':
                list.sort(key=attrgetter('last_name'), reverse=False)
                return list
            elif sort_result == '2':
                list.sort(key=attrgetter('last_name'), reverse=True)
                return list
            elif sort_result == '3':
                return list
            elif sort_result == '4':
                list.reverse()
                return list
            else:
                select_sort(list)

        print("\tПросмотр пользователей\n"
              "Выберите вариант вывода\n"
              "[1] - Вывести всех пользователей\n"
              "[2] - Вывести активных пользователей\n"
              "[3] - Вывести неактивных пользователей\n"
              "[4] - Вывести Мужчин\n"
              "[5] - Вывести Женщин\n"
              "[0] - Назад")

        result = input()
        temp = db.users.copy()

        if result == '1':
            temp = temp
        elif result == '2':
            temp = [user for user in filter(lambda user: user.is_enabled == True, temp)]
        elif result == '3':
            temp = [user for user in filter(lambda user: user.is_enabled == True, temp)]
        elif result == '4':
            temp = [user for user in filter(lambda user: user.gender == "муж", temp)]
        elif result == '5':
            temp = [user for user in filter(lambda user: user.gender == "жен", temp)]
        elif result == '0':
            return
        else:
            dialog()

        temp = select_sort(temp)
        users_print(temp)

    # создание пользователя
    def user_add():
        def user_create():
            # проверка логина на повторение
            def check_login(login):
                for user in db.users:
                    if user.login == login:
                        print("Пользователь с таким логином уже есть! Придумайте другой")
                        return False
                return True

            login_not_free = True
            user_first_name = input("Введите имя:").replace(' ', '')
            user_last_name = input("Введите фамилия:").replace(' ', '')
            user_middle_name = input("Введите отчество:").replace(' ', '')
            user_role = input("Введите роль (admin/user):").replace(' ', '')
            user_gender = input("Введите пол (муж/жен):").replace(' ', '')
            while login_not_free:
                user_login = input("Введите логин:").replace(' ', '')
                login_not_free = not check_login(user_login)
            user_password = input("Введите пароль:").replace(' ', '')

            new_user = db.User(id=db.users[len(db.users) - 1].id + 1, login=user_login, password=user_password,
                               first_name=user_first_name, last_name=user_last_name, middle_name=user_middle_name,
                               gender=user_gender, role=user_role, enabled=True)
            db.users.append(new_user)
            db.update_data()
            print("Пользователь добавлен!")
            return

        def user_import():
            def read_info(file_name):
                with open(file_name, 'r', encoding="utf-8") as file:
                    return json.load(file)

            filename = filedialog.askopenfilename(filetypes=[('Json files', '*.json')])
            try:
                def check_user():
                    for user in db.users:
                        if item_user['login'] == user.login:
                            full_name = item_user['last_name'] + " " + item_user['first_name'] + " " + item_user[
                                'middle_name']
                            error_users.append(full_name)
                            return False
                    return True

                database = read_info(filename)
                error_users = []
                count = 0
                for item_user in database["user"]:
                    if check_user() == True:
                        id = int(db.users[len(db.users) - 1].id) + 1
                        user = db.User(id=id, login=item_user['login'], password=item_user['password'],
                                       first_name=item_user['first_name'],
                                       last_name=item_user['last_name'], middle_name=item_user['middle_name'],
                                       gender=item_user['gender'],
                                       role=item_user['role'], enabled=True)
                        db.users.append(user)
                        count += 1

                print(f"Пользовавтелей добавлено: {count}")
                if len(error_users) != 0:
                    print(f"Пользователей не добавлено: {len(error_users)}")
                    for user in error_users:
                        print(user)
                # db.update_data()
            except Exception as exeption:
                print(exeption)

        def dialog():
            print("\tДобавление пользователя\n"
                  "[1] - Добавить пользователя вручную\n"
                  "[2] - Добавить пользовател(-я/-ей) из файла\n"
                  "[0] - Назад")
            result = input()
            if result == '1':
                user_create()
                dialog()
            elif result == '2':
                user_import()
                dialog()
            elif result == '0':
                return
            else:
                dialog()

        dialog()

    # удаление пользователя
    def user_delete():
        print("\tУдаление пользователя\n"
              "Таблица пользователей\n")
        users_print(db.users)

        def find_user():
            for user in db.users:
                if user.id == int(user_id):
                    return user

        def check_users():
            for user in db.users:
                temp = str(user.id)
                if temp == user_id:
                    return True
            print("Пользователь с таким id не существует!")
            return False

        is_user_exist = False
        while not is_user_exist:
            user_id = input("0 - Перейти назад\n"
                            "Введите id пользователя, которого хотите удалить: ")
            if user_id == '0':
                return
            is_user_exist = check_users()
        user = find_user()
        if user == create_log.logged_user:
            print("Нельзя удалить свой профиль!")
            user_delete()
        if user.role == "admin":
            print("Нельзя удалить администратора!")
            user_delete()
        db.users.remove(user)
        db.update_data()
        db.upload_data(db.database)
        user_delete()

    # редактирование пользователя
    def user_edit():
        def find_user():
            for user in db.users:
                if user.id == int(user_id):
                    return user

        def check_users():
            for user in db.users:
                temp = str(user.id)
                if temp == user_id:
                    return True
            print("Пользователь с таким id не существует!")
            return False

        def check_login(login, id):
            for user in db.users:
                if user.login == login and user.id != id:
                    print("Пользователь с таким логином уже есть! Придумайте другой")
                    return False
            return True

        users_print(db.users)
        is_user_exist = False
        while not is_user_exist:
            user_id = input("Введите id пользователя, профиль которого хотите изменить: ")
            is_user_exist = check_users()
        edit_user = find_user()

        print("Данные пользователя")
        print(f'Фамилия: {edit_user.last_name}')
        print(f'Имя: {edit_user.first_name}')
        print(f'Отчество: {edit_user.middle_name}')
        print(f'Роль: {edit_user.role}')
        print(f'Пол: {edit_user.gender}')
        print(f'Логин: {edit_user.login}')
        print(f'Пароль: {edit_user.password}')
        print(f'Статус: {edit_user.is_enabled}')

        login_free = False
        print("Режим изменения")
        edit_user.last_name = input(f"Введите фамилия ({edit_user.last_name}):").replace(' ', '')
        edit_user.first_name = input(f"Введите имя ({edit_user.first_name}):").replace(' ', '')
        edit_user.middle_name = input(f"Введите отчество ({edit_user.middle_name}):").replace(' ', '')
        edit_user.role = input(f"Введите роль (admin/user) ({edit_user.role}):").replace(' ', '')
        edit_user.gender = input(f"Введите пол (муж/жен) ({edit_user.gender}):").replace(' ', '')
        while not login_free:
            edit_user.login = input(f"Введите логин: ({edit_user.login}):").replace(' ', '')
            login_free = check_login(edit_user.login, edit_user.id)
        edit_user.password = input(f"Введите пароль ({edit_user.password}):").replace(' ', '')
        db.update_data()
        edit_user.is_enabled = input(f"Статус ({edit_user.is_enabled}):")
        print("Изменения сохранены!")
        return

    def dialog():
        print("\tУправление пользователями\n"
              "[1] - Вывести пользователей\n"
              "[2] - Добавить пользователя\n"
              "[3] - Удалить пользователя\n"
              "[4] - Редактировать пользователя\n"
              "[0] - Назад")
        result = input()

        if result == '1':
            users_view()
            dialog()
        elif result == '2':
            user_add()
            dialog()
        elif result == '3':
            user_delete()
            dialog()
        elif result == '4':
            user_edit()
            dialog()
        elif result == '0':
            return
        else:
            dialog()

    dialog()


# блок создания графиков
def create_graph():
    def all_users_graph():

        def get_dates(var):

            def dialog():
                month = int(input("Введите номер месяца:"))
                if month < 0 or month >= 13:
                    dialog()
                return month

            dates = []
            # 1 - месяц
            if var == 1:
                month = dialog()
                not_finished = False
                last_day = calendar.monthrange(datetime.date.today().year, month)[1]
                day = 1
                while not not_finished:
                    date = datetime.datetime(year=datetime.date.today().year, month=month, day=day)
                    dates.append(date.strftime('%d'))
                    if day == last_day:
                        not_finished = True
                    day += 1
                return dates
            # 2 - неделя
            if var == 2:
                num = 0
                while num < 7:
                    day = f'{datetime.datetime.now().day - datetime.datetime.now().weekday() + num}'
                    dates.append(day)
                    num += 1
                return dates

        def dialog():
            print("Выберите диапозон дат:\n"
                  "[1] - Месяц\n"
                  "[2] - Текущая неделя\n"
                  "[0] - Назад")

            var = input()
            if var == '0':
                return int(var)
            elif var == '1':
                return int(var)
            elif var == '2':
                return int(var)
            else:
                dialog()

        temp_users = []

        var = dialog()
        if var == 0:
            return
        if var == 2:
            title = 'Работа пользователей за текущую неделю'
        else:
            title = 'Работа пользователей за выбранный месяц'

        dates = get_dates(var)
        new_logs = []
        for log in db.logs:
            for day in dates:
                if str(log.get_data()) == str('10/' + day):
                    new_logs.append(log)
                    for user in db.users:
                        if str(user.id) == log.id:
                            temp_users.append(user)

        current_users = []
        [current_users.append(x) for x in temp_users if x not in current_users]
        g_list = []
        for user in current_users:
            g = []
            for day in dates:
                count = 0
                for log in new_logs:
                    if str(log.get_data()) == str('10/' + day):
                        if log.id == str(user.id):
                            count += 1
                g.append(count)
            g_list.append(g)

        width = 0.1
        x = np.arange(len(dates))
        fig, ax = plt.subplots()
        number = 1
        while number < len(current_users):
            if number < (len(current_users) / 2):
                rects = ax.bar(x - width * number, g_list[number - 1], width, label=current_users[number - 1].last_name)
            else:
                rects = ax.bar(x + width * (number - len(current_users) / 2), g_list[number - 1], width,
                               label=current_users[number - 1].last_name)
            number += 1

        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(dates)
        ax.legend()

        plt.show()

    def current_user_graph(user):
        def get_dates(var):

            def dialog():
                month = int(input("Введите номер месяца:"))
                if month < 0 or month >= 13:
                    dialog()
                return month

            dates = []
            # 1 - месяц
            if var == 1:
                month = dialog()
                not_finished = False
                last_day = calendar.monthrange(datetime.date.today().year, month)[1]
                day = 1
                while not not_finished:
                    date = datetime.datetime(year=datetime.date.today().year, month=month, day=day)
                    dates.append(date.strftime('%d'))
                    if day == last_day:
                        not_finished = True
                    day += 1
                return dates
            # 2 - неделя
            if var == 2:
                num = 0
                while num < 7:
                    day = f'{datetime.datetime.now().day - datetime.datetime.now().weekday() + num}'
                    dates.append(day)
                    num += 1
                return dates

        def dialog():
            print("Выберите диапозон дат:\n"
                  "[1] - Месяц\n"
                  "[2] - Текущая неделя\n"
                  "[0] - Назад")

            var = input()
            if var == '0':
                return int(var)
            elif var == '1':
                return int(var)
            elif var == '2':
                return int(var)
            else:
                dialog()

        var = dialog()
        if var == 0:
            return
        if var == 2:
            title = 'Работа пользователя за текущую неделю'
        else:
            title = 'Работа пользователя за выбранный месяц'

        dates = get_dates(var)
        new_logs = []
        for log in db.logs:
            for day in dates:
                if str(log.get_data()) == str('10/' + day):
                    new_logs.append(log)

        g = []
        for day in dates:
            count = 0
            for log in new_logs:
                if str(log.get_data()) == str('10/' + day):
                    if log.id == str(user.id):
                        count += 1
            g.append(count)

        width = 0.1
        x = np.arange(len(dates))
        fig, ax = plt.subplots()
        rects = ax.bar(x, g, width, label=user.last_name)

        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(dates)
        ax.legend()

        plt.show()

    def dialog():
        print("\tПостроение графика\n"
              "Выберите опцию:\n"
              "[1] - Всех пользователей\n"
              "[2] - Конкретного пользователя\n"
              "[0] - Назад")
        var = input()
        if var == '0':
            return int(var)
        elif var == '1':
            return int(var)
        elif var == '2':
            return int(var)
        else:
            dialog()

        return var

    var = dialog()
    if var == 0:
        return
    if var == 1:
        all_users_graph()
    else:
        user_table = PrettyTable()
        user_table.field_names = ["id", "Фамилия", "Имя", "Отчество", "Пол", "Роль", "Статус"]
        for user in db.users:
            user_table.add_row(
                [user.id, user.last_name, user.first_name, user.middle_name, user.gender, user.role,
                 user.is_enabled])
        print(user_table)

        def find_user():
            for user in db.users:
                if user.id == int(user_id):
                    return user

        def check_users():
            for user in db.users:
                temp = str(user.id)
                if temp == user_id:
                    return True
            print("Пользователь с таким id не существует!")
            return False

        is_user_exist = False
        while not is_user_exist:
            user_id = input("Введите id пользователя: ")
            is_user_exist = check_users()
        user = find_user()
        current_user_graph(user)
    create_graph()

def create_stat():
    user_table = PrettyTable()
    user_table.field_names = ["id", "Фамилия", "Имя", "Отчество", "Пол", "Роль", "Статус"]
    for user in db.users:
        user_table.add_row(
            [user.id, user.last_name, user.first_name, user.middle_name, user.gender, user.role,
             user.is_enabled])
    print(user_table)

    def find_user():
        for user in db.users:
            if user.id == int(user_id):
                return user

    def check_users():
        for user in db.users:
            temp = str(user.id)
            if temp == user_id:
                return True
        print("Пользователь с таким id не существует!")
        return False

    is_user_exist = False
    while not is_user_exist:
        user_id = input("Введите id пользователя: ")
        is_user_exist = check_users()
    user = find_user()

    temp_logs = [log for log in filter(lambda log: log.id == str(user.id), db.logs)]
    total_time = datetime.timedelta(0)
    login_count = len(temp_logs)
    for log in temp_logs:
        total_time += log.get_session_time()
    total_time = total_time.seconds / 60

    p = Petrovich()
    if user.gender == 'муж':
        gender = Gender.MALE
    else:
        gender = Gender.FEMALE
    dative_fullname = (p.lastname(user.last_name, Case.GENITIVE, gender) + " " +
                       p.firstname(user.first_name, Case.GENITIVE,gender) + " " +
                       p.middlename(user.middle_name, Case.GENITIVE, gender))
    print(f"Статистика {dative_fullname}\n"
          f"Количество входов: {login_count}\n"
          f"Время работы: {total_time} минут\n")


# блок меню админа
def admin_menu():
    def dialog():
        print("\tМеню администратора\n"
              "[1] - Управление пользователями\n"
              "[2] - Просмотр статистики\n"
              "[3] - Построение графика\n"
              "[0] - Выйти из аккаунта")
        result = input()
        if result == '1':
            user_managment()
            dialog()
        elif result == '2':
            create_stat()
            dialog()
        elif result == '3':
            create_graph()
            dialog()
        elif result == '0':
            return
        else:
            dialog()

    dialog()
