import unittest
from unittest.mock import MagicMock, Mock, patch

import gitlab
from decouple import config

from src.classes.gitlab import GitLabAPI

TOKEN = config("TOKEN_GITLAB")


class TestCreateRepo(unittest.TestCase):
    def setUp(self):
        self.gitlab = GitLabAPI(TOKEN)

    @patch("src.classes.gitlab.GitLabAPI.create_repo")
    def test_create_repo(self, mock_project):
        mock_project_instance = Mock()
        mock_group_instance = Mock()
        mock_group_instance.create_repository.return_value = mock_project_instance
        mock_projects_instance = Mock()
        mock_projects_instance.create.return_value = mock_project_instance
        mock_project.return_value = mock_project_instance

        result = self.gitlab.create_repo("test_repo", "", "test")
        self.assertEqual(result, mock_project_instance)

    @patch.object(gitlab, "Gitlab")
    def test_add_users_to_repo(self, mock_gitlab):
        mock_project = MagicMock()
        mock_project.members.create.return_value = None
        mock_user = MagicMock()
        mock_user.id = 1234

        mock_gitlab.return_value.projects.get.return_value = mock_project
        mock_gitlab.return_value.users.get.return_value = mock_user

        api = GitLabAPI(TOKEN)
        result = api.add_users_to_repo("my-project", "example@example.com")

        mock_gitlab.return_value.projects.get.assert_called_once_with(id="my-project")
        mock_gitlab.return_value.users.get.assert_called_once_with(
            id="example@example.com"
        )
        mock_project.members.create.assert_called_once_with(
            {"user_id": 1234, "access_level": gitlab.const.AccessLevel.DEVELOPER}
        )
        self.assertEqual(result, mock_project)

    @patch.object(gitlab, "Gitlab")
    def test_remove_users_from_repo(self, mock_gl):
        mock_project = Mock()
        mock_user = Mock()
        mock_project.members.delete = Mock()
        mock_gl_instance = Mock()
        mock_gl_instance.projects.get = Mock(return_value=mock_project)
        mock_gl_instance.users.get = Mock(return_value=mock_user)
        mock_gl.return_value = mock_gl_instance

        api = GitLabAPI(TOKEN)
        result = api.remove_users_from_repo("my_repo", "my_email")

        mock_gl_instance.projects.get.assert_called_once_with(id="my_repo")
        mock_gl_instance.users.get.assert_called_once_with(id="my_email")
        mock_project.members.delete.assert_called_once_with(mock_user.id)
        self.assertEqual(result, mock_user.id)

    @patch.object(gitlab, "Gitlab")
    def test_update_repo(self, mock_get):
        mock_project = MagicMock()
        mock_project.name = "New Name"
        mock_project.description = "New Description"
        mock_get.return_value = mock_project

        api = GitLabAPI(TOKEN)
        updated_repo = api.update_repo("my_repo", "New Name", "New Description")

        self.assertEqual(updated_repo.name, "New Name")
        self.assertEqual(updated_repo.description, "New Description")

    # @patch.object(gitlab, "Gitlab")
    def test_delete_repo(self):
        with patch("gitlab.Gitlab") as MockGitlab:
            mock_project = MagicMock()
            mock_project.delete.return_value = None
            MockGitlab.return_value.projects.get.return_value = mock_project
            api = GitLabAPI(TOKEN)
            result = api.delete_repo("repo_name")
            self.assertTrue(result)
            MockGitlab.assert_called_once()
            MockGitlab.return_value.projects.get.assert_called_once_with(id="repo_name")
            mock_project.delete.assert_called_once()

    def test_get_project(self):
        with patch("gitlab.Gitlab") as mock_gitlab:
            mock_project = MagicMock()
            mock_project.id = 1
            mock_gitlab_instance = MagicMock()
            mock_gitlab_instance.projects.get.return_value = mock_project
            mock_gitlab.return_value = mock_gitlab_instance

            api = GitLabAPI(TOKEN)
            result = api.get_project("1")
            self.assertEqual(result, mock_project)
            mock_gitlab_instance.projects.get.assert_called_once_with(id="1")

    def test_clone_repo(self):
        with patch("gitlab.Gitlab") as mock_gitlab:
            mock_project = mock_gitlab.return_value.projects.get.return_value
            mock_project.name = "test_repo"
            mock_project.ssh_url_to_repo = "ssh://gitlab.com/test_repo.git"
            mock_project.http_url_to_repo = "https://gitlab.com/test_repo.git"
            mock_project.path = "test_repo"

            repo_root_dir = "/path/to/repo_root_dir"
            cloning_mode = "http"
            branchName = "master"
            user = "test_user"
            password = "test_password"

            api = GitLabAPI(TOKEN)
            repo = api.clone_repo(
                "test_project_id",
                repo_root_dir,
                cloning_mode,
                branchName,
                user,
                password,
            )

            assert mock_gitlab.call_count == 1
            assert mock_gitlab.return_value.projects.get.call_count == 1
            assert repo == mock_project

    @patch.object(gitlab, "Gitlab")
    def test_get_user(self, mock_gitlab):
        # Simular la respuesta de la API de GitLab
        mock_user = {"id": 123, "name": "John Smith", "username": "jsmith"}
        mock_users_list = [mock_user]
        mock_users = mock_gitlab.return_value.users
        mock_users.list.return_value = mock_users_list

        # Llamar a la función que se está probando
        api = GitLabAPI(TOKEN)
        user = api.get_user("jsmith")

        # Verificar que la respuesta de la función sea la esperada
        self.assertEqual(user["id"], mock_user["id"])
        self.assertEqual(user["name"], mock_user["name"])
        self.assertEqual(user["username"], mock_user["username"])

    def test_create_access_token(self):
        with patch("gitlab.Gitlab") as mock_gitlab:
            mock_project = MagicMock()
            mock_token = MagicMock()
            mock_token.token = "my_access_token"
            mock_project.access_tokens.create.return_value = mock_token
            mock_gitlab().projects.get.return_value = mock_project

            api = GitLabAPI(TOKEN)
            access_token = api.create_access_token("my_project", "my_token_name")

            assert access_token == "my_access_token"

    @patch("subprocess.call")
    def test_remove_folders(self, mock_call):
        nameProject = "test_project"
        GitProject = "test_git_project"
        expected_cmd = f"rm -rf {nameProject} && rm -rf {GitProject}"

        api = GitLabAPI(TOKEN)
        result = api.remove_to_folders(nameProject, GitProject)

        mock_call.assert_called_once_with(expected_cmd, shell=True)
        self.assertTrue(result)

    def test_upload_a_file(self):
        url = "https://gitlab.com/myuser/myrepo.git"
        new_directory = "myproject"
        template_name = "mytemplate"
        is_jenkins = "True"

        with patch("subprocess.call") as mock_call:
            api = GitLabAPI(TOKEN)
            api.upload_a_file(url, new_directory, template_name, is_jenkins)
            assert mock_call.call_count == 3


if __name__ == "__main__":
    unittest.main()
