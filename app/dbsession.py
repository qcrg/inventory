from sqlalchemy.orm import sessionmaker as _sessionmaker
from sqlalchemy import create_engine as _create_engine
from config.database import get_db_user_url as _get_url

_engine = _create_engine(_get_url())
_SessionLocal = _sessionmaker(bind=_engine, autoflush=False)

def create_session():
  return _SessionLocal()

class SessionWrapper():
  def __init__(self):
    self.session = create_session()
  
  def __del__(self):
    print("Session closed")
    self.session.close()