import sys
import json
import db


db.upload_data()
db.update_data()

# # метод для считывания json-файла со всеми данными
# def read_info(file_name):
#     with open(file_name, 'r', encoding="utf-8") as file:
#         return json.load(file)
#
#
# # блок авторизации
# def authentication():
#     def dialog():
#         print("1 - Авторизация\nЛюбая(кроме 1) кнопка - Выйти")
#         result = input()
#         if result == 1:
#             authentication()
#         else:
#             exit(1)
#
#     print("Логин: ")
#     login = input()
#     print("Пароль: ")
#     password = input()
#     for user in users:
#         if user['login'] == login and user['password'] == password:
#             if user['is_enabled'] == True:
#                 print("Вы вошли в систему как", get_fullname(user))
#                 current_user = user
#             else:
#                 print("Ваша учетная запись неактивна")
#                 dialog()
#         else:
#             print("Пользователь с такими данными не найден")
#             dialog()
#
#
# # блок меню админа
# # def admin_menu():
# #     print("\tМеню администратора")
# #
# #     def dialog():
# #         print("1 - Управление пользователями\n2 - Просмотр статистики\n3 - Построение графика")
# #         result = input()
# #         if result == 1:
# #             print()
# #         elif result == 2:
# #             print()
# #         elif result == 3:
# #             print()
# #         else:
# #             dialog()
# #
# #     dialog()
# # блок управления пользователями (админ)
# # def user_managment():
# #     print("\tУправление пользователями\n")
# #     print("\tПользователи системы")
# #     for user in users:
# #         print("")
# # метод для создания строки фио
# def get_fullname(user):
#     return user['last_name'] + " " + user['first_name'] + " " + user['middle_name']
#
#
# # присваеваем переменной считанные данные
# database = read_info("db.json")
# users = database["user"]
# print("Добро пожаловть!\nАтворизируйтесь в системе")
# authentication()
#
# import subprocess
#
# subprocess.Popen(r'explorer /open,"C:\Users\deer\RiderProjects\WpfApp2\WpfApp2\test.txt"')
