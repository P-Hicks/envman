import os
import json
import shutil
'''
My windows PC doesn't have make installed, so I use this script instead.
'''

def read_json_file(path):
    with open(path, 'r', encoding='utf8') as file:
        return json.loads(file.read())

os.system('python setup.py build_ext --inplace')
os.system('pyinstaller --onefile env_manager.pyx')
# settings.json:
# {
#     "src":...,
#     "dest":...
# }
settings = read_json_file('settings.json')
shutil.copy(
    src=settings['src'],
    dst=settings['dest'],
)