from os import listdir
from os.path import basename,normpath,isdir


def take_first_name_same(pathFolder,fileType = "image"):
    """
        Agarra el primer elemento en una carpeta puede ser un archivo o una carpeta, lo copia fuera de la carpeta y lo renombra con el mismo nombre de la carpeta.
    """
    if fileType == "image":
        pass
    #agarrar el primer archivo y copiarlo
    #pegalo en la ruta donde se encuentra el pathFolder
    #renombrarlo con el nombre del folder del pathFolder

take_first_name_same('C:/Users/worf_/Desktop/test/01')