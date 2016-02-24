from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy import create_engine
from determine_env import get_env

env = get_env()

# the second arg after : is the db instance name
if env == "INT":
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/provisioning?unix_socket=/cloudsql/skykit-display-device-int:provisioning-int"

elif env == "STAGE":
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/provisioning?unix_socket=/cloudsql/skykit-provisioning-stage-int:provisioning-stage"

elif env == "PROD":
    SQLALCHEMY_DATABASE_URI = "mysql+mysqldb://root@/provisioning?unix_socket=/cloudsql/skykit-provisioning-int:provisioning-prod"

else:
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqldb://root@localhost/provisioning'

engine = create_engine(SQLALCHEMY_DATABASE_URI)
session_factory = sessionmaker(bind=engine, expire_on_commit=False)
Session = scoped_session(session_factory)
