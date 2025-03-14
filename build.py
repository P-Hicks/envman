import os

'''
My windows PC doesn't have make installed, so I use this script instead.
'''

os.system('python setup.py build_ext --inplace')
os.system('pyinstaller --onefile env_manager.pyx')