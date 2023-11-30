def create_file(filepath,data):
    with open(filepath, 'x') as file:
        for line in data:
            file.write(line + '\n')
    return file