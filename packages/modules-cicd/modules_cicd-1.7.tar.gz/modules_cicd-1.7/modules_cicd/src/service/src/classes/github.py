import subprocess
import time
import os
import git
import boto3
import base64
import zipfile
from github import Github, GithubException, InputGitTreeElement
import github
from ..Interfaces.git import RepoAPI
import requests
import io


class GitHubAPI(RepoAPI):
    def __init__(self, token: str):
        self.g = Github(token)

    def search_group(self, group_name: str):
        pass

    def create_or_update_pull_request(
        self,
        repo_name: str,
        title: str,
        body: str,
        head: str,
        base: str,
        reviewers=None,
        assignee=None,
        labels=None,
        state=None,
    ):
        pass

    def get_statistics(self, repo_name: str, emails: str):
        pass

    def create_access_token(self, id: str, name: str):
        pass

    def remove_to_folders(self, name: str, templateName: str):
        pass

    def clone_repo(self, repo_name: str, user: str, token: str):
        try:
            url = f"https://{user}:{token}@github.com/{user}/{repo_name}.git"
            repo_clone = git.Repo.clone_from(url, repo_name)
            cmd = f"""cd {repo_name} && rm -rf .git"""
            subprocess.call(cmd.replace("\n", "").replace("  ", " "), shell=True)
            return repo_clone
        except GithubException as e:
            raise Exception(f"Error cloning repository: {e}")

    def create_repo(self, repo_name: str):
        try:
            user = self.g.get_user()
            repo = user.create_repo(repo_name, auto_init=True, private=True)
            return repo.id
        except GithubException as e:
            raise Exception(f"Error creating project: {e}")

    def delete_repo(self, name: str):
        try:
            user = self.g.get_user()
            repo = user.get_repo(name)
            repo.delete()
            return repo
        except GithubException as e:
            raise Exception(f"Error deleting repository: {e}")

    def update_repo(self, repo_name: str, new_name: str, description: str = None):
        try:
            user = self.g.get_user()
            repo = user.get_repo(repo_name)
            if new_name:
                repo.edit(name=new_name)
            response = {
                "id": repo.id,
                "name": repo.name,
                "url": repo.html_url
            }
            return response
        except GithubException as e:
            raise Exception(f"Error updating repository: {e}")

    def add_users_to_repo(self, name: str, username: str):
        try:
            repo = self.g.get_repo(name)
            repo.add_to_collaborators(username)
            return repo
        except GithubException as e:
            raise Exception(f"Error adding user to repository: {e}")

    def remove_users_from_repo(self, name: str, username: str):
        try:
            user = self.g.get_user()
            repo = user.get_repo(name)
            repo.remove_from_collaborators(username)
            return repo
        except GithubException as e:
            raise Exception(f"Error when deleting user from repository: {e}")

    def get_project(self, name: str):
        try:
            user = self.g.get_user()
            repo = user.get_repo(name)
            repo_info = {
                "id": repo.id,
                "name": repo.name,
                "url": repo.html_url,
            }
            return repo_info
        except GithubException as e:
            raise Exception(f"Error getting projects: {e}")

    def clone_and_push_repo(
        self, url: str, NewDirectory: str, templateName: str, isJenkins: str
    ):
        try:
            if isJenkins == "True":
                cmd = f"""git clone {url} && cd {NewDirectory}/ 
                    && git pull origin main"""
                subprocess.call(cmd.replace("\n", "").replace("  ", " "), shell=True)
                cmd = f"cp -Rf {templateName}/. {NewDirectory}/"
                subprocess.call(cmd, shell=True)
                time.sleep(2)
                cmd = f"""cd {NewDirectory}/ && git remote set-url origin {url} 
                          && git checkout -b dev 
                          && git add . 
                          && git commit -m 'Init project' 
                          && git push origin dev"""
                print(cmd)
                subprocess.call(cmd.replace("\n", "").replace("  ", " "), shell=True)
            else:
                cmd = f"""git clone {url} && cd {NewDirectory}/ 
                      && git pull origin main && rm README.md"""
                subprocess.call(cmd.replace("\n", "").replace("  ", " "), shell=True)
                cmd = f"cp -Rf {templateName}/. {NewDirectory}/"
                time.sleep(2)
                subprocess.call(cmd, shell=True)
                cmd = f"""cd {NewDirectory}/ && git add . 
                        && git commit -m 'Init project' 
                        && git remote set-url origin {url} 
                        && git push origin main"""
                subprocess.call(cmd.replace("\n", "").replace("  ", " "), shell=True)
            return True
        except GithubException as e:
            raise Exception(f"Error cloning and uploading files to the repo: {e}")

    def get_user(self, username: str):
        try:
            user = self.g.get_user(username)
            return user
        except GithubException as e:
            raise Exception(f"Error getting user: {e}")

    def create_commit_and_push(self, name: str, branch: str, nameZip: str = "", token:str = "", is_zip: bool = False):
        try:
            bucket_name = os.environ['bucket_name']
            aws_access_key_id = os.environ['aws_access_key_id']
            aws_secret_access_key = os.environ['aws_secret_access_key']
            s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-2')

            user = self.g.get_user()
            
            headers = {
                'Authorization': 'token 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'
            }
            if is_zip:
                response = s3_client.get_object(Bucket=bucket_name, Key=nameZip)
                
                zip_content = response['Body'].read()

                with open(f'/tmp/{nameZip}', 'wb') as zip_file:
                    zip_file.write(zip_content)
                
                with zipfile.ZipFile(f'/tmp/{nameZip}', 'r') as zip_ref:
                    zip_ref.extractall('/tmp')

                for folder_name in ['Back', 'Front']:
                    name = ""
                    if folder_name == 'Back':
                        name = f"back-{name}"
                        project = user.create_repo(name, auto_init=True, private=True)
                    else:
                        name = f"front-{name}"
                        project = user.create_repo(name, auto_init=True, private=True)
                    file_info_list = []
                    for root, _, files in os.walk(f"/tmp/{folder_name}"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(file_path, f"/tmp/{folder_name}")
                            with open(file_path, 'rb') as content_file:
                                archivo_contenido = content_file.read()
                                b64_content = base64.b64encode(archivo_contenido).decode('utf-8')
                            file_info_list.append({
                                "name": relative_path,
                                "content": b64_content
                            })
                    url_template = f'https://api.github.com/repos/torrencia/{name}/contents/'
                    for file_info in file_info_list:
                        file_name = file_info["name"]
                        base64_content = file_info["content"]
                        url = f'{url_template}{file_name}'
                        data = {
                            "message": f"Add base64 file: {file_name}",
                            "content": base64_content,
                            "branch": branch
                        }
                        response = requests.put(url, headers=headers, json=data)
                response = {
                    "statusCode": 200,
                    "body": "Repository created for Back and Front"
                }
            else:
                repo = self.g.get_user().get_repo(name)
                file_name = "README.md"
                file_content = "Init Commit"
                archivo = repo.get_contents(file_name, ref=branch)

                repo.update_file(
                    path=file_name,
                    message="Init Commit",
                    content=file_content,
                    sha=archivo.sha,
                    branch=branch,
                )
                response = {
                    "statusCode": 200,
                    "body": "Create and push Commit"
                }
            return response
        except Exception as err:
            raise Exception(f"Error create and commit push: {err}")
