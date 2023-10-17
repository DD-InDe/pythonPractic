# блок меню админа
import db
import sys
from prettytable import PrettyTable


def admin_menu():
    print("\tМеню администратора\n")

    def dialog():
        print("1 - Управление пользователями\n"
              "2 - Просмотр статистики\n"
              "3 - Построение графика\n"
              "0 - Выйти")
        result = input()
        if result == 1:
            print()
        elif result == 2:
            print()
        elif result == 3:
            print()
        elif result == 0:
            exit(1)
        else:
            dialog()

    dialog()


db.upload_data()


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

        def dialog():
            print("Выберите вариант вывода\n"
                  "1 - Вывести А-Я\n"
                  "2 - Вывести Я-А\n"
                  "3 - Вывести активных пользователей\n"
                  "4 - Вывести неактивных пользователей\n"
                  "5 - Вывести Мужчин\t"
                  "6 - Вывести Женщин\t")
            result = int(input())
            if result == 1:
                temp = db.users.copy()
                temp.sort()
                users_print()

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


user_managment()
