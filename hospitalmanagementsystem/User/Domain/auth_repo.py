from abc import ABC, abstractmethod
from typing import Dict, Optional

class IAuthRepository(ABC):

    @abstractmethod
    def signUp(self, username: str, email: str, password: str, role_name: str, ip, device, location) -> Dict: pass

    @abstractmethod
    def login(self, email: str, password: str, ip, device, location) -> Optional[Dict]: pass

    @abstractmethod
    def logout(self, refresh_token: str) -> None: pass