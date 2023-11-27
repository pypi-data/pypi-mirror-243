from os.path import splitext


def check_extension_list_(fileExtencion,fileFormat):
    for extencion in fileFormat:
        if(extencion == fileExtencion):
            return True
    return False
    

def check_extension_string_(fileExtencion,fileFormat):
    if (fileFormat == fileExtencion):
        return True
    return False

def check_extension(file,fileExtension):
    """
        Verificara el formato de un archivo. Devuelve True si el file coincide con el fileFormat
    """
    # TODO: usar extract_format_file
    fileExtencion = splitext(file)[1].partition(".")[2]
    if (isinstance(fileExtension,list)):
        return check_extension_list_(fileExtencion,fileExtension)
    return check_extension_string_(fileExtencion,fileExtension)