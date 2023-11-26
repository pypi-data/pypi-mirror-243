import unittest
from unittest.mock import Mock, patch

from decouple import config

from src.classes.dataClass import DataClass
from src.classes.vercelAPI import VercelInterfaceAPI

TOKEN_VERCEL = config("TOKEN_VERCEL")


class TestVercelAPI(unittest.TestCase):
    def setUp(self):
        # self.vercel = DataClass(projectID="prj_123")
        self.vercel = DataClass(
            nameProject="testapivercel",
            projectID="prj_123",
            updateProject="vercelapitest",
            framework="vite",
            buildOptions=[
                "vite build",
                "vite --port $PORT",
                "testApi",
                "gitlab",
                "npm install",
                "dist",
            ],
            env=[
                {
                    "key": "VARIABLE_1",
                    "value": "VALOR_1",
                    "target": "production",
                    "type": "plain",
                }
            ],
        )
        self.ProjectVercel = VercelInterfaceAPI(self.vercel)

    @patch("src.classes.vercelAPI.requests.get")
    def test_read_project(self, mock_get):
        response_data = {
            "accountId": "team_123",
            "autoExposeSystemEnvs": True,
            "autoAssignCustomDomains": True,
            "autoAssignCustomDomainsUpdatedBy": "system",
            "buildCommand": "vite build",
            "commandForIgnoringBuildStep": "",
            "createdAt": 1694206514029,
            "devCommand": "vite --port $PORT",
            "directoryListing": False,
            "framework": "vite",
            "gitForkProtection": True,
            "gitLFS": False,
            "id": "prj_123",
            "installCommand": "vite",
            "lastRollbackTarget": None,
            "lastAliasRequest": None,
            "name": "vercelapitest",
            "nodeVersion": "18.x",
            "outputDirectory": "npm install",
            "publicSource": True,
            "rootDirectory": None,
            "serverlessFunctionRegion": "iad1",
            "sourceFilesOutsideRootDirectory": True,
            "updatedAt": 1694552190093,
            "live": False,
            "gitComments": {"onCommit": False, "onPullRequest": True},
            "link": {
                "type": "gitlab",
                "projectId": "49060691",
                "projectName": "testApi",
                "projectNameWithNamespace": "test / testApi",
                "projectNamespace": "ktja",
                "projectUrl": "https://gitlab.com/test/testapi",
                "gitCredentialId": "cred_36",
                "productionBranch": "main",
                "createdAt": 1694206513217,
                "updatedAt": 1694206513217,
                "deployHooks": [],
            },
            "latestDeployments": [],
            "targets": {},
        }
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = response_data

        instance = self.ProjectVercel
        result = instance.ReadProject()

        mock_get.assert_called_once_with(
            "https://api.vercel.com/v12/projects/prj_123?teamId=team_HFjyG4RdbIeFralE86LXV4Yp",
            headers={"Authorization": "Bearer %s" % TOKEN_VERCEL},
        )

        self.assertEqual(result, response_data)

    @patch("src.classes.vercelAPI.requests.delete")  # Mock de requests.delete
    def test_delete_project(self, mock_delete):
        # Simular una respuesta exitosa para la solicitud DELETE
        mock_delete.return_value.status_code = 204

        # Llamar a la función que se está probando
        instance = self.ProjectVercel
        result = instance.DeleteProject()

        # Verificar que la solicitud DELETE se hizo a la URL correcta con los encabezados correctos
        mock_delete.assert_called_once_with(
            "https://api.vercel.com/v12/projects/prj_123?teamId=team_HFjyG4RdbIeFralE86LXV4Yp",
            headers={"Authorization": "Bearer %s" % TOKEN_VERCEL},
        )

        # Verificar que la función devuelve True en caso de éxito
        self.assertTrue(result)

    @patch("src.classes.vercelAPI.requests.patch")
    def test_update_project(self, mock_patch):
        response_data = {
            "buildCommand": "buildCmd",
            "devCommand": "devCmd",
            "framework": "your_framework",
            "installCommand": "installCmd",
            "name": "project_name",
            "outputDirectory": "outputDir",
        }
        mock_patch.return_value.status_code = 200
        mock_patch.return_value.json.return_value = response_data

        instance = self.ProjectVercel
        instance.data.TokenAPI = (TOKEN_VERCEL,)
        instance.data.BuildOptions = ["buildCmd", "devCmd", "installCmd", "outputDir"]
        instance.data.Framework = "your_framework"
        instance.data.updateProject = "project_name"

        result = instance.UpdateProject()

        url = "https://api.vercel.com/v12/projects/prj_123?teamId=team_HFjyG4RdbIeFralE86LXV4Yp"
        headers = {
            "Authorization": "Bearer %s" % TOKEN_VERCEL,
            "Content-Type": "application/json",
        }
        data = {
            "buildCommand": "buildCmd",
            "devCommand": "devCmd",
            "framework": "your_framework",
            "installCommand": "installCmd",
            "name": "project_name",
            "outputDirectory": "outputDir",
        }
        mock_patch.assert_called_once_with(url, headers=headers, json=data)

        self.assertEqual(result, response_data)

    @patch("src.classes.vercelAPI.requests.post")
    def test_create_project_success(self, mock_post):
        response_data = {
            "name": "name",
            "buildCommand": "buildCommand",
            "commandForIgnoringBuildStep": "",
            "devCommand": "devCommand",
            "environmentVariables": [
                {
                    "key": "VARIABLE_1",
                    "value": "VALOR_1",
                    "target": "production",
                    "type": "plain",
                }
            ],
            "framework": "framework",
            "gitRepository": {
                "repo": "main",
                "type": "gitlab",
            },
            "installCommand": "installCommand",
            "outputDirectory": "outputDirectory",
            "publicSource": True,
            "skipGitConnectDuringLink": True,
        }
        mock_post.return_value.status_code = 200
        mock_post.return_value.json.return_value = response_data

        instance = self.ProjectVercel

        result = instance.CreateProject()

        mock_post.assert_called_once_with(
            instance.data.Url_Api,
            json=instance.createVarEnv(),
            headers={"Authorization": f"Bearer {TOKEN_VERCEL}"},
        )

        self.assertEqual(result, response_data)
