import datetime
import db

logged_user = str
user_log_in =  str
user_log_out = str

def save_session():
    session = db.Log(logged_user.id, user_log_in,user_log_out)
    db.logs.append(session)
    db.update_data()