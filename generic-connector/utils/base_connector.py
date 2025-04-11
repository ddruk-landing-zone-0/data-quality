from abc import ABC, abstractmethod

class BaseConnector(ABC):
    @abstractmethod
    def connect(self, username, password, database, host, port):
        pass

    @abstractmethod
    def execute_and_return_result(self, query):
        pass
