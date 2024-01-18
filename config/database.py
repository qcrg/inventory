### config
IP = "127.0.0.1"
PORT = 3306
NAME = "inventory"

### helpers

_BASE_URL_FMT = "mysql://{user}:{password}@{ip}:{port}"

def base_url(user, password):
  return _BASE_URL_FMT.format(user = user,
                    password = password,
                    ip = IP,
                    port = PORT)

def db_url(user, password):
  return _BASE_URL_FMT.format(user = user,
                    password = password,
                    ip = IP,
                    port = PORT) + "/" + NAME

def get_base_user_url():
  from . import db_user as info
  return base_url(info.USERNAME, info.PASSWORD)

def get_base_root_url():
  from . import db_root as info
  return base_url(info.USERNAME, info.PASSWORD)

def get_db_user_url():
  from . import db_user as info
  return db_url(info.USERNAME, info.PASSWORD)

def get_db_root_url():
  from . import db_root as info
  return db_url(info.USERNAME, info.PASSWORD)