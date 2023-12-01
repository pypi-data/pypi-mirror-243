# Deploy aurori


install requirements: `pip install -r .\requirements.build.txt`
build with: `python -m build`
deploy with: `python -m twine upload .\dist\aurori-1.1.1*` (replace the version)
