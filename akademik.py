# ============================
# KELAS AKADEMIK
# ============================

class MataKuliah:
    def __init__(self, kode_mk, nama_mk, sks, dosen=None):
        self.kode_mk = kode_mk
        self.nama_mk = nama_mk
        self.sks = sks
        self.dosen = dosen  # objek Dosen

    def info(self):
        dosen_nama = self.dosen.nama if self.dosen else "Belum ada dosen"
        return f"{self.kode_mk} - {self.nama_mk} ({self.sks} SKS) - Dosen: {dosen_nama}"


class KRS:
    def __init__(self, mahasiswa, semester, tahun_ajaran):
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


# ============================
# KELAS PRESENSI
# ============================

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


# ============================
# KELAS NILAI
# ============================

class Nilai:
    def __init__(self, mahasiswa, mata_kuliah, nilai_angka):
        self.mahasiswa = mahasiswa      # objek Mahasiswa
        self.mata_kuliah = mata_kuliah  # objek MataKuliah
        self.nilai_angka = nilai_angka
        self.nilai_huruf = self.konversi_huruf()

    def konversi_huruf(self):
        n = self.nilai_angka
        if n >= 85:
            return "A"
        elif n >= 75:
            return "B"
        elif n >= 65:
            return "C"
        elif n >= 55:
            return "D"
        else:
            return "E"

    def info(self):
        return f"{self.mata_kuliah.kode_mk} - {self.mata_kuliah.nama_mk}: {self.nilai_angka} ({self.nilai_huruf})"

