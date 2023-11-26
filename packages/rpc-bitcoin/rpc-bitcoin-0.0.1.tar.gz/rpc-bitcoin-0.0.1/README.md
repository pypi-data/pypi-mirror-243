## Build package

`build` is needed to build the package, you can install it with:
```shell
pip install build
```

Then for build the package just run:
```shell
python3 -m build
```

packages will be in `dist/` folder

## upload on pypi

Just run:
```shell
python3 -m twine upload dist/*
```

If you want to upload on the test repository of pypi:
```shell
python3 -m twine  upload --repository testpypi dist/*
```