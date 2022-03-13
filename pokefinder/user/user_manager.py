"""class to create an Usermanager"""
from pokefinder.logging.get_logger import get_logger
from pokefinder.databases.maria_db_client import MariaDB

class UserManager:
    """Class to handle all User related functions."""
    def __init__(self):
        self._server = "0.0.0.0"
        self._port = 3306
        self._username = "root"
        self._password = 'qwerty'
        self._user_data_db = MariaDB(server=self._server,
                                    databasename='pokefinder',
                                    user=self._username,
                                    password=self._password,
                                    port=self._port)
        self._logger = get_logger('INFO')

    def register_new_user(self,user_id, username):
        """Method to register a new user.
        If the user is already registered, the registration will be skipped"""
        self._logger.info(f'registering new user')
        SQL = f'SELECT * from user_data where userid = {user_id};'
        response = self._user_data_db.read_data(SQL)
        if len(response) == 0:
            SQL = f'INSERT INTO user_data(userid, username) values("{user_id}","{username}");'
            self._user_data_db.write_data(SQL)
        else:
            self._logger.info(f'user: {user_id} already exists. no need to register')
