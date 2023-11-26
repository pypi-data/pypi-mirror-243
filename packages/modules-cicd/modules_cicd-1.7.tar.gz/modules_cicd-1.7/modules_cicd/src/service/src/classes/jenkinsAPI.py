import json
import re

import requests

from ..Interfaces.interfaces import BaseInterface
from .dataClass import DataClass
from decouple import config


class JenkinsInterface(BaseInterface):
    def __init__(self, data: DataClass):
        self.data = data

    def Login(self):
        pass

    def CreateProject(self):
        try:
            #region XML
            xml_folder = f"""
                <com.cloudbees.hudson.plugins.folder.Folder plugin="cloudbees-folder@6.815.v0dd5a_cb_40e0e">
                <properties/>
                <folderViews class="com.cloudbees.hudson.plugins.folder.views.DefaultFolderViewHolder">
                <views>
                <hudson.model.AllView>
                <owner class="com.cloudbees.hudson.plugins.folder.Folder" reference="../../../.."/>
                <name>All</name>
                <filterExecutors>false</filterExecutors>
                <filterQueue>false</filterQueue>
                <properties class="hudson.model.View$PropertyList"/>
                </hudson.model.AllView>
                </views>
                <tabBar class="hudson.views.DefaultViewsTabBar"/>
                </folderViews>
                <healthMetrics/>
                <icon class="com.cloudbees.hudson.plugins.folder.icons.StockFolderIcon"/>
                </com.cloudbees.hudson.plugins.folder.Folder>"""

            if self.data.git == 'Gitlab':
                new_xml = f"""
                    <org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch@746.v05814d19c001">
                    <actions/>
                    <displayName>{self.data.nameProject.lower()}</displayName>
                    <properties>
                    <jenkins.branch.ProjectNameProperty plugin="branch-api@2.1105.v472604208c55">
                    <name>{self.data.nameProject.lower()}</name>
                    </jenkins.branch.ProjectNameProperty>
                    </properties>
                    <folderViews class="jenkins.branch.MultiBranchProjectViewHolder" plugin="branch-api@2.1105.v472604208c55">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </folderViews>
                    <healthMetrics>
                    <com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric plugin="cloudbees-folder@6.815.v0dd5a_cb_40e0e">
                    <nonRecursive>false</nonRecursive>
                    </com.cloudbees.hudson.plugins.folder.health.WorstChildHealthMetric>
                    </healthMetrics>
                    <icon class="jenkins.branch.MetadataActionFolderIcon" plugin="branch-api@2.1105.v472604208c55">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </icon>
                    <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy" plugin="cloudbees-folder@6.815.v0dd5a_cb_40e0e">
                    <pruneDeadBranches>true</pruneDeadBranches>
                    <daysToKeep>-1</daysToKeep>
                    <numToKeep>3</numToKeep>
                    <abortBuilds>false</abortBuilds>
                    </orphanedItemStrategy>
                    <triggers/>
                    <disabled>false</disabled>
                    <sources class="jenkins.branch.MultiBranchProject$BranchSourceList" plugin="branch-api@2.1105.v472604208c55">
                    <data>
                    <jenkins.branch.BranchSource>
                    <source class="io.jenkins.plugins.gitlabbranchsource.GitLabSCMSource" plugin="gitlab-branch-source@660.vd45c0f4c0042">
                    <id>io.jenkins.plugins.gitlabbranchsource.GitLabSCMNavigator::https://gitlab.com::novateva::novateva/{self.data.repoName.lower()}</id>
                    <serverName>default</serverName>
                    <projectOwner>novateva</projectOwner>
                    <projectPath>novateva/{self.data.repoName.lower()}</projectPath>
                    <credentialsId>Ec2</credentialsId>
                    <traits>
                    <io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait>
                    <strategyId>3</strategyId>
                    </io.jenkins.plugins.gitlabbranchsource.BranchDiscoveryTrait>
                    <io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait>
                    <strategyId>1</strategyId>
                    </io.jenkins.plugins.gitlabbranchsource.OriginMergeRequestDiscoveryTrait>
                    <io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait>
                    <strategyId>1</strategyId>
                    <trust class="io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait$TrustPermission"/>
                    <buildMRForksNotMirror>false</buildMRForksNotMirror>
                    </io.jenkins.plugins.gitlabbranchsource.ForkMergeRequestDiscoveryTrait>
                    <io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait>
                    <alwaysBuildMROpen>true</alwaysBuildMROpen>
                    <alwaysBuildMRReOpen>true</alwaysBuildMRReOpen>
                    <alwaysIgnoreMRApproval>false</alwaysIgnoreMRApproval>
                    <alwaysIgnoreMRUnApproval>false</alwaysIgnoreMRUnApproval>
                    <alwaysIgnoreMRApproved>false</alwaysIgnoreMRApproved>
                    <alwaysIgnoreMRUnApproved>false</alwaysIgnoreMRUnApproved>
                    <alwaysIgnoreNonCodeRelatedUpdates>false</alwaysIgnoreNonCodeRelatedUpdates>
                    <alwaysIgnoreMRWorkInProgress>false</alwaysIgnoreMRWorkInProgress>
                    </io.jenkins.plugins.gitlabbranchsource.WebhookListenerBuildConditionsTrait>
                    </traits>
                    <sshRemote>git@gitlab.com:novateva/{self.data.repoName.lower()}.git</sshRemote>
                    <httpRemote>https://gitlab.com/novateva/{self.data.repoName.lower()}.git</httpRemote>
                    <projectId>44119409</projectId>
                    </source>
                    <strategy class="jenkins.branch.DefaultBranchPropertyStrategy">
                    <properties class="empty-list"/>
                    </strategy>
                    </jenkins.branch.BranchSource>
                    </data>
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </sources>
                    <factory class="org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    <scriptPath>Jenkinsfile</scriptPath>
                    </factory>
                    </org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>
                """
            else:
                new_xml = f"""<org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject plugin="workflow-multibranch@746.v05814d19c001">
                    <actions/>
                    <description/>
                    <displayName>{self.data.nameProject}</displayName>
                    <properties>
                    <jenkins.branch.ProjectNameProperty plugin="branch-api@2.1105.v472604208c55">
                    <name>{self.data.nameProject}</name>
                    </jenkins.branch.ProjectNameProperty>
                    </properties>
                    <folderViews class="jenkins.branch.MultiBranchProjectViewHolder" plugin="branch-api@2.1105.v472604208c55">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </folderViews>
                    <healthMetrics/>
                    <icon class="jenkins.branch.MetadataActionFolderIcon" plugin="branch-api@2.1105.v472604208c55">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </icon>
                    <orphanedItemStrategy class="com.cloudbees.hudson.plugins.folder.computed.DefaultOrphanedItemStrategy" plugin="cloudbees-folder@6.815.v0dd5a_cb_40e0e">
                    <pruneDeadBranches>true</pruneDeadBranches>
                    <daysToKeep>-1</daysToKeep>
                    <numToKeep>4</numToKeep>
                    <abortBuilds>false</abortBuilds>
                    </orphanedItemStrategy>
                    <triggers/>
                    <disabled>false</disabled>
                    <sources class="jenkins.branch.MultiBranchProject$BranchSourceList" plugin="branch-api@2.1105.v472604208c55">
                    <data>
                    <jenkins.branch.BranchSource>
                    <source class="org.jenkinsci.plugins.github_branch_source.GitHubSCMSource" plugin="github-branch-source@1703.vd5a_2b_29c6cdc">
                    <apiUri>https://api.github.com</apiUri>
                    <credentialsId>github-app</credentialsId>
                    <repoOwner>novateva</repoOwner>
                    <repository>{self.data.repoName}</repository>
                    <repositoryUrl>https://github.com/novateva/{self.data.repoName}.git</repositoryUrl>
                    <traits>
                    <org.jenkinsci.plugins.github__branch__source.BranchDiscoveryTrait>
                    <strategyId>3</strategyId>
                    </org.jenkinsci.plugins.github__branch__source.BranchDiscoveryTrait>
                    <org.jenkinsci.plugins.github__branch__source.OriginPullRequestDiscoveryTrait>
                    <strategyId>1</strategyId>
                    </org.jenkinsci.plugins.github__branch__source.OriginPullRequestDiscoveryTrait>
                    <org.jenkinsci.plugins.github__branch__source.ForkPullRequestDiscoveryTrait>
                    <strategyId>1</strategyId>
                    <trust class="org.jenkinsci.plugins.github_branch_source.ForkPullRequestDiscoveryTrait$TrustPermission"/>
                    </org.jenkinsci.plugins.github__branch__source.ForkPullRequestDiscoveryTrait>
                    </traits>
                    </source>
                    <strategy class="jenkins.branch.DefaultBranchPropertyStrategy">
                    <properties class="empty-list"/>
                    </strategy>
                    </jenkins.branch.BranchSource>
                    </data>
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    </sources>
                    <factory class="org.jenkinsci.plugins.workflow.multibranch.WorkflowBranchProjectFactory">
                    <owner class="org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject" reference="../.."/>
                    <scriptPath>Jenkinsfile</scriptPath>
                    </factory>
                    </org.jenkinsci.plugins.workflow.multibranch.WorkflowMultiBranchProject>"""
            #endregion
            new_folder_url = f"""http://jenkins.novateva.tech/job/Projects/
                                createItem?name={self.data.nameProject.lower()}"""
            create_folder_response = requests.post(
                new_folder_url.replace("\n", "").replace(" ", ""),
                auth=(self.data.user, self.data.token),
                data=xml_folder,
                headers={"Content-Type": "text/xml"},
            )

            if create_folder_response.status_code == 200:
                new_job_url = f"""http://jenkins.novateva.tech/job/
                                Projects/job/{self.data.nameProject.lower()}/
                                createItem?name={self.data.nameProject.lower()}"""
                create_job_response = requests.post(
                    new_job_url.replace("\n", "").replace(" ", ""),
                    auth=(self.data.user, self.data.token),
                    data=new_xml,
                    headers={"Content-Type": "text/xml"},
                )

                if create_job_response.status_code == 200:
                    response = {
                        "statusCode": 201,
                        "body": json.dumps("Project created in jenkins"),
                    }
                    return response
                else:
                    raise Exception("The project has not been created in Jenkins")
            else:
                raise Exception("The folder has not been created in Jenkins")
        except Exception as err:
            raise Exception(f"Error when creating the project in Jenkins: {err}")

    def DeleteProject(self):
        try:
            del_job_url = f"""http://jenkins.novateva.tech/job/Projects/
                            job/{self.data.nameProject}/doDelete"""
            del_job_response = requests.post(
                del_job_url.replace("\n", "").replace(" ", ""),
                auth=(self.data.user, self.data.token))
            if del_job_response.status_code == 200:
                response = {
                    "statusCode": 200,
                    "body": json.dumps("Project deleted in jenkins"),
                }
                return json.dumps(response)
            else:
                raise Exception("The project does not exist in Jenkins")
        except Exception as err:
            raise Exception(f"Error when deleting the project in Jenkins: {err}")

    def ReadProject(self):
        try:
            job_url = f"""http://jenkins.novateva.tech/job/Projects/
                        job/{self.data.nameProject}/job/{self.data.nameProject}/
                        config.xml"""
            response = requests.get(
                job_url.replace("\n", "").replace(" ", ""),
                auth=(self.data.user, self.data.token))

            if response.status_code == 200:
                regex_name = r"""<projectPath>novateva/(.*?)</projectPath>|
                                <repository>(.*?)</repository>"""
                project_name_match = re.search(
                    regex_name.replace("\n", "").replace(" ", ""),
                    response.text,
                )
                regex_path = r"""<httpRemote>(.*?)</httpRemote>|
                                <repositoryUrl>(.*?)</repositoryUrl>"""
                project_path_link = re.search(
                    regex_path.replace("\n", "").replace(" ", ""),
                    response.text,
                )
                if project_name_match and project_path_link:
                    if self.data.git == "Gitlab":
                        project_name = project_name_match.group(1)
                        project_path = project_path_link.group(1)
                    else:
                        project_name = project_name_match.group(2)
                        project_path = project_path_link.group(2)
                    data = {"nameProject": project_name, "provider": project_path}
                    response = {"statusCode": 200, "body": json.dumps(data)}
                    return json.dumps(response)
                else:
                    raise Exception("The project does not exist")
            else:
                raise Exception("The project does not exist in Jenkins")

        except Exception as err:
            raise Exception(f"Error when read the project in Jenkins: {err}")

    def UpdateProject(self):
        try:
            token = self.getTokenJenkins()
            folder_upd_url = f"""http://jenkins.novateva.tech/job/Projects/
                                job/{self.data.nameProject}/confirmRename"""
            project_upd_url = f"""http://jenkins.novateva.tech/job/Projects/job/
                            {self.data.updateProject}/job/{self.data.nameProject}/
                            confirmRename"""
            form_data = {
                "newName": self.data.updateProject,
                "Submit": "",
                "Jenkins-Crumb": token,
            }

            response_folder = requests.post(
                folder_upd_url.replace("\n", "").replace(" ", ""),
                auth=(self.data.user, self.data.token),
                data=form_data,
            )

            response_project = requests.post(
                project_upd_url.replace("\n", "").replace(" ", ""),
                auth=(self.data.user, self.data.token),
                data=form_data,
            )

            if (
                response_folder.status_code == 200
                and response_project.status_code == 200
            ):
                response = {
                    "statusCode": 200,
                    "body": json.dumps("Project updated correctly"),
                }
                return json.dumps(response)
            else:
                raise Exception("Error updating project")

        except Exception as err:
            raise Exception(f"Error updated the project in Jenkins: {err}")

    def getTokenJenkins(self):
        try:
            jenkins_url = "http://jenkins.novateva.tech"
            response = requests.get(
                f"{jenkins_url}/crumbIssuer/api/json",
                auth=(self.data.user, self.data.token),
            )

            if response.status_code == 200:
                crumb = response.json()
                return crumb["crumb"]
            else:
                raise Exception("The token has not been created")
        except Exception as err:
            raise Exception(f"Error get token in Jenkins: {err}")
