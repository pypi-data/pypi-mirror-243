import getpass
from os.path import abspath,basename,dirname
from inspect import getsourcefile
from api.Chrome import Chrome

# obtiene el username del sistema
username = getpass.getuser()
history_folder = f"C:/Users/{username}/AppData/Local/Google/Chrome/User Data/Default"

""" history_file = f"History"
history_path = f"{history_folder}/{history_file}"
destination_history_path = dirname(__file__)+"\example.json" """
""" print(__file__)
print(os.getcwd())
print(basename(__file__))
print(dirname(__file__)) """

chrome = Chrome()

chrome.close_chrome()
"""
* crear el nombre de los posibles perfiles, esto es personal para cada navegador. Algunos navegadores ni perfiles tienen otros, se llaman diferente en cada pc. puede ser una funcion estatica ya que no necesita ningun componente interno de la clase.
* verificar si existen los perfiles
* crear la ruta completa con los perfiles que si existen
* usando la lista con los perfiles, extraer el historial de cada uno
* verificar si esta vacio el historial.
* si esta vacio lo descarta si no lo une.
* a la final la idea seria tener un objeto con todos los historiales.
* luego crear los archivos json
    * colocandolos en la carpeta del ano y mes correspondiente
    * luego el dia y la hora correspondiente, de menor a mayor.
"""

close_chrome_open()
chrome_history = get_chrome_browser_history(history_path)
# TODO: crear un extrarttor de history para todos los navegadores
# TODO: crear una funcion que los fucione a todos en un solo objeto.
chrome_historys_dictionary = history_to_dictionary(chrome_history,"chrome")
chrome_historys_string = history_to_string(chrome_historys_dictionary)
create_json_file(destination_history_path,chrome_historys_string) 

""" if os.path.isdir(history_folder) == False:

    exit() """




# verificamos que existe la carpeta donde esta el historial.
# verificamos si existe el archivo donde esta el historial.
    # en ambos cosos si no existe, podemos crear un log que muestre el resultado de la ultima ejecucion.
