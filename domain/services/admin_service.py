"""
services/admin_service.py
Service layer untuk logika bisnis spesifik Admin.
Menangani manajemen Mata Kuliah.
"""


class AdminServiceError(Exception):
    """Custom exception untuk AdminService"""
    pass


class AdminService:
    """
    Business logic untuk admin.
    Menangani operasi: Mata Kuliah management.
    """
    
    def __init__(self, state):
        """
        Args:
            state: AppState object yang berisi daftar data
        """
        if state is None:
            raise AdminServiceError("state tidak boleh None")
        self.state = state

    # ============ Mata Kuliah Operations ============
    
    def lihat_semua_mata_kuliah(self):
        """Lihat semua mata kuliah yang tersedia"""
        return self.state.daftar_mk
    
    def cari_mata_kuliah_by_kode(self, kode_mk):
        """
        Cari mata kuliah berdasarkan kode.
        
        Args:
            kode_mk: Kode mata kuliah
        
        Returns:
            Mata Kuliah object atau None
        """
        for mk in self.state.daftar_mk:
            if mk.kode_mk == kode_mk:
                return mk
        return None
    
    def tambah_mata_kuliah(self, kode_mk, nama, sks, deskripsi=""):
        """
        Tambah mata kuliah baru.
        
        Args:
            kode_mk: Kode mata kuliah (unique)
            nama: Nama mata kuliah
            sks: Jumlah SKS (1-4)
            deskripsi: Deskripsi (optional)
        
        Returns:
            Mata Kuliah object yang baru dibuat
        
        Raises:
            AdminServiceError: Jika validation gagal
        """
        from domain.entities.matakuliah import MataKuliah
        
        # Validasi kode unik
        if self.cari_mata_kuliah_by_kode(kode_mk):
            raise AdminServiceError(f"Kode mata kuliah {kode_mk} sudah ada")
        
        # Validasi input
        if not nama:
            raise AdminServiceError("Nama mata kuliah tidak boleh kosong")
        
        if not isinstance(sks, int) or sks < 1 or sks > 4:
            raise AdminServiceError("SKS harus antara 1-4")
        
        # Buat mata kuliah baru
        mk = MataKuliah(kode_mk, nama, sks, deskripsi)
        self.state.daftar_mk.append(mk)
        return mk
    
    def edit_mata_kuliah(self, kode_mk, nama=None, sks=None, deskripsi=None):
        """
        Edit mata kuliah yang sudah ada.
        
        Args:
            kode_mk: Kode mata kuliah
            nama: Nama baru (optional)
            sks: SKS baru (optional)
            deskripsi: Deskripsi baru (optional)
        
        Returns:
            Mata Kuliah object yang sudah diedit
        
        Raises:
            AdminServiceError: Jika tidak ditemukan atau validation gagal
        """
        mk = self.cari_mata_kuliah_by_kode(kode_mk)
        if not mk:
            raise AdminServiceError(f"Mata kuliah {kode_mk} tidak ditemukan")
        
        # Update field yang diberikan
        if nama:
            mk.nama = nama
        
        if sks is not None:
            if not isinstance(sks, int) or sks < 1 or sks > 4:
                raise AdminServiceError("SKS harus antara 1-4")
            mk.sks = sks
        
        if deskripsi is not None:
            mk.deskripsi = deskripsi
        
        return mk
    
    def hapus_mata_kuliah(self, kode_mk):
        """
        Hapus mata kuliah (dengan validasi).
        
        Args:
            kode_mk: Kode mata kuliah
        
        Raises:
            AdminServiceError: Jika tidak ditemukan atau sedang digunakan
        """
        mk = self.cari_mata_kuliah_by_kode(kode_mk)
        if not mk:
            raise AdminServiceError(f"Mata kuliah {kode_mk} tidak ditemukan")
        
        # Cek apakah mata kuliah sudah digunakan di KRS
        if any(mk in krs.daftar_mk for krs in self.state.daftar_krs):
            raise AdminServiceError(
                f"Mata kuliah {kode_mk} tidak bisa dihapus karena sudah digunakan di KRS"
            )
        
        self.state.daftar_mk.remove(mk)

    # ============ Statistic Operations ============
    
    def hitung_total_mahasiswa(self):
        """Hitung total jumlah mahasiswa"""
        return len(self.state.daftar_mahasiswa)
    
    def hitung_total_dosen(self):
        """Hitung total jumlah dosen"""
        return len(self.state.daftar_dosen)
    
    def hitung_total_mata_kuliah(self):
        """Hitung total jumlah mata kuliah"""
        return len(self.state.daftar_mk)
    
    def lihat_statistik_sistem(self):
        """Lihat ringkasan statistik sistem"""
        return {
            'total_mahasiswa': self.hitung_total_mahasiswa(),
            'total_dosen': self.hitung_total_dosen(),
            'total_mata_kuliah': self.hitung_total_mata_kuliah(),
            'total_krs': len(self.state.daftar_krs),
            'total_presensi': len(self.state.daftar_presensi),
            'total_nilai': len(self.state.daftar_nilai)
        }

    # ============ Validation Methods ============
    
    def validasi_tambah_mata_kuliah(self, kode_mk, nama, sks):
        """Validasi sebelum tambah mata kuliah"""
        errors = []
        
        if not kode_mk:
            errors.append("Kode mata kuliah tidak boleh kosong")
        elif self.cari_mata_kuliah_by_kode(kode_mk):
            errors.append(f"Kode mata kuliah {kode_mk} sudah ada")
        
        if not nama:
            errors.append("Nama mata kuliah tidak boleh kosong")
        
        if sks is None:
            errors.append("SKS harus diisi")
        elif not isinstance(sks, int) or sks < 1 or sks > 4:
            errors.append("SKS harus antara 1-4")
        
        return errors
    
    def validasi_edit_mata_kuliah(self, kode_mk, sks=None):
        """Validasi sebelum edit mata kuliah"""
        errors = []
        
        mk = self.cari_mata_kuliah_by_kode(kode_mk)
        if not mk:
            errors.append(f"Mata kuliah {kode_mk} tidak ditemukan")
        
        if sks is not None:
            if not isinstance(sks, int) or sks < 1 or sks > 4:
                errors.append("SKS harus antara 1-4")
        
        return errors
