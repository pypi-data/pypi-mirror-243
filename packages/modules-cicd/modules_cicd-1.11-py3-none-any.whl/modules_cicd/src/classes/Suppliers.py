from ..interfaces.CICDService import CICDInterface
from ..service.src.Interfaces.interfaces import BaseInterface


class RepoCICD(CICDInterface):
    def __init__(self, providerClass: BaseInterface):
        self.Service = providerClass

    def add_cicd_to_repository(self):
        try:
            project = self.Service.CreateProject()
            return project
        except Exception as err:
            raise Exception(f"Error creating repository CICD: {err}")

    def update_cicd_in_repository(self):
        try:
            project = self.Service.UpdateProject()
            return project
        except Exception as err:
            raise Exception(f"Error updating repository CICD: {err}")

    def delete_cicd_from_repository(self):
        try:
            project = self.Service.DeleteProject()
            return project
        except Exception as err:
            raise Exception(f"Error removing CICD from repository: {err}")
