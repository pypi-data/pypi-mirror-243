import json
import unittest
from unittest.mock import Mock, patch

import requests
from decouple import config

# from src.service.src.classes.dataClass import DataClass
from src.service.src.classes.dataClass import DataClass
from src.service.src.classes.jenkinsAPI import JenkinsInterface

USER_JENKINS = config("USER_JENKINS")
PASSWORD_JENKINS = config("PASSWORD_JENKINS")
TOKEN_JENKINS = config("TOKEN_JENKINS")


class TestJenkinsXML(unittest.TestCase):
    def setUp(self):
        self.jenkins = DataClass(
            user=USER_JENKINS,
            password=PASSWORD_JENKINS,
            nameProject="testjenkins",
            updateProject="jenkinstest",
            repoName="novateva",
            git="Gitlab",
            login=False,
        )
        self.ProjectJenkins = JenkinsInterface(self.jenkins)

    @patch("requests.post")
    def test_create_project(self, mock_post):
        mock_post.side_effect = [Mock(status_code=200), Mock(status_code=200)]

        result = self.ProjectJenkins.CreateProject()

        expected_folder_url = f"""http://jenkins.novateva.tech/job/
                                Projects/createItem?name={self.jenkins.nameProject}"""
        expected_job_url = f"""http://jenkins.novateva.tech/job/Projects
                                /job/{self.jenkins.nameProject}/
                                createItem?name={self.jenkins.nameProject}"""
        expected_headers = {"Content-Type": "text/xml"}
        expected_auth = (USER_JENKINS, TOKEN_JENKINS)

        mock_post.assert_has_calls(
            [
                unittest.mock.call(
                    expected_folder_url.replace("\n", "").replace(" ",""),
                    auth=expected_auth,
                    data=unittest.mock.ANY,
                    headers=expected_headers,
                ),
                unittest.mock.call(
                    expected_job_url.replace("\n", "").replace(" ",""),
                    auth=expected_auth,
                    data=unittest.mock.ANY,
                    headers=expected_headers,
                ),
            ],
            any_order=False,
        )

        expected_result = {
            "statusCode": 201,
            "body": json.dumps("Project created in jenkins"),
        }
        self.assertEqual(result, json.dumps(expected_result))

    @patch.object(requests, "get")
    def test_read_project(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = """
            <?xml version='1.1' encoding='UTF-8'?>
            <projectPath>novateva/your_project</projectPath>
            <httpRemote>https://your_project_url</httpRemote>
            """
        mock_get.return_value = mock_response

        result = self.ProjectJenkins.ReadProject()

        expected_result = {
            "statusCode": 200,
            "body": json.dumps(
                {"nameProject": "your_project", "provider": "https://your_project_url"}
            ),
        }
        self.assertEqual(result, json.dumps(expected_result))

    @patch("requests.post")
    def test_delete_project(self, mock_post):
        mock_post.return_value.status_code = 200
        result = self.ProjectJenkins.DeleteProject()

        expected_url = f"""http://jenkins.novateva.tech/job/Projects
                        /job/{self.jenkins.nameProject}/doDelete"""
        mock_post.assert_called_once_with(
            expected_url.replace("\n", "").replace(" ",""), auth=(USER_JENKINS, TOKEN_JENKINS)
        )

        expected_result = {
            "statusCode": 200,
            "body": json.dumps("Project deleted in jenkins"),
        }
        self.assertEqual(result, json.dumps(expected_result))

    @patch("requests.post")
    def test_update_project(self, mock_post):
        mock_post.return_value.status_code = 200

        data = DataClass(
            user=USER_JENKINS,
            password=PASSWORD_JENKINS,
            nameProject="testjenkins",
            updateProject="jenkinstest",
            repoName="novateva",
            login=False,
        )
        mock_updater = JenkinsInterface(data)
        mock_updater.getTokenJenkins = Mock(return_value="fake_token")

        result = mock_updater.UpdateProject()
        folder = f"""http://jenkins.novateva.tech/job/Projects
                    /job/{self.jenkins.nameProject}/confirmRename"""
        job = f"""http://jenkins.novateva.tech/job/Projects/
                    job/{self.jenkins.updateProject}/
                    job/{self.jenkins.nameProject}/confirmRename"""
        self.assertEqual(mock_post.call_count, 2)
        expected_post_calls = [
            unittest.mock.call(
                folder.replace("\n", "").replace(" ",""),
                auth=(USER_JENKINS, TOKEN_JENKINS),
                data=unittest.mock.ANY,
            ),
            unittest.mock.call(
                job.replace("\n", "").replace(" ",""),
                auth=(USER_JENKINS, TOKEN_JENKINS),
                data=unittest.mock.ANY,
            ),
        ]
        mock_post.assert_has_calls(expected_post_calls, any_order=False)

        expected_result = {
            "statusCode": 200,
            "body": json.dumps("Project updated correctly"),
        }
        self.assertEqual(result, json.dumps(expected_result))

    @patch("requests.get")
    def test_get_token(self, mock_get):
        fake_response = Mock()
        fake_response.status_code = 200
        fake_response.json.return_value = {"crumb": "fake_crumb"}
        mock_get.return_value = fake_response

        token = self.ProjectJenkins.getTokenJenkins()

        mock_get.assert_called_once_with(
            "http://jenkins.novateva.tech/crumbIssuer/api/json",
            auth=(USER_JENKINS, TOKEN_JENKINS),
        )

        self.assertEqual(token, "fake_crumb")
