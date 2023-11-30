from take_first_image_folder import take_first_image_folder
from extract_format_file import extract_format_file
from shutil import copyfile
from os.path import dirname,normpath,basename,join


def take_copy_rename_(filePath):
    pathFolder = dirname(filePath)
    originFolderName = basename(pathFolder)
    fileFormat = extract_format_file(filePath)
    destinationFolder = dirname(pathFolder)
    renamedFile = originFolderName+fileFormat
    destination = join(destinationFolder,renamedFile)
    destination = normpath(destination)
    return copyfile(filePath,destination)

def take_first_file_name_same(pathFolder,fileType = "image"):
    """
        Agarra el primer archivo, lo copia fuera de la carpeta y lo renombra con el mismo nombre de la carpeta.
        Valores para fileType: image,music,video,text. TODO: Faltan mas tipos de archivos.
    """
    # TODO: verificar que pathFolder sea una carpeta
    # TODO: verificar si el archivo que vas a copiar ya existe.
    curatedPathFolder = normpath(pathFolder)
    filePath = ""
    if fileType == "image":
        filePath = take_first_image_folder(curatedPathFolder)
        return take_copy_rename_(filePath)
    return False