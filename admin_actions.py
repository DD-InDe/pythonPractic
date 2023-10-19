import calendar
import datetime
from datetime import date, timedelta
import matplotlib.pyplot as plt
import numpy as np

import create_log
import db
from prettytable import PrettyTable
from operator import attrgetter


# блок управления пользователями (CRUD)
def user_managment():
    # вывод пользователей
    def users_print(users_list):
        user_table = PrettyTable()
        user_table.field_names = ["id", "Фамилия", "Имя", "Отчество", "Пол", "Роль", "Статус"]
        for user in users_list:
            user_table.add_row(
                [user.id, user.last_name, user.first_name, user.middle_name, user.gender, user.role,
                 user.is_enabled])
        print(user_table)

    # задание фильтра и поиска
    def users_view():
        def select_sort(list):
            print("Выберите вариант сортировки\n"
                  "[1] - Вывести А-Я\n"
                  "[2] - Вывести Я-А\n")

            sort_result = input()
            if sort_result == '1':
                list.sort(key=attrgetter('last_name'), reverse=False)
                return list
            elif sort_result == '2':
                list.sort(key=attrgetter('last_name'), reverse=True)
                return list
            else:
                select_sort(list)

        print("Выберите вариант вывода\n"
              "[1] - Вывести всех пользователей\n"
              "[2] - Вывести активных пользователей\n"
              "[3] - Вывести неактивных пользователей\n"
              "[4] - Вывести Мужчин\n"
              "[5] - Вывести Женщин\n")

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
        else:
            dialog()

        temp = select_sort(temp)
        users_print(temp)
        return

    # создание пользователя
    def user_add():
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

    def user_delete():
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

    print("\tУправление пользователями\n")

    def dialog():
        print("1 - Вывести пользователей\n"
              "2 - Добавить пользователя\n"
              "3 - Удалить пользователя\n"
              "4 - Редактировать пользователя\n")
        result = input()

        if result == '1':
            users_view()
        elif result == '2':
            user_add()
        elif result == '3':
            user_delete()
        elif result == '4':
            user_edit()
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
                  "1 - Месяц\n"
                  "2 - Текущая неделя\n")

            var = int(input())
            if (var < 1 or var > 2):
                dialog()
            return var

        temp_users = []

        var = dialog()
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
                  "1 - Месяц\n"
                  "2 - Текущая неделя\n")

            var = int(input())
            if (var < 1 or var > 2):
                dialog()
            return var

        var = dialog()
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
        print("Выберите опцию:\n"
              "1 - Всех пользователей\n"
              "2 - Конкретного пользователя\n")
        var = int(input())
        if var < 1 or var > 2:
            dialog()

        return var

    var = dialog()
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
        total_time+=log.get_session_time()
    total_time = total_time.seconds/60
    print(f"Статистика {user.get_fullname()}\n"
          f"Количество входов: {login_count}\n"
          f"Время работы: {total_time} минут")


# блок меню админа
def admin_menu():
    print("\tМеню администратора\n")

    def dialog():
        print("1 - Управление пользователями\n"
              "2 - Просмотр статистики\n"
              "3 - Построение графика\n"
              "0 - Выйти")
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
