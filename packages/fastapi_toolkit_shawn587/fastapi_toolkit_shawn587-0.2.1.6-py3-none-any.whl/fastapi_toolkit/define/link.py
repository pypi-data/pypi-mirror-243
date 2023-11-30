from abc import ABC, abstractmethod
from typing import Tuple, Type


class Link(ABC):
    @abstractmethod
    def two_sides(self) -> Tuple[str, str]:
        pass


class OneManyLink(Link):
    """
    OneManyLink is a link between one object and many objects.
    Must set in one side.
    """

    def __init__(self, one: str, many: str):
        self.one = one
        self.many = many

    def two_sides(self) -> Tuple[str, str]:
        return self.one, self.many


class ManyManyLink(Link):
    """
    ManyManyLink is a link between many objects and many objects.
    Just could set in one side.
    """

    # TODO: data_model should be a optional param
    def __init__(self, left, right, data_model):
        self.left = left
        self.right = right
        self.data_model = data_model

    def two_sides(self) -> Tuple[str, str]:
        return self.left, self.right


class UserManyLink(ManyManyLink):
    def __init__(self, right, data_model):
        super().__init__('User', right, data_model)
