def norm_path(path):
    if not path.endswith('/'):
        return path + '/'
    return path
