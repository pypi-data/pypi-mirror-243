@echo off
if not exist distbackup (mkdir distbackup)
move /y dist\*.*  distbackup
rmdir /s /q dist
py -m pip install --upgrade pip
py -m pip install --upgrade build
py -m pip install --upgrade twine
py -m build   
py -m twine upload --config-file "c://pypi//.pypirc" --repository EventHandler_edog0049a dist/*

