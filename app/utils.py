
from functools import partial


class ReloadingIterator:
    def __init__(self, iterator_factory):
        self.iterator_factory = iterator_factory

    def __iter__(self):
        return self.iterator_factory()


class DynamicOptionsMixin:
    def get_dynamic_options(self, view):
        raise NotImplementedError

    def get_options(self, view):
        return ReloadingIterator(partial(self.get_dynamic_options, view))