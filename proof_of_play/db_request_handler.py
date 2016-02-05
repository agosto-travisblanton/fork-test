from webapp2 import RequestHandler
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

if os.environ.get('SERVER_SOFTWARE', '').startswith('Google'):
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/logging?unix_socket=/cloudsql/skykit-logs-reporter:skykit-logs-reporter-prod"
else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://daniel:agosto@173.194.235.204/logging'

engine = create_engine(SQLALCHEMY_DATABASE_URI)

db = scoped_session(sessionmaker(bind=engine))


