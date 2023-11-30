#cSpell:disable
from os import listdir,mkdir
from os.path import isfile,join,normpath
from .get_extension import get_extension
from core_scripts.string.group_similar_strings import group_similar_strings
from shutil import move

def group_similarFiles_inSequenceFolders(
        files_path,
        files_format,
        sequence_startup,
        differences_number
        ):
    """
        Group similar files and put them in a numeric sequency of folders.
    """
        #TODO: refactorizar los argumentos
    # * optener los archivos del path
    #   * Solo los archivos y solo los que tengan el files_format
    files = listdir(files_path)
    files_with_path = []
    only_desired_files = []
    for file in files:
        # TODO: Esta podria ser una funcion aparte, join_files_path
        files_with_path.append(join(files_path,file))
    for file in files_with_path:
        # TODO: Esta podria ser una funcion aparte
        file_format = extract_format_file(file,options={"noDot": True})
        if (isfile(file) and file_format == files_format):
            # TODO: crear una operacion en caso de que files_format sea un array.
            only_desired_files.append(file)
    # * agruparlos
    grouped_files = group_similar_strings(only_desired_files,differences_number)
    # * crear la carpeta y colocar los archivos en ella.
    sequence_startup__ = str(sequence_startup)
    sequence_continue = sequence_startup
    for group_files in grouped_files:
        group_files_index = grouped_files.index(group_files)
        if (group_files_index == 0):
            dir_path = join(files_path,sequence_startup__)
            mkdir(dir_path)
            for files in group_files:
                move(files,dir_path)
            continue
        sequence_continue = sequence_continue + 1
        sequence_continue__ = str(sequence_continue)
        dir_path = join(files_path,sequence_continue__)
        mkdir(dir_path)
        for files in group_files:
            move(files,dir_path)
    

group_similar_files_folder("E:\\static\\porn\\AshMcKn p2\\Ashleigh McKenzie p2","jpg",13,4)