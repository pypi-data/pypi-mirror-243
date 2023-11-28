from scrippy_db import logger
import sqlite3

class DbSqlite3:

  @staticmethod
  def connect(username=None,
              password=None,
              host=None,
              port=None,
              database=None,
              service=None):
    return sqlite3.connect(database=database)

  @staticmethod
  def query(cursor, query, params=None, verbose=False):
    if verbose:
      logger.info(f"Request: {query}")
      logger.info(f"Params: {params}")
    if params is not None:
      cursor.execute(query, params)
    else:
      cursor.execute(query)
    rows = cursor.fetchall()
    if verbose:
      for row in rows:
        logger.info(f"{' | '.join([str(i) for i in row])}")
    return rows
