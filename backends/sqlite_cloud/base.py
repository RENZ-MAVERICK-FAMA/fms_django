from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
import sqlitecloud

class DatabaseWrapper(SQLiteDatabaseWrapper):
    def get_new_connection(self, conn_params):
        # Debugging: Print conn_params to inspect its contents
        print("Connection parameters:", conn_params)

        # Ensure 'name' exists in conn_params
        if 'name' not in conn_params:
            raise ValueError("Missing 'name' in connection parameters. Check your DATABASES setting.")

        # Connect to SQLite Cloud
        url = conn_params['name']
        return sqlitecloud.connect(url)