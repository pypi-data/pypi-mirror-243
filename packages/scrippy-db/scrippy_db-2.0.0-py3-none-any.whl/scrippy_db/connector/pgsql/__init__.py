from scrippy_db import logger
import psycopg2


class DbPgsql:

  @staticmethod
  def connect(username, password, host, port, database, service):
    if service is not None:
      logger.warning(f"Using service {service}. Username, password, host and port are ignored.")
      return psycopg2.connect(service=service)
    return psycopg2.connect(user=username,
                            host=host,
                            port=port,
                            dbname=database,
                            password=password)

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
    except psycopg2.ProgrammingError:
      return list()
