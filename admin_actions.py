# блок меню админа
def admin_menu():
    print("\tМеню администратора")

    def dialog():
        print("1 - Управление пользователями\n2 - Просмотр статистики\n3 - Построение графика")
        result = input()
        if result == 1:
            print()
        elif result == 2:
            print()
        elif result == 3:
            print()
        else:
            dialog()

    dialog()


# блок управления пользователями (админ)
def user_managment(users):
    print("\tУправление пользователями\n")
    print("\tПользователи системы")
    for user in users:
        print("")
