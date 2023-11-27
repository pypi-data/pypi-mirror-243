from sqlite3 import connect
from os import system
from psutil import process_iter
from getpass import getuser
from pathlib import Path

class Browser:
# TODO: transformar mucho de las funciones estaticas a funciones normales. solo dejar las que sean estrictamente.
    username = getuser()
    profiles = []
    def __init__(self,history_folder,history_query,history_file,browser_process_name):
        self.history_folder = history_folder
        self.history_query = history_query
        self.history_file = history_file
        self.browser_process_name = browser_process_name
    @staticmethod
    def make_query_sqlite3(path_to_history, query):
    # crea querys a la base de datos sqlite3, del navegador
        connect_ = connect(path_to_history)
        cursor_ = connect_.cursor()
        cursor_.execute(query)
        result = cursor_.fetchall()
        return result
    @staticmethod
    def history_to_dictionary(historys, browser, profile):
    # tansforma un historial en un objeto
        history_holder = []
        for history in historys:
        # TODO:  se puede crear un objeto, usando un array?
            history_holder.append({"url": history[0], "title": history[1],
                              "visit_count": history[2], "timestamp": history[3], "browser": browser, "profile": profile})
        return history_holder
    @staticmethod
    def close_browser(browser_process):
    # cierra el navegador para realizar operaciones en el archivo history
        if browser_process in (p.name() for p in process_iter()):
            system(f"taskkill /im {browser_process} /f")
    @staticmethod
    def create_json_file(path_to_create, historys):
    # crea el archivo json con el historial
    # usar la fecha para verificar si existen las carpetas contenedoras - ano y mes
    # verificar si ya existe el archivo
    # si ya existe tomar la informacion y fucionarla con la nueva
    # si no existe crear el archivo
        with open(path_to_create, "w") as file:
            file.write(historys)
    @classmethod
    def get_all_colums(cls,table_name,path_to_history):
    # obtiene todas las columnas de un archivo sqlite
        query = f"PRAGMA table_info({table_name})"
        return cls.make_query_sqlite3(path_to_history,query)
    @classmethod
    def get_all_tables(cls,path_to_history):
    # obtiene todas las tablas de un archivo sqlite
        query = "SELECT name FROM sqlite_master WHERE type='table'"
        return cls.make_query_sqlite3(path_to_history,query)
    @staticmethod
    def check_exist_profile(path_to_history_folder):
    # verifica si existe la carpeta con el perfil
        history_folder = Path(path_to_history_folder)
        if history_folder.is_dir():
            return True
        return False
    @staticmethod
    def check_exist_history_file(path_to_history_file):
    # verifica si existe el archivo con el historial
        history_file = Path(path_to_history_file)
        if history_file.is_file():
            return True
        return False
    
    def create_profile_path(self,profiles_names):
    # crea una lista de rutas a los perfiles de los navegadores.
        full_path = ""
        for names in profiles_names:
            full_path = f"{self.history_folder}/{names}"
            self.profiles.append(full_path)
        return True
    