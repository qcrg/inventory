#!/bin/env python3
import add_app_root

from sqlalchemy import create_engine as _create_engine
import config.db_user as _db_conf
from config.database import \
  get_base_root_url as _get_base_url, get_db_root_url as _get_db_url, \
  NAME as _DB_NAME

def _create_tables(engine):
  from app.models import Base
  Base.metadata.create_all(bind=engine)

def _create_db(engine):
  engine.execute("CREATE DATABASE IF NOT EXISTS " + _DB_NAME + ";")

def _create_user(engine):
  engine.execute("CREATE USER IF NOT EXISTS %s IDENTIFIED BY '%s'" %
                 (_db_conf.USERNAME, _db_conf.PASSWORD))

def _grant_privileges(engine):
  engine.execute(
    "GRANT INSERT, UPDATE, DELETE, SELECT, REFERENCES ON %s.* TO '%s'" %
    (_DB_NAME, _db_conf.USERNAME))

def createdb():
  engine = _create_engine(_get_base_url())
  _create_db(engine)
  _create_user(engine)
  _grant_privileges(engine)

  engine = _create_engine(_get_db_url())
  _create_tables(engine)

### exec
if __name__ == "__main__":
  createdb()