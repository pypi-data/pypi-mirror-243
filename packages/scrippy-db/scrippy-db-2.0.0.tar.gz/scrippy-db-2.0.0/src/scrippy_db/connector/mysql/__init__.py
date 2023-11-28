from scrippy_db import logger
import mysql.connector


class DbMysql:

  @staticmethod
  def connect(username, password, host, port, database, service):
    return mysql.connector.connect(user=username,
                                   password=password,
                                   host=host,
                                   port=port,
                                   database=database)

  @staticmethod
  def query(cursor, query, params=None, verbose=False):
    if verbose:
      logger.info(f"Query: {query}")
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
