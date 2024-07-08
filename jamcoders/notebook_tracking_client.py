####################################################################################################
# JamCoders Notebook Tracker Client
#
# This file is a copy of https://github.com/shaferjo/jam_coder_server/blob/main/notebook_tracker/client.py
####################################################################################################


####################################################################################################
# Installs
####################################################################################################

#!pip install requests --quiet


####################################################################################################
# Imports
####################################################################################################

import inspect
import requests
import socket
import subprocess
import importlib

from urllib.parse import urljoin
from google.colab import auth

from .common import EVENT


####################################################################################################
# Constants
####################################################################################################

SERVER_URL = "https://jamescheng.pythonanywhere.com"
ASSERTION_URL = urljoin(SERVER_URL, "notebook_tracker/assertion/")


####################################################################################################
# Classes
####################################################################################################

class NotebookTracker():

    is_initialized = False
    current_user_email = None
    current_notebook_id = None

    ################################################################################################
    # Colab Hacks
    ################################################################################################

    @staticmethod
    def get_user_email():
        """
        This is a hack and may break in the future if colab change their implementation.
        """
        try:
            auth.authenticate_user()
            result = subprocess.run(['gcloud', 'config', 'get-value', 'account'], stdout=subprocess.PIPE)
            email_address = result.stdout.decode("utf-8").strip()
            return email_address
        except:
            return None
    
    @staticmethod
    def get_user_name():
        # Dynamically import colab module
        module = importlib.import_module("__main__")

        # Access the module's global variables
        module_globals = vars(module)

        if "student_name" in module_globals:
            return module_globals["student_name"]
        else:
            print("User name not found.")
            return None

    @staticmethod
    def get_notebook_name():
        """
        This is a hack and may break in the future if colab change their implementation.
        """
        # try:
        #     ip = socket.gethostbyname(socket.gethostname())
        #     return requests.get(f"http://{ip}:9000/api/sessions").json()[0]["name"]
        # except:
        #     return None
        # Dynamically import colab module
        module = importlib.import_module("__main__")

        # Access the module's global variables
        module_globals = vars(module)

        if "notebook_name" in module_globals:
            return module_globals["notebook_name"]
        else:
            print("Notebook name not found.")
            return None
        
    @staticmethod
    def get_cell_id():
        """
        This is a hack and may break in the future if colab change their implementation.
        """
        result = None
        stack = inspect.stack()
        for frame_info in stack:
            if frame_info.function == "execute_request":
                try:
                    result = frame_info.frame.f_locals["parent"]["metadata"]["colab"]["cell_id"]
                except:
                    pass
                break
        return result


    ################################################################################################
    # Assertion Event
    ################################################################################################

    def send_assertion_event(self, assertions_result):
        assert self.is_initialized, (
            f"Must call init() before using send_assertion_event()."
        )
        self._send_assertion_event(
            self.current_user_email,
            self.current_notebook_id,
            self.get_cell_id(),
            assertions_result,
        )
    
    def send_assertion_event_with_num(self, assertions_result, num):
        assert self.is_initialized, (
            f"Must call init() before using send_assertion_event()."
        )
        self._send_assertion_event(
            self.current_user_name,
            self.current_notebook_id,
            num,
            assertions_result,
        )
    
    @staticmethod
    def _send_assertion_event(student_name, notebook_id, cell_id, result):
        post_data = {
            EVENT.STUDENT_NAME: student_name, 
            EVENT.NOTEBOOK_ID: notebook_id,
            EVENT.CELL_ID: cell_id,
            EVENT.ASSERTION_RESULT: result,
        }
        requests.post(ASSERTION_URL, post_data)


    ####################################################################################################
    # Initialization
    ####################################################################################################

    def init(self):
        """
        We don't want to put this in __init__() because it performs network operations and requires 
        user interaction (login to google).
        """
        self.current_user_name = self.get_user_name()
        self.current_notebook_id = self.get_notebook_name()
        self.is_initialized = True