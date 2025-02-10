from django.db.backends.sqlite3.base import DatabaseWrapper as SQLiteDatabaseWrapper
import sqlitecloud
import sys
import os
from pathlib import Path
# Add the project root directory to the Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
class DatabaseWrapper(SQLiteDatabaseWrapper):
    def get_new_connection(self, conn_params):
        # Connect to SQLite Cloud
        url = conn_params['name']
        return sqlitecloud.connect(url)