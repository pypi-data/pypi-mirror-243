from typing import TypeVar, Generic

T = TypeVar('T')


class Singleton(Generic[T]):
    def __init__(self, decorated):
        self._decorated: T = decorated

    def get_instance(self) -> T:
        """
                Returns the singleton instance. Upon its first call, it creates a
                new instance of the decorated class and calls its `__init__` method.
                On all subsequent calls, the already created instance is returned.

                """
        try:
            return self._instance
        except AttributeError:
            self._instance: T = self._decorated()
            return self._instance

    @property
    def shared(self) -> T:
        return self.get_instance()

    @property
    def instance(self) -> T:
        return self.get_instance()

    @property
    def singleton(self) -> T:
        return self.get_instance()

    def __call__(self):
        raise TypeError('Singletons must be accessed through `instance()`.')
