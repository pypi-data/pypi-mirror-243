import uuid
import datetime
import inspect
from typing import Type, TypeVar, Tuple, List, Optional, Dict, Union

from sqlalchemy.sql import sqltypes

from fastapi_toolkit.generate.mock import MockMetadata, MockType
from fastapi_toolkit.define.link import Link


class BaseModel:
    def __init_subclass__(cls, **kwargs):
        register_model(cls)


class UserModel:
    def __init_subclass__(cls, **kwargs):
        register_model(cls, is_user=True)


class DataModel:
    """
    Define only the data model without generating the corresponding tables and their routes
    """

    def __init_subclass__(cls, **kwargs):
        register_model(cls, just_data=True)


def get_type_str(type) -> str:
    mod = inspect.getmodule(type)
    if mod is None:
        if type.__name__ == 'now':
            return 'datetime.datetime.now'
        raise TypeError("unknown type")
    mod = mod.__name__ + '.'
    if mod == 'builtins.':
        mod = ''
    if isinstance(type, sqltypes.String):
        return mod + f'String({type.length})'
    return mod + type.__name__


class Field:
    def __init__(self,
                 python_type,
                 sql_type,
                 primary_key: bool = False,
                 optional: bool = False,
                 default=None,
                 default_factory=None,
                 mock: Optional[MockMetadata] = None):
        self.python_type = python_type
        self.python_type_str = get_type_str(python_type)
        self.sql_type = sql_type
        self.sql_type_str = get_type_str(sql_type)
        self.primary_key = primary_key
        self.optional = optional
        if mock:
            self.mock = mock
        else:
            if python_type is int:
                self.mock = (MockType.int, (0, 100))
            elif python_type is float:
                self.mock = (MockType.float, (0, 100, 2))
            elif python_type is bool:
                self.mock = (MockType.bool, None)
            elif python_type is str:
                self.mock = (MockType.str, 10)
            elif python_type is uuid.UUID:
                self.mock = (MockType.uuid, None)
            elif python_type is datetime.datetime:
                self.mock = (MockType.datetime, None)
            else:
                self.mock = (MockType.str, 10)
        mock_type, mock_args = self.mock
        mock_func = f'mock_{mock_type.name}'
        if mock_args is not None:
            if isinstance(mock_args, tuple):
                mock_args = ', '.join([str(arg) for arg in mock_args])
            else:
                mock_args = str(mock_args)
            mock_args = f'{mock_args}'
        else:
            mock_args = ''
        self.mock = (mock_func, mock_args)
        assert not (default and default_factory), 'default and default_factory can not both exist'
        if default is not None:
            self.default = default
            self.default_str = str(default)
        if default_factory is not None:
            self.default_factory = default_factory
            self.default_factory_str = get_type_str(default_factory)


T = TypeVar('T', bound=Union[BaseModel, UserModel, DataModel])


def register_model(model: Type[T], is_user=False, just_data=False):
    info = ModelInfo(is_user, just_data)
    info.model = model
    for name, field in model.__dict__.items():
        if isinstance(field, Field):
            info.fields.append({'name': name, 'field': field})
    if is_user:
        import sqlalchemy
        info.fields.append({'name': 'id', 'field': Field(uuid.UUID, sqlalchemy.UUID, primary_key=True)})
    if hasattr(model, 'TKConfig'):
        config = model.TKConfig
        if hasattr(config, 'title'):
            info.title = config.title
        if hasattr(config, 'links'):
            info.links = config.links
            ModelManager.links.extend(config.links)
    ModelManager.models[model.__name__] = info


class ModelInfo:
    model: Type[T]
    fields: List[Dict[str, Field]]
    title: str = ''
    links: List[Link]
    is_user: bool
    just_data: bool

    def __init__(self, is_user: bool = False, just_data: bool = False):
        self.fields = []
        self.links = []
        self.is_user = is_user
        self.just_data = just_data


class ModelManager:
    models: Dict[str, ModelInfo] = {}
    links = []

    @staticmethod
    def _dont_appear_in_child(target: str, link: Link, chain: Optional[List[str]] = None) -> Tuple[bool, List]:
        if chain is None:
            chain = []
        _, nex = link.two_sides()
        chain.append(nex)
        if nex == target:
            return False, chain
        else:
            links = [l for l in ModelManager.links if nex == l.two_sides()[0]]
            for l in links:
                val, chain_ = ModelManager._dont_appear_in_child(target, l, chain.copy())
                if not val:
                    return False, chain_
            return True, []

    @staticmethod
    def check_links():
        # check link target is exist
        for link in ModelManager.links:
            a, b = link.two_sides()
            if a not in ModelManager.models:
                raise Exception(f"link's {a} not exist")
            if b not in ModelManager.models:
                raise Exception(f"link's {b} not exist")

        # check for circular links
        for link in ModelManager.links:
            a, b = link.two_sides()
            val, chain = ModelManager._dont_appear_in_child(a, link, [a])
            if not val:
                raise Exception(f"has circular links: {chain}")
