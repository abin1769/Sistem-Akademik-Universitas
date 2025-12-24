class Nilai:
    def __init__(self, *args, **kwargs):
        """
        Bentuk yang didukung:
        - Nilai(dosen, mata_kuliah, mahasiswa, nilai_angka)
        - Nilai(mahasiswa, mata_kuliah, nilai_angka)  (legacy)
        """

        dosen = kwargs.pop("dosen", None)
        mata_kuliah = kwargs.pop("mata_kuliah", None)
        mahasiswa = kwargs.pop("mahasiswa", None)
        nilai_angka = kwargs.pop("nilai_angka", None)
        nilai_huruf = kwargs.pop("nilai_huruf", None)

        if args:
            if len(args) == 4:
                dosen, mata_kuliah, mahasiswa, nilai_angka = args
            elif len(args) == 3:
                mahasiswa, mata_kuliah, nilai_angka = args
            else:
                raise TypeError("Nilai() menerima 3 atau 4 argumen posisi")

        if mata_kuliah is None or mahasiswa is None:
            raise ValueError("mata_kuliah dan mahasiswa wajib diisi")

        if dosen is None:
            dosen = getattr(mata_kuliah, "dosen", None)

        self.dosen = dosen
        self.mahasiswa = mahasiswa      # objek Mahasiswa
        self.mata_kuliah = mata_kuliah  # objek MataKuliah
        self.nilai_angka = float(nilai_angka)
        self.nilai_huruf = nilai_huruf or self.konversi_huruf()

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

