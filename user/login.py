class Login:
    def __init__(self, identifier, password):
        self.identifier = identifier          # public
        self.__password = password             # PRIVATE
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
        if not self.identifier or not self.__password:
            raise ValueError("Identifier dan password tidak boleh kosong.")
        if len(self.__password) < 6:
            raise ValueError("Password minimal 6 karakter.")
