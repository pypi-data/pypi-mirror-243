from take_first_file_name_same import take_first_file_name_same
from os import listdir
from os.path import normpath,join,isfile
from natsort import natsorted


def take_all_file_name_same(pathFolder,fileType = "image"):
    """
        Agarra todos los primeros archivos, de todas las carpetas de una ruta dada, los va a copiar y renombrar en la ruta dada.
    """
    # TODO: verificar si pathFolder es una carpeta.
    curatedPathFolder = normpath(pathFolder)
    # se listaran todos los archivos de la ruta.
    allFiles = listdir(curatedPathFolder)
    allFiles = natsorted(allFiles)
    allFilesWithPath = ""
    # se filtraran solo las carpetas
    for file in allFiles:
        allFilesWithPath = join(pathFolder,file)
        allFilesWithPath = normpath(allFilesWithPath)
        if (isfile(allFilesWithPath)):
            continue
        take_first_file_name_same(allFilesWithPath,fileType)

    # y se aplicara la operacion en las carpetas.

take_all_file_name_same("C:\\Users\\worf_\\Desktop\\test")

