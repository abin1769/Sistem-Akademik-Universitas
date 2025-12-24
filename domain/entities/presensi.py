class Presensi:
    def __init__(
        self,
        id=None,
        mata_kuliah=None,
        dosen=None,
        tanggal=None,
        id_presensi=None,
    ):
        self.id = id if id is not None else id_presensi
        self.id_presensi = self.id
        self.mata_kuliah = mata_kuliah   # objek MataKuliah
        self.dosen = dosen               # objek Dosen
        self.tanggal = tanggal
        self.daftar_hadir = []           # list Mahasiswa

    def isi_hadir(self, mahasiswa):
        if mahasiswa not in self.daftar_hadir:
            self.daftar_hadir.append(mahasiswa)

    def info(self):
        mk_nama = getattr(self.mata_kuliah, "nama_mk", getattr(self.mata_kuliah, "nama", ""))
        return f"ID {self.id_presensi} - {mk_nama} - {self.tanggal}"
