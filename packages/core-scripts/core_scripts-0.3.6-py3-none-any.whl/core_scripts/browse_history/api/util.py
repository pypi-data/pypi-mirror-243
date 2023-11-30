from os import system
from psutil import process_iter
from sqlite3 import connect
from json import dumps, loads
from vars import chrome_query

# crea querys a la base de datos sqlite3, del navegador


def make_query_sqlite3(path_to_history, query):
    connect_ = connect(path_to_history)
    cursor_ = connect_.cursor()
    cursor_.execute(query)
    result = cursor_.fetchall()
    return result

# optiene el historial de un navegador


def get_chrome_browser_history(path_to_history):
    result = make_query_sqlite3(path_to_history, chrome_query)
    return result  # regresa una lista de tuples

# ansforma un historial en un objeto


def history_to_dictionary(historys, browser):
    # ! aqui existe un pequeno problema, se quiere usar los historys de todos los navegadores, pero es muy probable, que no todos tengan los mismos campos, asi que eso la puede complicar un poco.
    history_holder = []
    for history in historys:
        # TODO:  se puede crear un objeto, usando un array?
        history_holder.append({"url": history[0], "title": history[1],
                              "visit_count": history[2], "timestamp": history[3], "browser": browser})
    return history_holder

# transforma un historial en formato json


def history_to_string(historys):
    history_string = dumps(historys)
    return history_string

# cerramos gogle chrome para poder borrar el historial de


def close_chrome_open():
    if "chrome.exe" in (p.name() for p in process_iter()):
        system("taskkill /im chrome.exe /f")

# crea el archivo json con el historial


def create_json_file(path_to_create, historys):
    # usar la fecha para verificar si existen las carpetas contenedoras - ano y mes
    # verificar si ya existe el archivo
    # si ya existe tomar la informacion y fucionarla con la nueva
    # si no existe crear el archivo
    with open(path_to_create, "w") as file:
        file.write(historys)
