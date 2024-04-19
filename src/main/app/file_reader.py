import pickle


def read_file(path: str):
    with open(path, 'rb') as f:
        return f.read()


def read_file_by_pickle(path: str):
    with open(path, 'rb') as f:
        return pickle.load(f)
