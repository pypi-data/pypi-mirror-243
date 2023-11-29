import unittest
from unittest.mock import MagicMock, Mock, patch

from decouple import config
from github import Github

from src.classes.github import GitHubAPI

TOKEN = config("TOKEN_GITHUB")


class TestCreateRepo(unittest.TestCase):
    def setUp(self):
        self.manager = GitHubAPI(TOKEN)

    @patch.object(Github, "get_user")
    def test_create_repo(self, mock_get_user):
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_repo.name = "test_repo"
        mock_user.create_repo.return_value = mock_repo
        mock_get_user.return_value = mock_user

        result = self.manager.create_repo("test_repo")
        self.assertEqual(result, mock_repo)
        mock_user.create_repo.assert_called_once_with(
            "test_repo", auto_init=True, private=True
        )

    @patch.object(Github, "get_user")
    def test_delete_repo(self, mock_get_user):
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        mock_repo = MagicMock()
        mock_user.get_repo.return_value = mock_repo

        self.manager.delete_repo("mock_repo")
        mock_get_user.assert_called_once()
        mock_user.get_repo.assert_called_once_with("mock_repo")
        mock_repo.delete.assert_called_once()

    @patch.object(Github, "get_user")
    def test_update_repo(self, mock_get_user):
        mock_user = MagicMock()
        mock_get_user.return_value = mock_user
        mock_repo = MagicMock()
        mock_user.get_repo.return_value = mock_repo

        result = self.manager.update_repo("repo_name", "new_name")
        self.assertTrue(result)
        mock_user.get_repo.assert_called_once_with("repo_name")
        mock_repo.edit.assert_called_once_with(name="new_name")

    @patch.object(Github, "get_user")
    def test_get_project(self, mock_get_user):
        mock_user = MagicMock()
        mock_project1 = MagicMock()
        mock_project1.name = "Project 1"
        mock_project2 = MagicMock()
        mock_project2.name = "Project 2"
        mock_user.get_projects.return_value = [mock_project1, mock_project2]
        mock_get_user.return_value = mock_user
        project_names = self.manager.get_project("dummy_username")
        mock_get_user.assert_called_once_with("dummy_username")
        self.assertEqual(project_names, ["Project 1", "Project 2"])

    @patch.object(Github, "get_user")
    def test_upload_a_file(self, mock_get_user):
        url = "https://gitlab.com/myuser/myrepo.git"
        new_directory = "myproject"
        template_name = "mytemplate"
        is_jenkins = "True"
        with patch("subprocess.call") as mock_call:
            self.manager.upload_a_file(url, new_directory, template_name, is_jenkins)
            assert mock_call.call_count == 3

    @patch.object(Github, "get_user")
    def test_remove_user_from_repo(self, mock_get_user):
        mock_user = MagicMock()
        mock_repo = MagicMock()
        mock_get_user.return_value = mock_user
        mock_user.get_repo.return_value = mock_repo

        result = self.manager.remove_users_from_repo("my_repo", "my_user")

        mock_get_user.assert_called_once_with()
        mock_user.get_repo.assert_called_once_with("my_repo")
        mock_repo.remove_from_collaborators.assert_called_once_with("my_user")
        self.assertTrue(result)

    def test_clone_repo(self):
        repo_name = "myrepo"
        user = "myuser"
        token = "mytoken"
        url = f"https://{user}:{token}@github.com/{user}/{repo_name}.git"
        with patch("git.Repo.clone_from", autospec=True) as mock_clone_from, patch(
            "subprocess.call", autospec=True
        ) as mock_subprocess:
            result = self.manager.clone_repo(repo_name, user, token)
            self.assertEqual(result, mock_clone_from.return_value)
            mock_clone_from.assert_called_once_with(url, repo_name)
            mock_subprocess.assert_called_once_with(
                f"cd {repo_name} && rm -rf .git", shell=True
            )

    @patch.object(Github, "get_user")
    @patch.object(Github, "get_repo")
    def test_add_users_to_repo(self, mock_get_repo, mock_get_user):
        mock_user = Mock()
        mock_repo = Mock()
        mock_user.get_repo.return_value = mock_repo
        mock_get_user.return_value = mock_user
        mock_get_repo.return_value = mock_repo

        result = self.manager.add_users_to_repo("my_repo", "my_username")

        mock_get_user.assert_called_once()
        mock_user.get_repo.assert_called_once_with("my_repo")
        mock_repo.add_to_collaborators.assert_called_once_with("my_username")
        self.assertEqual(result, mock_repo)

    @patch.object(Github, "get_user")
    def test_get_user(self, mock_user):
        mock_user.return_value = "user"

        result = self.manager.get_user("my_username")

        self.assertEqual(result, "user")
        mock_user.assert_called_once_with("my_username")


if __name__ == "__main__":
    unittest.main()
