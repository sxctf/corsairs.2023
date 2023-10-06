from tsapp.routes import app, db
from tsapp.models import TS_User, TS_Task
from tsapp.config import file_db
import time
import os

db_is_created = os.path.exists(file_db)
if not db_is_created:
    with app.app_context():
        db.create_all()
        app.logger.info('[INIT] [DB] [Succeess] DB create <%s>', app.config['SQLALCHEMY_DATABASE_URI'])
        time.sleep(3)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run()
