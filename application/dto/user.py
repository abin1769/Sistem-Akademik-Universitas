class User:
    def __init__(self, id, nama, email, password): #Menginisialisasi
        self.id = id
        self.nama = nama
        self.__email = email
        self.__password = password
        self.role = 'user'

    @property
    def email(self):
        """Getter untuk email"""
        return self.__email
    
    @property
    def password(self):
        """Getter untuk password"""
        return self.__password

    def tampilkan_profil(self):
        print(f"ID      : {self.id}")
        print(f"Nama    : {self.nama}")
        print(f"Email   : {self.email}")
        print(f"Role    : {self.role}")
