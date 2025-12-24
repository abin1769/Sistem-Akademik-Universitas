class MataKuliah:
    def __init__(self, kode_mk, nama_mk, sks, dosen=None):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks
        self.dosen = dosen  # objek Dosen

    def info(self):
        dosen_nama = self.dosen.nama if self.dosen else "Belum ada dosen"
        return f"{self.kode_mk} - {self.nama_mk} ({self.sks} SKS) - Dosen: {dosen_nama}"