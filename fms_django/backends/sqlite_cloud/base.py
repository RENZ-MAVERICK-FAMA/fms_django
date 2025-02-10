from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
import sqlitecloud

class DatabaseWrapper(SQLiteDatabaseWrapper):
    def get_connection_params(self):
        # Get the default connection parameters
        settings_dict = self.settings_dict
        params = super().get_connection_params()

        # Ensure 'database' is included in the parameters
        params['database'] = settings_dict['NAME']
        return params

    def get_new_connection(self, conn_params):
        # Debugging: Print conn_params to inspect its contents
        print("Connection parameters:", conn_params)

        # Extract the database URL from conn_params
        db_url = conn_params.get('database')  # Use 'database' instead of 'name'
        if not db_url:
            raise ValueError("Database URL is missing. Check your DATABASES setting in settings.py.")

        # Connect to SQLite Cloud
        return sqlitecloud.connect(db_url)

    def create_cursor(self, name=None):
        # Override create_cursor to avoid passing the 'factory' argument
        return CursorWrapper(self.connection.cursor(), self)


class CursorWrapper:
    def __init__(self, cursor, connection):
        self.cursor = cursor
        self.connection = connection

    def execute(self, sql, params=None):
        # Replace Django's parameter placeholders (%s) with SQLite Cloud's format (?)
        if params:
            sql = sql.replace('%s', '?')
        # Handle cases where params is None
        params = () if params is None else params
        return self.cursor.execute(sql, params)

    def executemany(self, sql, param_list):
        # Replace Django's parameter placeholders (%s) with SQLite Cloud's format (?)
        sql = sql.replace('%s', '?')
        return self.cursor.executemany(sql, param_list)

    def __getattr__(self, attr):
        # Delegate other methods and attributes to the underlying cursor
        return getattr(self.cursor, attr)