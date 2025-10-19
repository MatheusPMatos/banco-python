from user_repository_impl import UserRepository
from model.forma import Logger

class UserService:
    def __init__(self, repo: UserRepository, logger: Logger):
        self.repo = repo
        self.logger = logger

    def list_users(self):
        self.logger.log("Listando usuários")
        return self.repo.get_all_users()

    def find_user(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            self.logger.warn(f"Usuário {user_id} não encontrado")
        return user