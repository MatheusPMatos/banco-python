from user_repository import UserRepository

class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = [{"id":1,"name":"Alice"},{"id":2,"name":"Bob"}]

    def get_all_users(self) -> list[dict]:
        return self.users

    def get_user_by_id(self, user_id: int) -> dict:
        for u in self.users:
            if u["id"] == user_id:
                return u
        return None
