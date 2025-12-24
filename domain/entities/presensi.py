class Presensi:
    def __init__(self, id_presensi, mata_kuliah, dosen, tanggal):
        self.id_presensi = id_presensi
        self.mata_kuliah = mata_kuliah   # objek MataKuliah
        self.dosen = dosen               # objek Dosen
        self.tanggal = tanggal
        self.daftar_hadir = []           # list Mahasiswa

    def isi_hadir(self, mahasiswa):
        if mahasiswa not in self.daftar_hadir:
            self.daftar_hadir.append(mahasiswa)

    def info(self):
        return f"ID {self.id_presensi} - {self.mata_kuliah.nama_mk} - {self.tanggal}"
