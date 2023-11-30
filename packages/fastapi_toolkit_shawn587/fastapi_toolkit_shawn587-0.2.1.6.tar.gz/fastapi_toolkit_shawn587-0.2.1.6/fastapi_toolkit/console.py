import importlib
import importlib.util as import_utils
import os
from pathlib import Path

import typer

from fastapi_toolkit.generate import CodeGenerator

app = typer.Typer()

tk_root = Path('.fastapi-toolkit')


def add_path_to_gitignore(path: Path):
    gitignore_path = Path('.gitignore')
    if not gitignore_path.exists():
        with open(gitignore_path, 'w') as f:
            f.write(f'{path}\n')
    else:
        with open(gitignore_path, 'r') as f:
            lines = f.readlines()
        if path.name not in lines:
            with open(gitignore_path, 'a') as f:
                f.write(f'{path}\n')


def import_module(module_name, module_path):
    spec = import_utils.spec_from_file_location(module_name, module_path)
    module = import_utils.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@app.command('i')
@app.command('init')
def init():
    os.mkdir(tk_root)
    add_path_to_gitignore(tk_root)


@app.command('g')
@app.command('generate')
def generate(metadata_path: Path = 'metadata', root_path: Path = 'inner_code',
             table: bool = True, router: bool = True, mock: bool = True, auth: bool = True):
    if not root_path.is_dir():
        typer.confirm(f'root_path: {root_path} is not a dir, do you want to create it?', abort=True)
        root_path.mkdir(parents=True)
    module_name = "models"
    import_module(module_name, metadata_path.joinpath(f'{module_name}.py'))
    generator = CodeGenerator(root_path)
    generator.parse_models()
    if table:
        generator.generate_tables()
    if router:
        generator.generate_routers()
    if mock:
        generator.generate_mock()
    if auth:
        generator.generate_auth()


@app.command('mock')
@app.command('m')
def mock(root_path: Path = 'inner_code'):
    main = importlib.import_module(str(root_path).replace('\\', '.') + '.mock').main
    main()


db_app = typer.Typer()


def get_dev_db(root_path: Path):
    module_path = root_path.joinpath('dev').joinpath(f'db.py')
    return import_module('db', module_path)


@db_app.command('init')
@db_app.command('i')
def db_init(root_path: Path = 'inner_code'):
    init = get_dev_db(root_path).init
    init(str(root_path).replace('\\', '.'))


@db_app.command('migrate')
@db_app.command('m')
def db_migrate(root_path: Path = 'inner_code', msg: str = None):
    migrate = get_dev_db(root_path).migrate
    migrate(msg)
    print('must add "import fastapi_users_db_sqlalchemy" to migrate script')


@db_app.command('upgrade')
@db_app.command('u')
def db_upgrade(root_path: Path = 'inner_code'):
    upgrade = get_dev_db(root_path).upgrade
    upgrade()


app.add_typer(db_app, name="db")
