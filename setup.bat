IF EXIST dist (rmdir dist /s /q)
py setup.py sdist
py -m twine upload --repository testpypi dist/*
rmdir dist /s /q
rmdir regex_build.egg-info /s /q
PAUSE