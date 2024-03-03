def read_file(path: str):
    with open(path, 'rb') as f:
        return f.read()
