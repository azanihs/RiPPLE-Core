import os
from dotenv import load_dotenv
from collections import OrderedDict

DEFAULT_ENVS = OrderedDict([
    ['DEVELOPMENT_ENVIRONMENT', 'DEVELOPMENT'],
    ['DJANGO_KEY', 'UNIQUE_LONG_STRING'],
    ['PROXY_LOCATION', ''],
    ['LTI_SUCCESS_REDIRECT', 'http://localhost:8080'],
    ['LTI_URL', ''],
    ['LTI_APP_KEY', ''],
    ['DATABASE_TYPE', 'sqlite3'],
    ['DATABASE_NAME', 'rippledb'],
    ['DATABASE_HOST', 'localhost'],
    ['DATABASE_USER', 'ripple'],
    ['DATABASE_PASSWORD', 'password']
])


def init_env(try_path):
    dotenv_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), try_path))
    if not os.path.isfile(dotenv_path):
        print("Could not load " + dotenv_path + "!")
        print("Would you like to initialise .env.current to example values? (Y/N)")
        user_answer = input("> ")
        if user_answer == "Y":
            with open(dotenv_path, "w") as config_file:
                for key, value in DEFAULT_ENVS.items():
                    config_file.write(key + "=" + value + "\n")
        else:
            raise ImportError(
                "Could not load application config. Please ensure you have an active development environment")
    load_dotenv(dotenv_path, verbose=True)
