import os.path

HERE = os.path.dirname(__file__)

def get_key(filename=None):
    """
    Grab the key from the super-secret location
    :return:
    """

    filename = filename or '{}/../../secret_key.txt'.format(HERE)

    with open(filename, 'r') as f:
        key = f.read()

    return key
