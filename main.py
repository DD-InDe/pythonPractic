import datetime
import db
import create_log
import admin_actions
import user_actions


# блок авторизации
def authentication():
    def dialog():
        print("[1] - Повторить попытку")
        result = input()
        if result == '1':
            authentication()
        else:
            exit(1)

    print("Логин:", end=' ')
    login = input().replace(" ", "")
    print("Пароль:", end=' ')
    password = input().replace(" ", "")
    for user in db.users:
        if user.login == login and user.password == password:
            if user.is_enabled:
                create_log.logged_user = user
                create_log.user_log_in = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                print("Вы вошли в систему как", user.get_fullname())
                if user.role == 'admin':
                    admin_actions.admin_menu()
                    return
                if user.role == 'user':
                    user_actions.user_menu()
                    return
            else:
                print("Ваша учетная запись неактивна")
                dialog()

    print("Пользователь с такими данными не найден")
    dialog()


if __name__ == '__main__':
    try:
        db.upload_data(db.database)
        print("Добро пожаловать!\nАвторизируйтесь в системе")
        authentication()
        raise RuntimeError
    except Exception as exception:
        print(exception)
    except exit():
        pass
    finally:
        if create_log.logged_user != 0:
            create_log.user_log_out = datetime.datetime.now().strftime('%d/%m/%Y %H:%M:%S')
            create_log.save_session()