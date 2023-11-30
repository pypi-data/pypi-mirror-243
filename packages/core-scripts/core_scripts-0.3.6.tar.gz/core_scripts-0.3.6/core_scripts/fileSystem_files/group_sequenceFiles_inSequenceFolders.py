#cSpell:disable
from os import listdir,mkdir
from os.path import isfile,join,normpath,splitext
from .get_extension import get_extension
from core_scripts.string.group_sequence_strings import group_sequence_strings
from shutil import move

#TODO: refactorizar
def group_sequenceFiles_inSequenceFolders(
        files_path,
        files_format, # TODO: crear un proceso para lidiar con arrays TODO: revisar si tiene punto, si tiene eliminarlo.
        sequence_startup
        ):
    """
        Group file sequences and put them in a numeric sequency of folders.
    """
    files = listdir(files_path)
    files_with_path = []
    only_desired_files = []
    only_desired_files_no_format = []
    grouped_files = []
    # * optener los archivos del path
    #   * Solo los archivos y solo los que tengan el files_format
    for file in files:
        # TODO: Esta podria ser una funcion aparte, join_files_path
        files_with_path.append(join(files_path,file))
    for file in files_with_path:
        # TODO: Esta podria ser una funcion aparte
        file_format = get_extension(file,options={"noDot": True})
        if (isfile(file) and file_format == files_format):
            # TODO: crear una operacion en caso de que files_format sea un array.
            only_desired_files.append(file)
    # * agruparlos
    for file in only_desired_files:
        file_no_format= splitext(file)[0]
        only_desired_files_no_format.append(file_no_format)
    grouped_files_no_format = group_sequence_strings(only_desired_files_no_format)
    for group in grouped_files_no_format:
        group_index = grouped_files_no_format.index(group)
        grouped_files.append([])
        for file in group:
            file = f"{file}.{files_format}"
            grouped_files[group_index].append(file)
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
