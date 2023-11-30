from os import listdir
from os.path import normpath,isdir,join
from natsort import natsorted #cSpell:disable-line

def take_first_file_folder(pathFolder):
    """
    Agarra solo el primer archivo de una carpeta.
    """
    pathFolder_ = normpath(pathFolder)
    filesInFolder = listdir(pathFolder_)
    orderedFilesInFolder = natsorted(filesInFolder) #cSpell:disable-line
    # FIXME: creo que en el caso de orderedFilesInFolderWithPath no es necesario que sea una lista, es mejor que sea una string
    orderedFilesInFolderWithPath = []
    firstFileInFolder = ""
    for file in orderedFilesInFolder:
        orderedFilesInFolderWithPath = join(pathFolder_,file)
        if isdir(orderedFilesInFolderWithPath):
            continue
        firstFileInFolder = orderedFilesInFolderWithPath
        break
    return firstFileInFolder