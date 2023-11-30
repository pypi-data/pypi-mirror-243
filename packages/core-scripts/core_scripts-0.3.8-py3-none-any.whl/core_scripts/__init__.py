from .fileSystem_files import fileSystem_files

# TODO: ver si funciona
def name_main(name):
    """
    Verifica si el script fue ejecutado localmente o fue importado.
    """
    if name == "__main__":
        return True
    return False