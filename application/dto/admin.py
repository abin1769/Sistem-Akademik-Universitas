from .user import User

class Admin(User):
    def __init__(self, id, nama, email, password, username):
        super().__init__(id, nama, email, password)
        self.role = 'admin'
        self.username = username