"""
General utils
"""
import string
import random
import os
from datetime import datetime

INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')

def get_current_time():
    """
    return the current time
    """
    return datetime.utcnow()

def id_generator(size=10, chars=string.ascii_letters+string.digits):
    """
    Return a random id
    """
    return ''.join(random.choice(chars) for x in range(size))

def make_dir(dir_path):
    """
    create the given directory if not exists
    """
    try:
        if not os.path.exists(dir_path):
            os.mkdir(dir_path)
    except Exception as e:
        raise e
