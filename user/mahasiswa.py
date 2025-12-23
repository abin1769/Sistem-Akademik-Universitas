from .user import User

class Mahasiswa(User):
    def __init__(self, id, nama, email, password, nim, prodi):
        super().__init__(id, nama, email, password)
        self.role = 'mahasiswa'
        self.nim = nim
        self.prodi = prodi
