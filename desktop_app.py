import sys
import os
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl
import threading
from waitress import serve
from fms_django.wsgi import application  # Replace 'fms_django' with your project name

def run_django_server():
    """
    Function to start the Django app using Waitress.
    """
    print("Starting Django server with Waitress...")
    serve(application, host='127.0.0.1', port=8000)
    print("Django server started.")

if __name__ == '__main__':
    # Start the Django server in a separate thread
    server_thread = threading.Thread(target=run_django_server)
    server_thread.daemon = True  # Ensure the thread stops when the main app exits
    server_thread.start()

    # Create the PyQt5 application
    app = QApplication(sys.argv)

    # Create a web view and load the Django app
    web_view = QWebEngineView()
    web_view.load(QUrl("http://127.0.0.1:8000"))
    web_view.resize(1024, 768)
    web_view.show()

    # Execute the PyQt5 app
    sys.exit(app.exec_())