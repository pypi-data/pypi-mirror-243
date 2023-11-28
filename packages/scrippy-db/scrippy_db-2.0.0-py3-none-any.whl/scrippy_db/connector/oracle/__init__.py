from scrippy_db import logger
import cx_Oracle


class DbOracle:

  @staticmethod
  def connect(username, password, host, port, database, service):
    dsn = cx_Oracle.makedsn(host, port, service_name=database)
    return cx_Oracle.connect(username, password, dsn)

  @staticmethod
  def query(cursor, query, params=None, verbose=False):
    if verbose:
      logger.info(f"Query: {query}")
      logger.info(f"Params: {params}")
    if params is not None:
      cursor.execute(query, params)
    else:
      cursor.execute(query)
    try:
      rows = cursor.fetchall()
      if verbose:
        for row in rows:
          logger.info(f"{' | '.join([str(i) for i in row])}")
      return rows
    except cx_Oracle.InterfaceError:
      return list()
