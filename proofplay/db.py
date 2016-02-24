from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google'):
    # the second arg after : is the db instance name
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/provisioning?unix_socket=/cloudsql/skykit-display-device-int:provisioning-int"
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost/provisioning'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
