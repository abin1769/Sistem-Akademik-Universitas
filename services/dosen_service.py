"""
services/dosen_service.py
Service layer untuk logika bisnis spesifik Dosen.
Menangani Presensi dan Nilai.
"""

from akademik.presensi import Presensi
from akademik.nilai import Nilai


class DosenServiceError(Exception):
    """Custom exception untuk DosenService"""
    pass


class DosenService:
    """
    Business logic untuk dosen.
    Menangani operasi: Presensi dan Nilai.
    """
    
    def __init__(self, state):
        """
        Args:
            state: AppState object yang berisi daftar data
        """
        if state is None:
            raise DosenServiceError("state tidak boleh None")
        self.state = state

    # ============ Presensi Operations ============
    
    def lihat_presensi_by_dosen(self, dosen):
        """
        Lihat semua presensi yang dibuat oleh dosen.
        
        Args:
            dosen: Objek Dosen
        
        Returns:
            List of Presensi objects
        """
        return [p for p in self.state.daftar_presensi if p.dosen == dosen]
    
    def buat_presensi(self, dosen, mata_kuliah, tanggal):
        """
        Buat presensi baru untuk suatu mata kuliah.
        
        Args:
            dosen: Objek Dosen
            mata_kuliah: Objek MataKuliah
            tanggal: String tanggal (format YYYY-MM-DD)
        
        Returns:
            Presensi object yang baru dibuat
        
        Raises:
            DosenServiceError: Jika validation gagal
        """
        if not dosen:
            raise DosenServiceError("Dosen tidak boleh kosong")
        if not mata_kuliah:
            raise DosenServiceError("Mata kuliah tidak boleh kosong")
        if not tanggal:
            raise DosenServiceError("Tanggal tidak boleh kosong")
        
        # Cek apakah sudah ada presensi untuk tanggal yang sama
        existing = any(
            p.dosen == dosen and p.mata_kuliah == mata_kuliah and p.tanggal == tanggal
            for p in self.state.daftar_presensi
        )
        if existing:
            raise DosenServiceError(
                f"Presensi untuk {mata_kuliah.nama} pada {tanggal} sudah dibuat"
            )
        
        presensi = Presensi(
            id=self.state.next_id_presensi,
            dosen=dosen,
            mata_kuliah=mata_kuliah,
            tanggal=tanggal
        )
        self.state.next_id_presensi += 1
        self.state.daftar_presensi.append(presensi)
        return presensi
    
    def lihat_mahasiswa_hadir(self, presensi_obj):
        """Lihat daftar mahasiswa yang hadir untuk suatu presensi"""
        if not presensi_obj:
            raise DosenServiceError("Presensi tidak valid")
        return presensi_obj.daftar_hadir
    
    def lihat_presensi_summary(self, dosen):
        """
        Lihat ringkasan presensi yang dibuat dosen.
        
        Returns:
            List of dict dengan info presensi
        """
        presensi_list = self.lihat_presensi_by_dosen(dosen)
        summary = []
        
        for p in presensi_list:
            summary.append({
                'mata_kuliah': p.mata_kuliah.nama,
                'tanggal': p.tanggal,
                'jumlah_hadir': len(p.daftar_hadir)
            })
        
        return summary

    # ============ Nilai Operations ============
    
    def input_nilai(self, dosen, mahasiswa, mata_kuliah, nilai_angka):
        """
        Input nilai untuk mahasiswa.
        
        Args:
            dosen: Objek Dosen
            mahasiswa: Objek Mahasiswa
            mata_kuliah: Objek MataKuliah
            nilai_angka: Nilai angka (0-100)
        
        Returns:
            Nilai object
        
        Raises:
            DosenServiceError: Jika validation gagal
        """
        if not dosen:
            raise DosenServiceError("Dosen tidak boleh kosong")
        if not mahasiswa:
            raise DosenServiceError("Mahasiswa tidak boleh kosong")
        if not mata_kuliah:
            raise DosenServiceError("Mata kuliah tidak boleh kosong")
        
        # Validasi nilai
        if not isinstance(nilai_angka, (int, float)):
            raise DosenServiceError("Nilai harus berupa angka")
        if nilai_angka < 0 or nilai_angka > 100:
            raise DosenServiceError("Nilai harus antara 0-100")
        
        # Cek apakah nilai sudah ada
        existing = next(
            (n for n in self.state.daftar_nilai
             if n.mahasiswa == mahasiswa and n.mata_kuliah == mata_kuliah),
            None
        )
        if existing:
            # Update nilai yang ada
            existing.nilai_angka = nilai_angka
            return existing
        
        # Buat nilai baru
        nilai = Nilai(dosen, mata_kuliah, mahasiswa, nilai_angka)
        self.state.daftar_nilai.append(nilai)
        return nilai
    
    def lihat_nilai_by_dosen(self, dosen):
        """Lihat semua nilai yang diinput oleh dosen"""
        return [n for n in self.state.daftar_nilai if n.dosen == dosen]
    
    def lihat_nilai_mata_kuliah(self, dosen, mata_kuliah):
        """
        Lihat nilai untuk suatu mata kuliah yang diampu dosen.
        
        Returns:
            List of dict dengan info nilai
        """
        nilai_list = [
            n for n in self.lihat_nilai_by_dosen(dosen)
            if n.mata_kuliah == mata_kuliah
        ]
        
        summary = []
        for n in nilai_list:
            summary.append({
                'mahasiswa': n.mahasiswa.nama,
                'nim': n.mahasiswa.nim,
                'nilai_angka': n.nilai_angka,
                'nilai_huruf': n.nilai_huruf
            })
        
        return summary
    
    def hitung_rata_rata_kelas(self, dosen, mata_kuliah):
        """Hitung rata-rata nilai kelas untuk suatu mata kuliah"""
        nilai_list = self.lihat_nilai_mata_kuliah(dosen, mata_kuliah)
        
        if not nilai_list:
            return 0.0
        
        total = sum(n['nilai_angka'] for n in nilai_list)
        return round(total / len(nilai_list), 2)

    # ============ Validation Methods ============
    
    def validasi_buat_presensi(self, dosen, mata_kuliah, tanggal):
        """Validasi sebelum buat presensi"""
        errors = []
        
        if not dosen:
            errors.append("Dosen harus dipilih")
        if not mata_kuliah:
            errors.append("Mata kuliah harus dipilih")
        if not tanggal:
            errors.append("Tanggal harus dipilih")
        
        return errors
    
    def validasi_input_nilai(self, mahasiswa, mata_kuliah, nilai_angka):
        """Validasi sebelum input nilai"""
        errors = []
        
        if not mahasiswa:
            errors.append("Mahasiswa harus dipilih")
        if not mata_kuliah:
            errors.append("Mata kuliah harus dipilih")
        
        try:
            nilai = float(nilai_angka)
            if nilai < 0 or nilai > 100:
                errors.append("Nilai harus antara 0-100")
        except (ValueError, TypeError):
            errors.append("Nilai harus berupa angka")
        
        return errors
