
# links and makes executable at dist/env_manager
executable: env_manager.c
	pyinstaller --onefile env_manager.pyx

# compiles to c
env_manager.c: env_manager.pyx
	python setup.py build_ext --inplace

# Creates correct filename, but allows original file to be python for syntax highlighting purposes
env_manager.pyx: env_manager.py
	ln -s env_manager.py env_manager.pyx

# .PHONY: pipenv virtual_environment init test server database chronjob
