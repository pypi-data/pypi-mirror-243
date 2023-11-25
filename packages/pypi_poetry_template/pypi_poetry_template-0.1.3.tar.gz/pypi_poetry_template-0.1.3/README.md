# pypi_poetry_template
a template for build python package to upload pypi repository bu using poetry

```bash

poetry init

poetry env use python

poetry add python-dotenv
poetry add pytest pytest-mock --group test
poetry add flake8 pylint mypy --group lint
poetry add black isort yapf --group format
poetry add mkdocs --group docs


poetry install --with test,docs --without docs
poetry install --only main
poetry remove mkdocs --group docs



poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry build
poetry publish -r testpypi
poetry publish

```


# References:
- [publishing-a-package-to-pypi-with-poetry](https://www.ianwootten.co.uk/2020/10/20/publishing-a-package-to-pypi-with-poetry/)
