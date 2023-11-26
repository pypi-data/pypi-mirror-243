from abc import ABC, abstractmethod


class RepoAPI(ABC):
    @abstractmethod
    def create_repo(self, repo_name, group=None, template=None):
        pass

    @abstractmethod
    def add_users_to_repo(self, repo, emails):
        pass

    @abstractmethod
    def remove_users_from_repo(self, repo_name, emails):
        pass

    @abstractmethod
    def update_repo(self, repo_name, new_name=None, new_description=None):
        pass

    @abstractmethod
    def create_or_update_pull_request(
        self,
        repo_name,
        title,
        body,
        head,
        base,
        reviewers=None,
        assignee=None,
        labels=None,
        state=None,
    ):
        pass

    @abstractmethod
    def get_statistics(self, repo_name, emails):
        pass

    @abstractmethod
    def delete_repo(self, repo_name):
        pass

    @abstractmethod
    def get_project(self, id):
        pass

    @abstractmethod
    def get_user(self, username, email):
        pass

    @abstractmethod
    def create_access_token(self, id, name):
        pass

    @abstractmethod
    def remove_to_folders(self, name, templateName):
        pass

    @abstractmethod
    def create_commit_and_push(self, project_id, branch_name):
        pass

    @abstractmethod
    def clone_and_push_repo(self, template, branch, name):
        pass