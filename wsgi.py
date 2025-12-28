import sys
import os

path = '/home/sduapp/SduSuperApp/SduSuperApp'
if path not in sys.path:
    sys.path.append(path)

os.chdir(path)

from app import create_app
application = create_app('production')
