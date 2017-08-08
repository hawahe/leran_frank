

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


DATABASE = {
    'engine': 'file_storage', #support mysql, postgresql in the future
    'name': 'accounts'
    'path': "%s/db" % BASE_DIR

}

