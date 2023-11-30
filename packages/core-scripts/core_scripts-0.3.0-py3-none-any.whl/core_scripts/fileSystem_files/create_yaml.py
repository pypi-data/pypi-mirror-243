from yaml import dump 

def create_yaml(pathFile,data):
  #TODO: opcion que la ruta no tenga extencion, agregarlo automaticamente.
  with open(pathFile, 'x', encoding='utf8') as outfile:
      return dump(data, outfile, default_flow_style=False, allow_unicode=True)
