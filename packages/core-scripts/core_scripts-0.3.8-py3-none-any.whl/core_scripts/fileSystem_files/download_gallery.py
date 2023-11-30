# yisus.py folder_name url_pictures total_pictures format_pictures
# * la funcion de este script, es descargar todas las imagenes de una url, seguiendo una secuencia numerica. 
# TODO: crear una manera que usando solo la url, te permita saber cual es el formato de la imagen y lograr detectar el patron de la imagen ejemplo, si es 1 o 01 o 001. esto se puede lograr con regular exprecion y usando el errorlevel del curl, para verificar el limite de imagenes, que existen.
# TODO: hacer refactorizacion
# TODO: colocar un destination
from subprocess import run
from sys import argv
from os import path
# from termcolor import colored

def clean_scream():
    run('cls',shell=True)

def get_folder_name():
    if(len(argv) == 1):
        folder_name = input("Nombre de la carpeta contenedora de la galeria ")
        return folder_name
    folder_name = argv[1]
    return folder_name

container_folder = get_folder_name()

def create_container_folder():
    run(f'mkdir {container_folder}',shell=True)

def get_user_data():
# TODO: agregar una forma de verificar si la url termina en /, en caso de terminar en / lanzar un error.
    if(len(argv) == 1):
        url_pictures = input("Cual es la url donde estan las imagenes? ")
        total_pictures = int(input("Cuantas imagenes tiene? ")) + 1
        format_pictures = input("Que formato tiene las imagenes? ")
        return list((url_pictures,total_pictures,format_pictures))
    url_pictures = argv[2]
    total_pictures = int(argv[3]) + 1
    format_pictures = argv[4]
    return list((url_pictures,total_pictures,format_pictures))

user_data = get_user_data()


def download_gallery(initial_picture = 1):
    pictures_to_download = range(initial_picture,user_data[1])
    for i in pictures_to_download:
            url = f'{user_data[0]}/{i}.{user_data[2]}'
            run(f'cd {container_folder} && curl -O {url} && echo Galeria: {container_folder} Terminado :: url: {url}',shell=True)  
    clean_scream()

def check_pictures_exist():
    initial_picture = 1
    pictures_to_check = range(initial_picture,user_data[1])
    for i in pictures_to_check:
        if (path.isfile(f'{container_folder}/{i}.{user_data[2]}') == False):
            download_gallery(i)

def download_gallery_process_true():
    create_container_folder()
    download_gallery()

if (path.isdir(container_folder) == False ):
    download_gallery_process_true()
else:   
    print(f"Ya existe: {container_folder}")
    print(f"Verificando Contenido")
    check_pictures_exist()
    
# crear una funcion que se encarge de verificar si existe la carpeta y otra de crearla.