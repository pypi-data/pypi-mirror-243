import subprocess
from pathlib import PurePath

# TODO: la mejor manera de crear esta funcion, es que no dependa del input de la consola.
location = input("Donde quieres crear ")
file_name = input("Como se llamara el archivo? ")
content = input(""" El contenido del archivo  """)
# TODO: le falta encontrar una manera de recibir el contenido, si lo mandas por la consola, no lo recibe por que en cada salto de linea lo interpreta como un comando.
file = PurePath.joinpath(location,file_name+"txt")

print(file)

subprocess.run(f'cd "{location}" && echo "" {i}',shell=True)