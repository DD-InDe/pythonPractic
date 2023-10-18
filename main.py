import datetime
import db
import create_log
import admin_actions
import user_actions


# блок авторизации
def authentication():
    def dialog():
        print()
        result = input()
        if result == '1':
            authentication()
        else:
            exit(1)

    print("Логин:",end=' ')
    login = input()
    print("Пароль:",end=' ')
    password = input()
    for user in db.users:
        if user.login == login and user.password == password:
            if user.is_enabled:
                create_log.logged_user = user.id
                create_log.user_log_in = datetime.datetime.now()
                print("Вы вошли в систему как", user.get_fullname())
                if user.role == 'admin':
                    admin_actions.admin_menu()
                if user.role == 'user':
                    user_actions.user_menu()

            else:
                print("Ваша учетная запись неактивна")
                dialog()
        else:
            print("Пользователь с такими данными не найден")
            dialog()


if __name__ == '__main__':
    db.upload_data(db.database)
    print("Добро пожаловть!\nАтворизируйтесь в системе")
    authentication()