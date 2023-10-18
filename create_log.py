import datetime
import db

logged_user = str
user_log_in = datetime.datetime.now()
user_log_out = datetime.datetime.now()

def save_session():
    session = db.Log(logged_user, user_log_in,user_log_out)
    db.logs.append(session)