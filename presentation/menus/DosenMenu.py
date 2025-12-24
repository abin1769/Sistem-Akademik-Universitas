"""
presentation/menus/DosenMenu.py
Menu untuk dosen.
Menampilkan menu operasi: Presensi dan Nilai.
"""

from datetime import datetime
from infrastructure.repositories import NilaiRepository
from domain.entities.presensi import Presensi
from domain.entities.nilai import Nilai
from presentation.ui.menu_ui_helper import MenuDisplay, MenuInputValidator, MenuUI
from domain.services.dosen_service import DosenService, DosenServiceError
from domain.entities.grading_strategy import GradingFactory


class DosenMenu:
    """Menu interface untuk dosen"""
    
    def __init__(self, state, service, conn):
        """
        Args:
            state: AppState object
            service: AkademikService atau DosenService
            conn: Database connection
        """
        self.state = state
        self.service = service
        self.conn = conn
        self.dosen_service = DosenService(state)
        self.grading_strategy = GradingFactory.create_strategy('standard')
        self.nilai_repo = NilaiRepository(conn) if conn else None

    def run(self, dosen):
        """
        Main menu loop untuk dosen.
        
        Args:
            dosen: Objek Dosen yang login
        """
        while True:
            self._display_menu(dosen)
            pilih = MenuInputValidator.get_string("Pilihan: ")

            try:
                if pilih == "1":
                    self._lihat_profil(dosen)
                elif pilih == "2":
                    self._lihat_mata_kuliah_diampu(dosen)
                elif pilih == "3":
                    self._buat_presensi(dosen)
                elif pilih == "4":
                    self._lihat_daftar_presensi(dosen)
                elif pilih == "5":
                    self._input_nilai(dosen)
                elif pilih == "0":
                    print("Logout dosen...")
                    break
                else:
                    MenuDisplay.error("Pilihan tidak valid")
            except DosenServiceError as e:
                MenuDisplay.error(str(e))
            except Exception as e:
                MenuDisplay.error(f"Terjadi kesalahan: {str(e)}")

    def _display_menu(self, dosen):
        """Tampilkan menu utama dosen"""
        MenuDisplay.header(f"MENU DOSEN ({dosen.nama})")
        print("1. Lihat profil")
        print("2. Lihat mata kuliah diampu")
        print("3. Buat presensi")
        print("4. Lihat daftar presensi")
        print("5. Input nilai mahasiswa")
        print("0. Logout")

    def _lihat_profil(self, dosen):
        """Menampilkan profil dosen"""
        MenuDisplay.subheader("Profil Dosen")
        dosen.tampilkan_profil()
        print(f"NIDN      : {dosen.nidn}")
        print(f"Departemen: {dosen.departemen}")
        MenuDisplay.pause()

    def _lihat_mata_kuliah_diampu(self, dosen):
        """Menampilkan mata kuliah yang diampu dosen"""
        MenuDisplay.subheader("Mata Kuliah Diampu")
        
        mk_dosen = [mk for mk in self.state.daftar_mk if mk.dosen == dosen]
        
        if not mk_dosen:
            MenuDisplay.info("Anda belum mengampu mata kuliah")
            MenuDisplay.pause()
            return
        
        MenuUI.show_list(
            mk_dosen,
            title="Daftar Mata Kuliah",
            item_format=lambda mk: mk.info()
        )
        MenuDisplay.pause()

    def _buat_presensi(self, dosen):
        """Menu untuk membuat presensi baru"""
        MenuDisplay.subheader("Buat Presensi")
        
        # Dapatkan mata kuliah yang diampu
        mk_dosen = [mk for mk in self.state.daftar_mk if mk.dosen == dosen]
        
        if not mk_dosen:
            MenuDisplay.error("Anda belum mengampu mata kuliah")
            MenuDisplay.pause()
            return
        
        # Pilih mata kuliah
        MenuUI.show_list(
            mk_dosen,
            title="Pilih Mata Kuliah",
            item_format=lambda mk: mk.info()
        )
        
        try:
            idx = MenuInputValidator.get_integer(
                "Pilih: ",
                min_val=1,
                max_val=len(mk_dosen)
            )
            mk_pilih = mk_dosen[idx - 1]
        except ValueError:
            MenuDisplay.error("Input tidak valid")
            MenuDisplay.pause()
            return
        
        # Input tanggal
        while True:
            tanggal = MenuInputValidator.get_string("Tanggal presensi (dd-mm-yyyy): ")
            try:
                datetime.strptime(tanggal, "%d-%m-%Y")
                break
            except ValueError:
                MenuDisplay.error("Format tanggal salah! Gunakan dd-mm-yyyy")
        
        try:
            pres = self.dosen_service.buat_presensi(dosen, mk_pilih, tanggal)
            MenuDisplay.success("Presensi berhasil dibuat")
        except DosenServiceError as e:
            MenuDisplay.error(str(e))
        
        MenuDisplay.pause()

    def _lihat_daftar_presensi(self, dosen):
        """Menu untuk lihat daftar presensi"""
        MenuDisplay.subheader("Daftar Presensi")
        
        pres_list = self.dosen_service.lihat_presensi_by_dosen(dosen)
        
        if not pres_list:
            MenuDisplay.info("Belum ada presensi yang dibuat")
            MenuDisplay.pause()
            return
        
        # Tampilkan ringkasan presensi
        summary = self.dosen_service.lihat_presensi_summary(dosen)
        for i, s in enumerate(summary, 1):
            print(f"{i}. {s['mata_kuliah']} ({s['tanggal']}) - {s['jumlah_hadir']} hadir")
        
        MenuDisplay.pause()

    def _input_nilai(self, dosen):
        """Menu untuk input nilai mahasiswa"""
        MenuDisplay.subheader("Input Nilai Mahasiswa")
        
        # Dapatkan mata kuliah yang diampu
        mk_dosen = [mk for mk in self.state.daftar_mk if mk.dosen == dosen]
        
        if not mk_dosen:
            MenuDisplay.error("Anda belum mengampu mata kuliah")
            MenuDisplay.pause()
            return
        
        # Pilih mata kuliah
        MenuUI.show_list(
            mk_dosen,
            title="Pilih Mata Kuliah",
            item_format=lambda mk: mk.info()
        )
        
        try:
            idx_mk = MenuInputValidator.get_integer(
                "Pilih: ",
                min_val=1,
                max_val=len(mk_dosen)
            )
            mk_pilih = mk_dosen[idx_mk - 1]
        except ValueError:
            MenuDisplay.error("Input tidak valid")
            MenuDisplay.pause()
            return
        
        # Dapatkan mahasiswa yang mengambil mata kuliah
        mhs_yang_ambil = []
        for krs in self.state.daftar_krs:
            if mk_pilih in krs.daftar_mk:
                mhs_yang_ambil.append(krs.mahasiswa)
        
        if not mhs_yang_ambil:
            MenuDisplay.error("Belum ada mahasiswa yang mengambil mata kuliah ini")
            MenuDisplay.pause()
            return
        
        # Pilih mahasiswa
        MenuUI.show_list(
            mhs_yang_ambil,
            title="Mahasiswa yang Mengambil Mata Kuliah",
            item_format=lambda m: f"{m.nim} - {m.nama}"
        )
        
        try:
            idx_mhs = MenuInputValidator.get_integer(
                "Pilih mahasiswa: ",
                min_val=1,
                max_val=len(mhs_yang_ambil)
            )
            m_pilih = mhs_yang_ambil[idx_mhs - 1]
        except ValueError:
            MenuDisplay.error("Input tidak valid")
            MenuDisplay.pause()
            return
        
        # Input nilai angka
        try:
            nilai_angka = MenuInputValidator.get_integer(
                "Masukkan nilai angka (0-100): ",
                min_val=0,
                max_val=100
            )
        except ValueError:
            MenuDisplay.error("Nilai harus berupa angka")
            MenuDisplay.pause()
            return
        
        # Input nilai ke database
        try:
            nilai_obj = self.dosen_service.input_nilai(
                dosen, m_pilih, mk_pilih, nilai_angka
            )
            
            # Simpan/update ke database (via repository)
            if self.nilai_repo:
                self.nilai_repo.simpan(nilai_obj)
            
            MenuDisplay.success(f"Nilai berhasil disimpan: {nilai_obj.info()}")
        except DosenServiceError as e:
            MenuDisplay.error(str(e))
        
        MenuDisplay.pause()

