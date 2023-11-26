from abc import ABC, abstractmethod

from ..classes.dataClass import Repository, TypeProjectTemplate


class RepoInterface(ABC):
    @abstractmethod
    def create_repository(self, data: Repository):
        pass

    @abstractmethod
    def update_repository(self, data: Repository):
        pass

    @abstractmethod
    def delete_repository(self, data: Repository):
        pass

    @abstractmethod
    def get_repository(self, data: Repository):
        pass

    @abstractmethod
    def clone_template(self, data: Repository):
        pass
