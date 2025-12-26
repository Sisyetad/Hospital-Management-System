from abc import ABC, abstractmethod


class IReceptionistRepository(ABC):
    @abstractmethod
    def createReceptionist(self, receptionist_name, email, role_name, phone, location):pass

    @abstractmethod
    def deleteReceptionist(self, receptionist_id): pass

    @abstractmethod
    def updateReceptionist(self, receptionist_id, receptionist_name, phone, location): pass

    @abstractmethod
    def getReceptionistByID(self, receptionist_id): pass

    @abstractmethod
    def getReceptionistOfBranch(self): pass