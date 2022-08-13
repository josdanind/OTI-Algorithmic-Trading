from colorama import Fore, init
import json

HOST = "localhost"
PORT = 80
URL = f"http://{HOST}:{PORT}/api/v1"


def read_json(path):
    with open(path, "r", encoding="utf-8") as file:
        jwt = json.loads(file.read())
        return jwt


init(autoreset=True)


def print_dict(dict_data):
    for k, v in dict_data.items():
        if type(v) == str:
            print(Fore.YELLOW + f"{k}:", Fore.RED + v)
        if type(v) == dict:
            print_dict(v)
