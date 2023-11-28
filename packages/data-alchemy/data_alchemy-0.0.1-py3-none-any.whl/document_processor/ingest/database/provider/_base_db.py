import abc
from typing import List

from .models import DatabaseConnectionConfig


class BaseDB(abc.ABC):
    db_connection_config = None
    client = None

    def __init__(self, db_connection_config: DatabaseConnectionConfig) -> None:
        self.db_connection_config = db_connection_config

    @abc.abstractmethod
    def insert(self, data: dict) -> str:
        pass

    @abc.abstractmethod
    def insert_many(self, data: List[dict]) -> List[str]:
        pass

    @abc.abstractmethod
    def update(self, document_id: str, data: dict):
        pass

    @abc.abstractmethod
    def delete(self, document_id: str):
        pass

    @abc.abstractmethod
    def get(self, document_id: str):
        pass

    @abc.abstractmethod
    def list_all(self, query: dict = None, limit: int = 100):
        pass

    @abc.abstractmethod
    def exists(self, filters: dict):
        pass
