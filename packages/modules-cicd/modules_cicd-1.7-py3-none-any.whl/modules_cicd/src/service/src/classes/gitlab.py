import os
import subprocess
import time
import json
import git
import gitlab
import urllib3
import boto3
from base64 import b64encode
import zipfile

from ..Interfaces.git import RepoAPI

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GitLabAPI(RepoAPI):
    def __init__(self, token: str):
        self.gl = gitlab.Gitlab(
            "https://gitlab.com/", oauth_token=token, api_version=4, ssl_verify=False
        )

    def create_repo(self, repo_name: str, group: str = None, template: str = None):
        try:
            new_repo = None
            if group:
                new_repo = group.create_repository({"name": repo_name})
                new_repo = self.gl.projects.create({"name": repo_name})
                data = {
                    "branch": "main",
                    "commit_message": f"First upload on repo {repo_name}",
                    "actions": [
                        {
                            "action": "create",
                            "file_path": "./README.md",
                            "content": f"First upload on repo {repo_name}",
                        },
                    ],
                }
                new_repo.commits.create(data)
            else:
                new_repo = self.gl.projects.create({"name": repo_name})
                data = {
                    "branch": "main",
                    "commit_message": f"First upload on repo {repo_name}",
                    "actions": [
                        {
                            "action": "create",
                            "file_path": "./README.md",
                            "content": f"First upload on repo {repo_name}",
                        },
                    ],
                }
                new_repo.commits.create(data)
            if template:
                new_repo.repository_tree.create(
                    {"path": "/", "branch": "master"}, template.id, "master"
                )
            return new_repo
        except Exception as err:
            raise Exception(f"Error creating project: {err}")


    def add_users_to_repo(self, repo: str, emails: str):
        try:
            repo = self.gl.projects.get(id=repo)
            user = self.gl.users.get(id=emails)
            repo.members.create(
                {"user_id": user.id, "access_level": gitlab.const.AccessLevel.DEVELOPER}
            )
            return repo
        except Exception as err:
            raise Exception(f"Error adding user to repository: {err}")


    def get_statistics(self, repo_name: str, emails: str):
        try:
            repo = self.gl.projects.get(repo_name)
            commit_count = 0
            merge_request_count = 0
            merge_request_changes_count = 0
            merge_request_comment_count = 0
            for email in emails:
                commits = repo.commits.list(author_email=email)
                commit_count += len(commits)
                merge_requests = repo.mergerequests.list(author_email=email)
                merge_request_count += len(merge_requests)
                for mr in merge_requests:
                    merge_request_changes_count += mr.changes_count
                    merge_request_comment_count += mr.notes.list().total
            return {
                "commits": commit_count,
                "merge_request_comments": merge_request_comment_count,
                "merge_request_changes": merge_request_changes_count,
                "merge_requests": merge_request_count,
            }
        except Exception as err:
            raise Exception(f"Error when obtaining statistics: {err}")


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
        try:
            repo = self.gl.projects.get(repo_name)
            pull_requests = repo.mergerequests.list(state="opened")
            pull_request = None
            for pr in pull_requests:
                if pr.title == title:
                    pull_request = pr
                    break
            if pull_request:
                pull_request.title = title
                pull_request.description = body
                pull_request.source_branch = head
                pull_request.target_branch = base
                if reviewers:
                    pull_request.reviewers = reviewers
                if assignee:
                    pull_request.assignee = assignee
                if labels:
                    pull_request.labels = labels
                if state:
                    pull_request.state = state
                pull_request.save()
            else:
                pull_request = repo.mergerequests.create(
                    {
                        "title": title,
                        "description": body,
                        "source_branch": head,
                        "target_branch": base,
                        "reviewers": reviewers,
                        "assignee": assignee,
                        "labels": labels,
                        "state": state,
                    }
                )
            return True
        except Exception as err:
            raise Exception(f"Error when create or update: {err}")


    def remove_users_from_repo(self, repo_name: str, emails: str):
        try:
            repo = self.gl.projects.get(id=repo_name)
            user = self.gl.users.get(id=emails)
            repo.members.delete(user.id)
            return user.id
        except Exception as err:
            raise Exception(f"Error when deleting user from repository: {err}")


    def update_repo(
        self, repo_name: str, new_name: str = None, new_description: str = None
    ):
        try:
            repo = self.gl.projects.get(id=repo_name)
            if new_name:
                repo.name = new_name
            if new_description:
                repo.description = new_description
            repo.save()
            #update_repo = self.gl.projects.get(id=repo_name)
            response = {
                "id": repo.id,
                "name": repo.name,
                "url": repo.http_url_to_repo
            }
            return response
        except Exception as err:
            raise Exception(f"Error updating repository: {err}")

    def delete_repo(self, repo_name: str):
        try:
            repo = self.gl.projects.get(id=repo_name)
            repo.delete()
            return repo
        except Exception as err:
            raise Exception(f"Error deleting repository: {err}")


    def get_project(self, id: str):
        try:
            project = self.gl.projects.get(id=id)
            response = {
                "id": project.id,
                "name": project.name,
                "url": project.http_url_to_repo
            }
            return response
        except Exception as err:
            raise Exception(f"Error getting projects: {err}")


    def get_user(self, username: str):
        try:
            user = self.gl.users.list(username=username)[0]
            return user
        except Exception as err:
            raise Exception(f"Error getting user: {err}")


    def create_access_token(self, id: str, name: str):
        try:
            myTuple = ("Token", name)
            name = "".join(myTuple)
            access_token = self.gl.projects.get(id).access_tokens.create(
                {"name": name, "scopes": ["api"]}
            )
            return access_token.token
        except Exception as err:
            raise Exception(f"Error creating token: {err}")


    def remove_to_folders(self, nameProject: str, GitProject: str):
        try:
            cmd = f"rm -rf {nameProject} && rm -rf {GitProject}"
            subprocess.call(cmd, shell=True)
            return True
        except Exception as err:
            raise Exception(f"Error removing repo folder: {err}")

    def create_commit_and_push(self, name: str, branch: str, nameZip: str = "" , is_zip: bool = False):
        try:
            if is_zip:
                bucket_name = os.environ['bucket_name']
                aws_access_key_id = os.environ['aws_access_key_id']
                aws_secret_access_key = os.environ['aws_secret_access_key']
                s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, region_name='us-east-2')

                response = s3_client.get_object(Bucket=bucket_name, Key=nameZip)

                zip_content = response['Body'].read()

                with open(f'/tmp/{nameZip}', 'wb') as zip_file:
                    zip_file.write(zip_content)

                with zipfile.ZipFile(f'/tmp/{nameZip}', 'r') as zip_ref:
                    zip_ref.extractall('/tmp')

                commit_data = {
                    'branch': branch,
                    'commit_message': "init commit"
                }

                ids_from_repo = []
                for folder_name in ['Back', 'Front']:
                    if folder_name == 'Back':
                        project = self.gl.projects.create({"name": f"back-{name}"})
                        ids_from_repo.append(project.id)
                    else:
                        project = self.gl.projects.create({"name": f"front-{name}"})
                        ids_from_repo.append(project.id)
                    changes = []
                    for root, dirs, files in os.walk(f"/tmp/{folder_name}"):
                        for file in files:
                            file_path = os.path.join(root, file)
                            relative_path = os.path.relpath(file_path, f"/tmp/{folder_name}")
                            with open(file_path, 'rb') as file_content:
                                archivo_contenido = file_content.read()
                                b64_content = b64encode(archivo_contenido).decode('utf-8')
                            cambio = {
                                'action': 'create',
                                'file_path': relative_path,
                                'content': b64_content,
                                'encoding': 'base64'
                            }
                            changes.append(cambio)
                    commit_data['actions'] = changes
                    project.commits.create(commit_data)
                response = {
                    "statusCode": 200,
                    "body": "Repository created for Back and Front",
                    "id_repo_back": ids_from_repo[0],
                    "id_repo_front": ids_from_repo[1],
                }
            else:
                project = self.gl.projects.get(name)
                project.commits.create(
                    {
                        "branch": branch,
                        "commit_message": "Init Commit",
                        "actions": [
                            {
                                "action": "update",
                                "file_path": "./README.md",
                                "content": "Init Commit",
                            }
                        ],
                    }
                )
                response = {
                    "statusCode": 200,
                    "body": "Create and push Commit"
                }
            return response
        except Exception as err:
            raise Exception(f"Error create and commit push: {err}")

    def clone_and_push_repo(self, template_id: str, branch: str, repo_name: str):
        try:
            project_origen = self.gl.projects.get(template_id)

            tree = project_origen.repository_tree(ref=branch, recursive=True, all=True)

            repository_structure = {}

            for item in tree:
                path = item['path']
                item_type = item['type']
                if item_type == 'tree':
                    if path not in repository_structure:
                        repository_structure[path] = {}
                elif item_type == 'blob':
                    file_info = project_origen.files.get(file_path=path, ref=f'{branch}')
                    content = file_info.decode()
                    encoded_content = b64encode(content).decode()
                    repository_structure[path] = encoded_content

            projecto = self.gl.projects.create({"name": f"{repo_name}"})
            commit_data = {
                'branch': f'{branch}',
                'commit_message': "init commit"
            }
            changes = []
            for path, encoded_content in repository_structure.items():
                if isinstance(encoded_content, str):
                    cambio = {
                        'action': 'create',
                        'file_path': path,
                        'content': encoded_content,
                        'encoding': 'base64'
                    }
                    changes.append(cambio)
                else:
                    pass
            commit_data['actions'] = changes
            projecto.commits.create(commit_data)
            response = {
                    "statusCode": 200,
                    "body": "Clone template ready!"
                }
            return response
        except Exception as err:
            raise Exception(f"Error clone and push repository: {err}")

