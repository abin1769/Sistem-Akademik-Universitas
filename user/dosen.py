from .user import User

class Dosen(User):
    def __init__(self, id, nama, email, password, nidn, departemen):
        super().__init__(id, nama, email, password)
        self.role = 'dosen'
        self.nidn = nidn
        self.departemen = departemen