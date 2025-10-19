from user_service import UserService

class UserController:
    def __init__(self, service: UserService):
        self.service = service

    def get_users(self):
        try:
            return self.service.list_users()
        except Exception as e:
            return {"status": "error", "message": str(e)}

    def get_user(self, user_id: int):
        try:
            user = self.service.find_user(user_id)
            if user:
                return {"status":"success","user":user}
            return {"status":"error","message":"User not found"}
        except Exception as e:
            return {"status":"error","message": str(e)}
  