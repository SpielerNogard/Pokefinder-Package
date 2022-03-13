import mariadb
from pokefinder.logging.get_logger import get_logger
import sys

class MariaDB:
    """Class to create an Client to handle all interaction with mariadb.
    Parameters
    ----------
    server: str 
        Server ip where the mariad db is located.
    databasename: str
        name of the database to connect to.
    user: str
        username for authentification ageinst db server.
    password: str
        password to authentificate as the user.
    port: int (default: 3306)
        port where the DB is located on the Server."""
    def __init__(self,  
                 server:str,
                 databasename:str,
                 user:str,
                 password:str,
                 port:int=3306):
        self._port = port 
        self._password = password
        self._database_name = databasename
        self._server = server
        self._user = user
        self._logger = get_logger('info')

        try:
            self._conn = mariadb.connect(user=self._user,
                                        password=self._password,
                                        host=self._server,
                                        port=self._port,
                                        database=self._database_name
        )
            self._logger.info(f'Connected to Database: {self._database_name}')
        except mariadb.Error as exc:
            self._logger.error(f'Cant connecting to MariaDB Platform: {exc}')
            sys.exit(1)

    def read_data(self,sql_command):
        """Method to read data from table.
        Parameters
        ----------
        sql_command:str
            SQL Command to be executed.

        Return
        ------
        response: list
            a list including every DB entry found for your query.
        """
        cur = self._conn.cursor()
        self._logger.info(f'SQL command is executed: {sql_command}')
        cur.execute(sql_command)
        sql_return = cur
        response = []
        for item in sql_return:
            response.append(item)
        return response

    def write_data(self,sql_command):
        """Method to write data to database.
        Parameters
        ----------
        sql_command: str
         SQL Command to be executed in DB.

        """
        cur = self._conn.cursor()
        self._logger.info(f'SQL command is executed: {sql_command}')
        cur.execute(sql_command) 
        self._conn.commit()        
        