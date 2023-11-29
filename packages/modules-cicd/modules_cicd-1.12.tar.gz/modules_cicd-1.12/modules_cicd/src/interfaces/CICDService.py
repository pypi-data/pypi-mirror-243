from abc import ABC, abstractmethod

from ..classes.TypeProjectEnum import TypeProject


class CICDInterface(ABC):
    @abstractmethod
    def add_cicd_to_repository(repository_name: str, project: TypeProject):
        pass

    @abstractmethod
    def update_cicd_in_repository(repository_name: str, project: TypeProject):
        pass

    @abstractmethod
    def delete_cicd_from_repository(repository_name: str, project_name: str):
        pass
