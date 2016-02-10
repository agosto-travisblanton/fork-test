from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google'):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/logging?unix_socket=/cloudsql/skykit-logs-reporter:skykit-logs-reporter"
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost/provisioning'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine)
Session = session_factory
