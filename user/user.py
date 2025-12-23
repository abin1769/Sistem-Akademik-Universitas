

class User:
    def __init__(self, id, nama, email, password): #Menginisialisasi
        self.id = id
        self.nama = nama
        self.email = email
        self.password = password
        self.role = 'user'

    def tampilkan_profil(self):
        print(f"ID      : {self.id}")
        print(f"Nama    : {self.nama}")
        print(f"Email   : {self.email}")
        print(f"Role    : {self.role}")
