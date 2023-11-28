
# init project
```powershell
$project_name="poetry_template"
$package_name=$($project_name -replace "-","_")
poetry new --src $project_name

echo "__version__ = '0.1.0'" > src/$package_name/__init__.py

poetry config virtualenvs.in-project true --local
poetry config virtualenvs.create true --local
# python -m venv .venv
poetry shell

poetry source add --priority=default tsinghua https://pypi.tuna.tsinghua.edu.cn/simple/
poetry source add --priority=primary aliyun https://mirrors.aliyun.com/pypi/simple/


poetry add python-dotenv
poetry add pytest pytest-mock pytest-cov --group test
poetry add flake8 mypy --group lint
poetry add black isort yapf --group format
poetry add mkdocs --group docs


poetry show --tree
poetry show --tree --only main
poetry show --tree --with test,docs


$testpypi_token="pypi-AgENdGVzdC5weXBpLm9yZwIkYmFlY2E1MTktYmVmZi00MDBiLWEyYzEtMjUwZjczNTU5OWYxAAIqWzMsIjFkZWM0NGY4LTA0YjEtNGI1Yi1iOTVjLTA5ZGE5MjNlZGY3NSJdAAAGIJjjVg8Gkxv7sZyRTo7LxflWIfcGABowByjbbpBzAyG2"
poetry config pypi-token.testpypi "$testpypi_token" --local
poetry config repositories.testpypi https://test.pypi.org/legacy/
poetry config http-basic.testpypi __token__ pypi-AgENdGVzdC5weXBpLm9yZwIkYmFlY2E1MTktYmVmZi00MDBiLWEyYzEtMjUwZjczNTU5OWYxAAIqWzMsIjFkZWM0NGY4LTA0YjEtNGI1Yi1iOTVjLTA5ZGE5MjNlZGY3NSJdAAAGIJjjVg8Gkxv7sZyRTo7LxflWIfcGABowByjbbpBzAyG2
poetry build
poetry publish -r testpypi
poetry publish


```

# use this template
```bash

poetry config virtualenvs.in-project true --local
# python -m venv .venv
poetry shell
poetry install

# pyenv local 3.9.0 && poetry config virtualenvs.in-project true --local && poetry [new | init | install]

# poetry install --with test,docs --without docs
# poetry install --only main
# poetry remove mkdocs --group docs

```
