from abc import ABC, abstractmethod
from typing import List

class UserRepository(ABC):
    @abstractmethod
    def get_all_users(self) -> List[dict]:
        pass

    @abstractmethod
    def get_user_by_id(self, user_id: int) -> dict:
        pass
