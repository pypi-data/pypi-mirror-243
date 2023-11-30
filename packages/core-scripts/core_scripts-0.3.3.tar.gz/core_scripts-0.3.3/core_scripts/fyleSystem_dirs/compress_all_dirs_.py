from sys import argv
from compress_only_dirs import compress_only_dirs

destination = False

if (len(argv) > 1):
    destination = argv[1]
else:
    # TODO: poner un mejor input
    destination = input("Donde estan las carpetas para comprimir ")

compress_only_dirs(destination)