from .fileSystem_files import (
    create_yaml,
    create_file,
    get_extension,
    check_extension
)

# TODO: ver si funciona
def name_main(name):
    """
    Verifica si el script fue ejecutado localmente o fue importado.
    """
    if name == "__main__":
        return True
    return False