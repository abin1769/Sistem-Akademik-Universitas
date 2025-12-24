class KRS:
    def __init__(self, mahasiswa, semester, tahun_ajaran, id_krs=None):
        self.id_krs = id_krs
        self.mahasiswa = mahasiswa    # objek Mahasiswa
        self.semester = semester
        self.tahun_ajaran = tahun_ajaran
        self.daftar_mk = []           # list MataKuliah

    def tambah_mk(self, mk):
        # CEK: jangan sampai 1 MK diambil 2 kali
        if mk in self.daftar_mk:
            print(f"Mata kuliah {mk.kode_mk} sudah ada di KRS, tidak dapat diambil dua kali.")
            return False
        self.daftar_mk.append(mk)
        return True

    def hitung_total_sks(self):
        return sum(mk.sks for mk in self.daftar_mk)

    def tampilkan_krs(self):
        print(f"\nKRS {self.mahasiswa.nama} - Semester {self.semester} ({self.tahun_ajaran})")
        if not self.daftar_mk:
            print("Belum ada mata kuliah yang diambil.")
            return
        for i, mk in enumerate(self.daftar_mk, start=1):
            print(f"{i}. {mk.info()}")
        print("Total SKS:", self.hitung_total_sks())
