import sys
import os

project = "keepmealive"

BASE_DIR = os.path.join(os.path.dirname(__file__))

if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from keepmealive import create_app
application = create_app()
