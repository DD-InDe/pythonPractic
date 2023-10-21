import datetime
import db

logged_user = 0
user_log_in = 0
user_log_out = 0

def save_session():
    session = db.Log(logged_user.id, user_log_in,user_log_out)
    db.logs.append(session)
    db.update_data()