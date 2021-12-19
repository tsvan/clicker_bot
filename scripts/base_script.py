from abc import ABC, abstractmethod


class BaseScript(ABC):
    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def before_start(self):
        pass

    @abstractmethod
    def after_stop(self):
        pass
