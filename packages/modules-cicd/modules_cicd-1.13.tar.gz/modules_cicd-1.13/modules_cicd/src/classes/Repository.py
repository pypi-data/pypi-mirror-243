import time
import json
from ..interfaces.Repository import RepoInterface
from ..service.src.Interfaces.git import RepoAPI
from .dataClass import Repository, TypeProjectTemplate


class Repo(RepoInterface):
    def __init__(
        self,
        repositoryClass: RepoAPI,
        dataRepo: Repository = None,
        cloneRepo: TypeProjectTemplate = None,
    ):
        self.Service = repositoryClass
        self.data = dataRepo
        self.cloneData = cloneRepo


    def create_repository(self):
        try:
            repo = self.Service.create_repo(self.data.name)
            time.sleep(5)
            if len(self.data.users) > 0:
                for id in self.data.users:
                    self.Service.add_users_to_repo(repo.id, id)
            return repo.id
        except Exception as err:
            raise Exception(f"Error creating repository: {err}")    


    def update_repository(self):
        try:
            if(self.data.new_name_repo):
                repo = self.Service.update_repo(self.data.name, self.data.new_name_repo,
                                                self.data.new_description)
            if len(self.data.users) > 0:
                for id in self.data.users:
                    self.Service.add_users_to_repo(self.data.name, id)

            if len(self.data.users_del) > 0:
                for id in self.data.users_del:
                    self.Service.remove_users_from_repo(self.data.name, id)

            repo = self.Service.get_project(self.data.name)
            return repo
        except Exception as err:
            raise Exception(f"Error updating repository: {err}")
    

    def delete_repository(self):
        try:
            repo = self.Service.delete_repo(self.data.name)
            return repo
        except Exception as err:
            raise Exception(f"Error deleting repository: {err}")


    def get_repository(self):
        try:
            repo = self.Service.get_project(self.data.name)
            return repo
        except Exception as err:
            raise Exception(f"Error getting repository: {err}")


    def create_commit_and_push(self):
        try:
            repo = self.Service.create_commit_and_push(self.data.name,
                                                    self.data.branch,
                                                    self.data.nameZip,
                                                    self.data.is_zip)
            return repo
        except Exception as err:
            raise Exception(f"Error create commit and push: {err}")    


    def clone_template(self):
        try:
            repo = self.Service.clone_and_push_repo(self.data.template,
                                                    self.data.branch,
                                                    self.data.name)
            return repo
        except Exception as err:  
            raise Exception(f"Error create template: {err}")     


