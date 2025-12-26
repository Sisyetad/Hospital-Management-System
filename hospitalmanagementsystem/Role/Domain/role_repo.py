from abc import ABC, abstractmethod
from typing import List
from .role_entity import Role


class IRoleRepository(ABC):
    @abstractmethod
    def createRole(self, role_name: str) -> Role: pass

    @abstractmethod
    def deleteRole(self, role_id: int): pass

    @abstractmethod
    def updateRole(self, role_id: int, role_name:str) -> Role: pass

    @abstractmethod
    def getAllRoles(self) -> List[Role]: pass

    @abstractmethod
    def getRole(self, role_name)->Role: pass