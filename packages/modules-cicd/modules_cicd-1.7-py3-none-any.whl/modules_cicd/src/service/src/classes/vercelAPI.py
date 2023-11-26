import requests

from ..Interfaces.interfaces import BaseInterface
from .dataClass import DataClass


class VercelInterfaceAPI(BaseInterface):
    def __init__(self, data: DataClass):
        self.data = data

    def getTokenJenkins(self):
        pass

    def createVarEnv(self):
        try:
            environment_variables = []
            if len(self.data.env) > 0:
                for env_var in self.data.env:
                    env_dict = {
                        "key": env_var["key"],
                        "value": env_var["value"],
                        "target": env_var["target"],
                        "type": env_var["type"],
                    }
                    environment_variables.append(env_dict)

            project_data = {
                "name": self.data.nameProject,
                "buildCommand": self.data.buildOptions[0] if len(self.data.buildOptions) > 0 else "",
                "commandForIgnoringBuildStep": "",
                "devCommand": self.data.buildOptions[1] if len(self.data.buildOptions) > 1 else "",
                "environmentVariables": environment_variables,
                "framework": self.data.framework,
                "gitRepository": {
                    "repo": self.data.buildOptions[2] if len(self.data.buildOptions) > 2 else "",
                    "type": self.data.buildOptions[3] if len(self.data.buildOptions) > 3 else "",
                },
                "installCommand": self.data.buildOptions[4] if len(self.data.buildOptions) > 4 else "",
                "outputDirectory": self.data.buildOptions[5] if len(self.data.buildOptions) > 5 else "",
                "publicSource": True,
                # "rootDirectory": self.data.BuildOptions[6],
                "skipGitConnectDuringLink": True,
            }

            return project_data
        except Exception as err:
            return False

    def CreateProject(self):
        try:
            project_data = self.createVarEnv()
            headers = {"Authorization": "Bearer %s" % self.data.token}
            if len(project_data) > 0:
                response = requests.post(
                    self.data.url_Api % self.data.group,
                    json=project_data,
                    headers=headers,
                )

                if response.status_code == 200:
                    response_data = response.json()
                    return response_data
                else:
                    return response.text
        except Exception as err:
            print(f"Error in Create Project: {err}")
            return False

    def UpdateProject(self):
        try:
            url = self.data.link_Api_All % (self.data.projectID, self.data.group)
            headers = {
                "Authorization": "Bearer %s" % self.data.token,
                "Content-Type": "application/json",
            }

            data = {
                "buildCommand": self.data.buildOptions[0] if len(self.data.buildOptions) > 0 else None,
                "devCommand": self.data.buildOptions[1] if len(self.data.buildOptions) > 1 else None,
                "framework": self.data.framework if self.data.framework else None,
                "installCommand": self.data.buildOptions[2] if len(self.data.buildOptions) > 2 else None,
                "name": self.data.updateProject if self.data.updateProject else None,
                "outputDirectory": self.data.buildOptions[3] if len(self.data.buildOptions) > 3 else None,
                #"rootDirectory":self.data.buildOptions[4] if len(self.data.buildOptions) > 4 else None,
            }

            response = requests.patch(url, headers=headers, json=data)

            if response.status_code == 200:
                print(response.text)
                response_data = response.json()
                return response_data
            else:
                print(response.text)
                raise Exception(response.status_code)
        except Exception as err:
            print(f"Error in Update Project: {err}")
            return False

    def DeleteProject(self):
        try:
            url = self.data.link_Api_All % (self.data.projectID, self.data.group)

            headers = {"Authorization": "Bearer %s" % self.data.token}

            response = requests.delete(url, headers=headers)

            if response.status_code == 204:
                return True
            else:
                raise Exception(response.status_code)
        except Exception as err:
            print(f"Error in Delete Project: {err}")
            return False

    def ReadProject(self):
        try:
            url = self.data.link_Api_All % (self.data.projectID, self.data.group)
            headers = {"Authorization": "Bearer %s" % self.data.token}

            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                return response_data
            else:
                raise Exception(response.text)
        except Exception as err:
            print(f"Error in Read Project: {err}")
            return False

    def Login(self):
        pass
