# ============================
# KELAS USER & TURUNANNYA
# ============================

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


class Login:
    def __init__(self, identifier, password):
        self.identifier = identifier  # NIM / NIDN / username admin
        self.password = password
        self.role = None

    def determine_role(self):
        # 9 digit angka  -> mahasiswa (NIM)
        # 8 digit angka  -> dosen (NIDN)
        # lainnya        -> admin (username)
        if self.identifier.isdigit() and len(self.identifier) == 9:
            self.role = 'mahasiswa'
        elif self.identifier.isdigit() and len(self.identifier) == 8:
            self.role = 'dosen'
        else:
            self.role = 'admin'
        return self.role

    def validate_input(self):
        if not self.identifier or not self.password:
            raise ValueError("Identifier dan password tidak boleh kosong.")
        if len(self.password) < 6:
            raise ValueError("Password minimal 6 karakter.")


class Admin(User):
    def __init__(self, id, nama, email, password, username):
        super().__init__(id, nama, email, password)
        self.role = 'admin'
        self.username = username


class Mahasiswa(User):
    def __init__(self, id, nama, email, password, nim, prodi):
        super().__init__(id, nama, email, password)
        self.role = 'mahasiswa'
        self.nim = nim
        self.prodi = prodi


class Dosen(User):
    def __init__(self, id, nama, email, password, nidn, departemen):
        super().__init__(id, nama, email, password)
        self.role = 'dosen'
        self.nidn = nidn
        self.departemen = departemen

