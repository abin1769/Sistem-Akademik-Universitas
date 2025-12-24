# services/akademik_service.py
class AkademikService:
    def __init__(self, state):
        self.state = state

    def cari_mahasiswa_by_nim(self, nim):
        for m in self.state.daftar_mahasiswa:
            if m.nim == nim:
                return m
        return None

    def cari_dosen_by_nidn(self, nidn):
        for d in self.state.daftar_dosen:
            if d.nidn == nidn:
                return d
        return None

    def cari_krs_by_mahasiswa(self, mahasiswa):
        for k in self.state.daftar_krs:
            if k.mahasiswa == mahasiswa:
                return k
        return None

    def presensi_by_dosen(self, dosen):
        return [p for p in self.state.daftar_presensi if p.dosen == dosen]

    def presensi_tersedia_untuk_mahasiswa(self, mahasiswa):
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs:
            return []
        mk_di_krs = set(krs.daftar_mk)
        hasil = []
        for p in self.state.daftar_presensi:
            if p.mata_kuliah in mk_di_krs and mahasiswa not in p.daftar_hadir:
                hasil.append(p)
        return hasil

    def nilai_mahasiswa(self, mahasiswa):
        return [n for n in self.state.daftar_nilai if n.mahasiswa == mahasiswa]
