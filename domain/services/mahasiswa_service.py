"""
domain/services/mahasiswa_service.py
Service layer untuk logika bisnis spesifik Mahasiswa.
Menangani KRS, Presensi, dan Nilai.
"""

from domain.entities.krs import KRS
from domain.entities.presensi import Presensi
from domain.entities.nilai import Nilai


class MahasiswaServiceError(Exception):
    """Custom exception untuk MahasiswaService"""
    pass


class MahasiswaService:
    """
    Business logic untuk mahasiswa.
    Menangani operasi: KRS, Presensi, Nilai.
    """
    
    def __init__(self, state):
        """
        Args:
            state: AppState object yang berisi daftar data (daftar_krs, daftar_presensi, dll)
        """
        if state is None:
            raise MahasiswaServiceError("state tidak boleh None")
        self.state = state

    # ============ KRS Operations ============
    
    def ambil_krs(self, mahasiswa, daftar_mk, semester=1, tahun_ajaran="2024/2025"):
        """
        Ambil KRS untuk mahasiswa.
        
        Args:
            mahasiswa: Objek Mahasiswa
            daftar_mk: List MataKuliah yang ingin diambil
            semester: Semester (default 1)
            tahun_ajaran: Tahun akademik (default "2024/2025")
        
        Returns:
            KRS object yang baru dibuat
        
        Raises:
            MahasiswaServiceError: Jika validation gagal
        """
        if not mahasiswa:
            raise MahasiswaServiceError("Mahasiswa tidak boleh kosong")
        if not daftar_mk:
            raise MahasiswaServiceError("Minimal harus ambil 1 mata kuliah")
        
        # Hitung total SKS
        total_sks = sum(mk.sks for mk in daftar_mk)
        if total_sks > 24:
            raise MahasiswaServiceError("Maksimal mata kuliah 24 SKS")
        
        # Cek apakah sudah punya KRS
        krs_existing = self.cari_krs_by_mahasiswa(mahasiswa)
        if krs_existing:
            raise MahasiswaServiceError(f"Mahasiswa {mahasiswa.nama} sudah punya KRS")
        
        krs = KRS(mahasiswa, semester, tahun_ajaran)
        for mk in daftar_mk:
            krs.tambah_mk(mk)
        self.state.daftar_krs.append(krs)
        return krs
    
    def cari_krs_by_mahasiswa(self, mahasiswa):
        """Cari KRS berdasarkan mahasiswa"""
        for k in self.state.daftar_krs:
            if k.mahasiswa == mahasiswa:
                return k
        return None
    
    def lihat_krs(self, mahasiswa):
        """Lihat KRS dan detail mata kuliah"""
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs:
            return None
        return {
            'mahasiswa': mahasiswa,
            'daftar_mk': krs.daftar_mk,
            'total_sks': sum(mk.sks for mk in krs.daftar_mk)
        }
    
    def hapus_krs(self, mahasiswa, mata_kuliah):
        """Hapus mata kuliah dari KRS"""
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs:
            raise MahasiswaServiceError("Mahasiswa tidak punya KRS")
        if mata_kuliah not in krs.daftar_mk:
            raise MahasiswaServiceError("Mata kuliah tidak ada di KRS")
        if len(krs.daftar_mk) <= 1:
            raise MahasiswaServiceError("Minimal harus ada 1 mata kuliah")
        
        krs.daftar_mk.remove(mata_kuliah)
        return krs

    # ============ Presensi Operations ============
    
    def lihat_presensi_tersedia(self, mahasiswa):
        """
        Lihat daftar presensi yang tersedia untuk mahasiswa.
        Hanya presensi dari mata kuliah yang diambil di KRS.
        """
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs:
            return []
        
        mk_di_krs = set(krs.daftar_mk)
        hasil = []
        for p in self.state.daftar_presensi:
            # Hanya jika mata kuliah ada di KRS dan belum hadir
            if p.mata_kuliah in mk_di_krs and mahasiswa not in p.daftar_hadir:
                hasil.append(p)
        return hasil
    
    def ambil_presensi(self, mahasiswa, presensi_obj):
        """
        Mahasiswa ambil presensi untuk suatu mata kuliah.
        
        Raises:
            MahasiswaServiceError: Jika validation gagal
        """
        if not presensi_obj:
            raise MahasiswaServiceError("Presensi tidak valid")
        
        # Cek apakah mahasiswa ada di KRS untuk mata kuliah ini
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs or presensi_obj.mata_kuliah not in krs.daftar_mk:
            raise MahasiswaServiceError(
                f"Mahasiswa tidak terdaftar di {presensi_obj.mata_kuliah.nama}"
            )
        
        # Cek apakah sudah pernah hadir
        if mahasiswa in presensi_obj.daftar_hadir:
            raise MahasiswaServiceError("Anda sudah absen untuk perkuliahan ini")
        
        presensi_obj.daftar_hadir.append(mahasiswa)
        return presensi_obj
    
    def lihat_presensi_history(self, mahasiswa):
        """Lihat riwayat presensi mahasiswa"""
        history = []
        for p in self.state.daftar_presensi:
            if mahasiswa in p.daftar_hadir:
                history.append({
                    'mata_kuliah': p.mata_kuliah.nama,
                    'dosen': p.dosen.nama,
                    'tanggal': p.tanggal
                })
        return history

    # ============ Nilai Operations ============
    
    def lihat_nilai(self, mahasiswa):
        """Lihat daftar nilai mahasiswa"""
        nilai_list = []
        for n in self.state.daftar_nilai:
            if n.mahasiswa == mahasiswa:
                nilai_list.append({
                    'mata_kuliah': n.mata_kuliah.nama,
                    'nilai_angka': n.nilai_angka,
                    'nilai_huruf': n.nilai_huruf,
                    'dosen': n.dosen.nama
                })
        return nilai_list
    
    def hitung_ipk(self, mahasiswa):
        """Hitung IPK mahasiswa"""
        nilai_list = self.lihat_nilai(mahasiswa)
        if not nilai_list:
            return 0.0
        
        total_bobot = 0
        total_sks = 0
        
        for n_info in nilai_list:
            # Cari mata kuliah untuk dapat SKS
            mk = self._cari_mata_kuliah(n_info['mata_kuliah'])
            if mk:
                bobot = self._huruf_to_bobot(n_info['nilai_huruf'])
                total_bobot += bobot * mk.sks
                total_sks += mk.sks
        
        if total_sks == 0:
            return 0.0
        return round(total_bobot / total_sks, 2)

    # ============ Helper Methods ============
    
    def _cari_mata_kuliah(self, nama_mk):
        """Cari mata kuliah berdasarkan nama"""
        for mk in self.state.daftar_mk:
            if mk.nama == nama_mk:
                return mk
        return None
    
    def _huruf_to_bobot(self, huruf):
        """Konversi nilai huruf ke bobot angka"""
        mapping = {
            'A': 4.0, 'A-': 3.7,
            'B+': 3.3, 'B': 3.0, 'B-': 2.7,
            'C+': 2.3, 'C': 2.0, 'C-': 1.7,
            'D+': 1.3, 'D': 1.0,
            'E': 0.0
        }
        return mapping.get(huruf, 0.0)

    # ============ Validation Methods ============
    
    def validasi_ambil_krs(self, mahasiswa, daftar_mk):
        """Validasi sebelum ambil KRS"""
        errors = []
        
        if not mahasiswa:
            errors.append("Mahasiswa harus dipilih")
        if not daftar_mk:
            errors.append("Minimal pilih 1 mata kuliah")
        elif len(daftar_mk) > 24:
            errors.append("Maksimal 24 SKS")
        
        if self.cari_krs_by_mahasiswa(mahasiswa):
            errors.append("Mahasiswa sudah punya KRS")
        
        return errors
