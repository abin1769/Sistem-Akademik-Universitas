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

