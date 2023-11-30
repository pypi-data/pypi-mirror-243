from abc import ABC, abstractmethod


class BaseInterface(ABC):
    @abstractmethod
    def CreateProject(self):
        pass

    @abstractmethod
    def UpdateProject(self):
        pass

    @abstractmethod
    def DeleteProject(self):
        pass

    @abstractmethod
    def ReadProject(self):
        pass

    @abstractmethod
    def Login(self):
        pass

    @abstractmethod
    def getTokenJenkins(self):
        pass
