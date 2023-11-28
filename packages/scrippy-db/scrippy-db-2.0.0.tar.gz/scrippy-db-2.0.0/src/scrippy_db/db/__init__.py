import re
from scrippy_db.connector.pgsql import DbPgsql
from scrippy_db.connector.sqlite3 import DbSqlite3
from scrippy_db.connector.mysql import DbMysql
from scrippy_db.connector.oracle import DbOracle
from scrippy_db import ScrippyDbError, logger


class Database:
  """This class purpose is to provide a simplified interface to all major relational database types.

  Arguments:
    ``db_type``: String, one of `postgres`, `sqlite3`, `mysql`. Mandatory.
    ``database``: The database name. Optional if provided by a service file.
    ``username``: String. Optional.
    ``password``: String. Optional.
    ``host``: String. Optional.
    ``port``: Int. Optional.
    ``service``: String. A PostgresSQL service name. Optional.
  """

  def __init__(self, db_type, database=None,
               username=None, password=None,
               host=None, port=None, service=None):
    self.db_type = db_type
    self.database = database
    self.host = host
    self.port = port
    self.service = service
    self.username = username
    self.password = password
    self.connectors = {"pgsql": DbPgsql,
                       "sqlite3": DbSqlite3,
                       "mysql": DbMysql,
                       "oracle": DbOracle}
    self.connector = None
    self.connection = None
    self.cursor = None

  def __enter__(self):
    self.connector = self.connectors[self.db_type]
    return self

  def __exit__(self, kind, value, traceback):
    if self.connection is not None:
      self.connection.close()

  def connect(self):
    """
    Connects to the database with database connection parameters provided at init time.
    """
    logger.debug("Connecting to database...")
    return self.connector.connect(username=self.username,
                                  password=self.password,
                                  host=self.host,
                                  port=self.port,
                                  database=self.database,
                                  service=self.service)

  def query(self, query, params=None, commit=False,
            verbose=False, exit_on_error=True):
    """Prepare and execute the specified query on the database.
    In conformance to `Python Database API v2.0` (See https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while query execution, the query will be `rollbacked`.

    Arguments:
      ``query``: String. The SQL query to execute. The string query should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle)v for parameters mapping.
      ``params``: An optional dictionary specifying the needed parameters to be mapped on the ``query`` string.
      ``commit``: Boolean. When set to `True`, a commit statement will be sent to the database immediately after the query execution.
      ``verbose``: Boolean. If set to `True`, query, parameters and result will be sent to the logger. Default to ``False``
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while query execution will raise an error and exit the workflow after query rollback. Default to ``True``.

    Returns:
      A database ``cursor`` containing the returned values.
    """
    with self.connect() as self.connection:
      logger.debug("Querying the database...")
      self.cursor = self.connection.cursor()
      try:
        rows = self.connector.query(cursor=self.cursor,
                                    query=query,
                                    params=params,
                                    verbose=verbose)
        if commit:
          self.connection.commit()
        if len(rows) > 0:
          return rows
        return None
      except Exception as err:
        logger.error(f"[{err.__class__.__name__}] {err}")
        logger.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise ScrippyDbError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err

  def multi_query(self, query, paramlist, commit=False,
                  verbose=False, exit_on_error=False):
    """Prepare and execute the specified query on the database for each set of parameters found in the`` paramlist`` argument.
    In conformance to `Python Database API v2.0` (See https://peps.python.org/pep-0249), parameters may be provided as sequence or mapping and will be bound to variables in the operation. If error occurs while query execution, the query will be `rollbacked`.

    This method is intended to insert data or update the database. It is not intended to retrieve data.

    Arguments:
      ``query``: String. The SQL query to execute. The string query should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle) for parameters mapping.
      ``paramlist``: An mandatory list of dictionaries specifying the needed parameters to be mapped on each execution of the ``query`` string.
      ``commit``: Boolean. When set to `True`, a commit statement will be sent to the database immediately after each query execution.
      ``verbose``: Boolean. If set to `True`, each query, parameters and result will be sent to the logger.
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while one of the query executions will raise an error and exit the workflow after current query rollback.

    Returns: None"""
    logger.debug("Querying the database...")
    with self.connect() as self.connection:
      self.cursor = self.connection.cursor()
      try:
        for params in paramlist:
          rows = self.connector.query(cursor=self.cursor,
                                      query=query,
                                      params=params,
                                      verbose=verbose)
          if commit:
            self.connection.commit()
      except Exception as err:
        logger.error(f"[{err.__class__.__name__}] {err}")
        logger.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise ScrippyDbError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err

  def transaction(self, queries, verbose=False, exit_on_error=False):
    """Prepare and execute on the database as a single transaction each query found in the ``queries`` list.

    The whole transaction is committed only if all queries specified in the ``queries`` argument are executed without error. If an error occurs within the transaction, the whole transaction is rollbacked.

    This method is intended to insert data or update the database. It is not intended to retrieve data.

    Arguments:
      ``queries``: A list of dictionaries specifying all queries and needed parameters to be executed within the transaction. The SQL query to execute. The string query should use the `named paramstyle` (see https://peps.python.org/pep-0249/#paramstyle) for parameters mapping.

      Each dictionary in the ``queries`` list must provide at least a ``query`` item specifying a query to execute. It may also provide a ``params`` item which is a dictionary of parameters to be mapped onto the ``query`` string (see the ``query()`` method for further details).
      ``verbose``: Boolean. If set to `True`, each query, parameters and result will be sent to the logger.
      ``exit_on_error``: Boolean. If set to `True`, any error encountered while one of the query executions will raise an error and exit the workflow after transaction rollback

    Returns: None"""

    logger.debug("Beginning transaction...")
    with self.connect() as self.connection:
      self.cursor = self.connection.cursor()
      try:
        for query in queries:
          rows = self.connector.query(cursor=self.cursor,
                                      query=query.get("query"),
                                      params=query.get("params"),
                                      verbose=verbose)
        self.connection.commit()
      except Exception as err:
        logger.error(f"[{err.__class__.__name__}] {err}")
        logger.error("Rollbacking...")
        self.connection.rollback()
        if exit_on_error:
          raise ScrippyDbError(f"[DatabaseQueryError] An error occurred while querying the database: {err}") from err


class ConnectionChain:
  """The ConnectionChain object allows you to retrieve connection information to a database from a character string following the format
  <DB_TYPE>:<ROLE>/<PASSWORD>@<HOST>:<PORT>//<DB_NAME>."""
  def __init__(self, connection_chain):
    pattern = r"^(.+):(.+)/(.+)@(.+):(.+)//(.+)$"
    self.db_type, self.username, self.password, self.host, self.port, self.database = re.match(pattern, connection_chain).groups()
    self.port = int(self.port)


class DbFromConnectionChain(Database):
  """The DbFromCc class allows a Db obkject instanciation directly from a ConnectionChain object."""
  def __init__(self, connection_chain):
    c_chain = ConnectionChain(connection_chain)
    super().__init__(username=c_chain.username,
                     host=c_chain.host,
                     database=c_chain.database,
                     port=c_chain.port,
                     password=c_chain.password,
                     service=None,
                     db_type=c_chain.db_type)
