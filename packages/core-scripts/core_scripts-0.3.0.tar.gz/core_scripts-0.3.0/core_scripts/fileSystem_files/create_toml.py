from toml import dump

def create_toml(filepath,data):
    with open(filepath, 'x') as f:
        created_toml_file = dump(data, f)
    return created_toml_file