# app.py
"""
Main application orchestrator.
Menangani initialization, dependency injection, dan routing ke menu.
"""

from db import get_connection
from user.login import Login
from loaders.db_loaders import DBLoader
from services.akademik_services import AkademikService
from services.mahasiswa_service import MahasiswaService
from menus.AdminMenu import AdminMenu
from menus.MahasiswaMenu import MahasiswaMenu
from menus.DosenMenu import DosenMenu


class AppState:
    """
    Application state management.
    Menyimpan semua data yang dimuat dari database.
    """
    def __init__(self):
        self.daftar_admin = []
        self.daftar_mahasiswa = []
        self.daftar_dosen = []
        self.daftar_mk = []
        self.daftar_krs = []
        self.daftar_presensi = []
        self.daftar_nilai = []
        self.next_id_presensi = 1
        self.dosen_by_id = {}
        self.mahasiswa_by_id = {}
        self.mk_by_id = {}
        self.krs_by_id = {}


class SistemAkademik:
    """
    Main application orchestrator.
    Menangani initialization, dependency injection, dan menu routing.
    """
    
    def __init__(self):
        """Initialize application dan load data dari database"""
        self.state = AppState()
        self.conn = self._initialize_database()
        self._setup_services()
        self._setup_menus()

    def _initialize_database(self):
        """
        Initialize database connection dan load data.
        
        Returns:
            Database connection object atau None jika gagal
        """
        conn = get_connection()

        if conn:
            try:
                DBLoader(conn).load_all(self.state)
                print("[OK] Data berhasil dimuat dari database")
            except Exception as e:
                print(f"[WARNING] Gagal load data: {str(e)}")
        else:
            print("[WARNING] Gagal koneksi ke database. Data hanya ada di memori.")
        
        return conn

    def _setup_services(self):
        """Setup service layer dengan dependency injection"""
        self.akademik_service = AkademikService(self.state)
        self.mahasiswa_service = MahasiswaService(self.state)

    def _setup_menus(self):
        """Setup menu dengan dependency injection"""
        self.admin_menu = AdminMenu(self.state, self.akademik_service, self.conn)
        self.mhs_menu = MahasiswaMenu(self.state, self.akademik_service, self.conn)
        self.dosen_menu = DosenMenu(self.state, self.akademik_service, self.conn)

    def login(self):
        """
        Handle login process.
        Validate credentials dan route ke menu yang sesuai.
        """
        identifier = input("\nMasukkan NIM / NIDN / Username Admin: ")
        password = input("Masukkan password: ")

        login_obj = Login(identifier, password)
        
        try:
            login_obj.validate_input()
            role = login_obj.determine_role()
        except Exception as e:
            print(f"[ERROR] {str(e)}")
            return

        # Route ke menu berdasarkan role
        if role == "mahasiswa":
            self._login_mahasiswa(identifier, password)
        elif role == "dosen":
            self._login_dosen(identifier, password)
        else:
            self._login_admin(identifier, password)

    def _login_mahasiswa(self, nim, password):
        """Login handler untuk mahasiswa"""
        mhs = self.akademik_service.cari_mahasiswa_by_nim(nim)
        
        if mhs and mhs.password == password:
            print(f"\n[OK] Login berhasil. Selamat datang, {mhs.nama}!")
            self.mhs_menu.run(mhs)
        else:
            print("[ERROR] Mahasiswa tidak ditemukan atau password salah")

    def _login_dosen(self, nidn, password):
        """Login handler untuk dosen"""
        dosen = self.akademik_service.cari_dosen_by_nidn(nidn)
        
        if dosen and dosen.password == password:
            print(f"\n[OK] Login berhasil. Selamat datang, {dosen.nama}!")
            self.dosen_menu.run(dosen)
        else:
            print("[ERROR] Dosen tidak ditemukan atau password salah")

    def _login_admin(self, username, password):
        """Login handler untuk admin"""
        admin = next(
            (a for a in self.state.daftar_admin
             if a.username == username and a.password == password),
            None
        )
        
        if admin:
            print(f"\n[OK] Login berhasil. Selamat datang, Admin {admin.username}!")
            self.admin_menu.run(admin)
        else:
            print("[ERROR] Admin tidak ditemukan atau password salah")

