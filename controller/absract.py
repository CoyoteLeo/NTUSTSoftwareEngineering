from abc import ABCMeta, abstractmethod


class BaseController(metaclass=ABCMeta):
    @classmethod
    @abstractmethod
    def setupUrl(cls):
        pass
