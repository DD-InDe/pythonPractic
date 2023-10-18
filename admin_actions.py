import db
import sys
from prettytable import PrettyTable
from operator import attrgetter


# блок управления пользователями (CRUD)
def user_managment():
    def users_view():
        def users_print(users_list):
            user_table = PrettyTable()
            user_table.field_names = ["id", "Фамилия", "Имя", "Отчество", "Пол", "Роль", "Статус"]
            for user in users_list:
                user_table.add_row(
                    [user.id, user.last_name, user.first_name, user.middle_name, user.gender, user.role,
                     user.is_enabled])
            print(user_table)
            users_view()

        def dialog():
            def select_sort(list):
                print("Выберите вариант вывода\n"
                      "[1] - Вывести А-Я\n"
                      "[2] - Вывести Я-А\n")

                sort_result = input()
                if result == '1':
                    list

            print("Выберите вариант вывода\n"
                  "[1] - Вывести А-Я\n"
                  "[2] - Вывести Я-А\n"
                  "[3] - Вывести активных пользователей\n"
                  "[4] - Вывести неактивных пользователей\n"
                  "[5] - Вывести Мужчин\n"
                  "[6] - Вывести Женщин\n")

            result = input()
            temp = db.users.copy()

            if result == 1:
                temp.sort(key=attrgetter('last_name'), reverse=False)
            if result == 2:
                temp.sort(key=attrgetter('last_name'), reverse=False)
            if result == 3:
                temp = [user for user in filter(lambda user: user.is_enabled == True, temp)]
            if result == 4:
                temp = [user for user in filter(lambda user: user.is_enabled == True, temp)]
            if result == 5:
                temp = [user for user in filter(lambda user: user.gender == "male", temp)]
            if result == 6:
                temp = [user for user in filter(lambda user: user.gender == "female", temp)]

            users_print(temp)

        dialog()

    print("\tУправление пользователями\n")

    def dialog():
        print("1 - Вывести пользователей\n"
              "2 - Добавить пользователя\n"
              "3 - Удалить пользователя\n"
              "4 - Редактировать пользователя\n")
        result = int(input())

        if result == 1:
            users_view()
        elif result == 2:
            print()
        elif result == 3:
            print()
        elif result == 4:
            print()
        elif result == 0:
            exit(1)
        else:
            dialog()

    dialog()

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
        elif result == '2':
            print()
        elif result == '3':
            print()
        elif result == '0':
            exit(1)
        else:
            dialog()

    dialog()