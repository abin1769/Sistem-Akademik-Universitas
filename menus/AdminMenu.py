"""
menus/AdminMenu.py
Menu untuk admin.
Menampilkan menu operasi: Manajemen Mata Kuliah dan Statistik.
"""

from db import simpan_mata_kuliah, update_mata_kuliah
from menus.menu_ui_helper import MenuDisplay, MenuInputValidator, MenuUI
from services.admin_service import AdminService, AdminServiceError


class AdminMenu:
    """Menu interface untuk admin"""
    
    def __init__(self, state, service, conn):
        """
        Args:
            state: AppState object
            service: AkademikService atau AdminService
            conn: Database connection
        """
        self.state = state
        self.service = service
        self.conn = conn
        self.admin_service = AdminService(state)

    def run(self, admin):
        """
        Main menu loop untuk admin.
        
        Args:
            admin: Objek Admin yang login
        """
        while True:
            self._display_menu(admin)
            pilih = MenuInputValidator.get_string("Pilihan: ")

            try:
                if pilih == "1":
                    self._lihat_semua_mata_kuliah()
                elif pilih == "2":
                    self._tambah_mata_kuliah()
                elif pilih == "3":
                    self._edit_mata_kuliah()
                elif pilih == "4":
                    self._lihat_semua_mahasiswa()
                elif pilih == "5":
                    self._lihat_statistik()
                elif pilih == "0":
                    print("Logout admin...")
                    break
                else:
                    MenuDisplay.error("Pilihan tidak valid")
            except AdminServiceError as e:
                MenuDisplay.error(str(e))
            except Exception as e:
                MenuDisplay.error(f"Terjadi kesalahan: {str(e)}")

    def _display_menu(self, admin):
        """Tampilkan menu utama admin"""
        MenuDisplay.header(f"MENU ADMIN ({admin.nama})")
        print("1. Lihat semua mata kuliah")
        print("2. Tambah mata kuliah")
        print("3. Edit mata kuliah")
        print("4. Lihat semua mahasiswa")
        print("5. Lihat statistik sistem")
        print("0. Logout")

    def _lihat_semua_mata_kuliah(self):
        """Menampilkan semua mata kuliah"""
        MenuDisplay.subheader("Daftar Semua Mata Kuliah")
        
        mk_list = self.admin_service.lihat_semua_mata_kuliah()
        
        if not mk_list:
            MenuDisplay.info("Belum ada mata kuliah")
            MenuDisplay.pause()
            return
        
        MenuUI.show_list(
            mk_list,
            title="Mata Kuliah",
            item_format=lambda mk: mk.info()
        )
        MenuDisplay.pause()

    def _tambah_mata_kuliah(self):
        """Menu untuk tambah mata kuliah baru"""
        MenuDisplay.subheader("Tambah Mata Kuliah Baru")
        
        # Input data
        kode_mk = MenuInputValidator.get_string("Kode MK: ")
        nama_mk = MenuInputValidator.get_string("Nama MK: ")
        sks = MenuInputValidator.get_integer("SKS (1-4): ", min_val=1, max_val=4)
        deskripsi = MenuInputValidator.get_string("Deskripsi (optional): ", allow_empty=True)
        
        # Validasi
        errors = self.admin_service.validasi_tambah_mata_kuliah(kode_mk, nama_mk, sks)
        if errors:
            for error in errors:
                MenuDisplay.error(error)
            MenuDisplay.pause()
            return
        
        # Pilih dosen
        if not self.state.daftar_dosen:
            MenuDisplay.error("Belum ada dosen, tambah dosen terlebih dahulu")
            MenuDisplay.pause()
            return
        
        MenuUI.show_list(
            self.state.daftar_dosen,
            title="Pilih Dosen Pengampu",
            item_format=lambda d: d.nama
        )
        
        try:
            idx = MenuInputValidator.get_integer(
                "Pilih: ",
                min_val=1,
                max_val=len(self.state.daftar_dosen)
            )
            dosen = self.state.daftar_dosen[idx - 1]
        except ValueError:
            MenuDisplay.error("Input tidak valid")
            MenuDisplay.pause()
            return
        
        # Tambah mata kuliah
        try:
            mk_baru = self.admin_service.tambah_mata_kuliah(
                kode_mk, nama_mk, sks, deskripsi
            )
            mk_baru.dosen = dosen
            
            # Simpan ke database
            simpan_mata_kuliah(self.conn, mk_baru)
            
            MenuDisplay.success("Mata kuliah berhasil ditambahkan")
        except AdminServiceError as e:
            MenuDisplay.error(str(e))
        
        MenuDisplay.pause()

    def _edit_mata_kuliah(self):
        """Menu untuk edit mata kuliah"""
        MenuDisplay.subheader("Edit Mata Kuliah")
        
        mk_list = self.admin_service.lihat_semua_mata_kuliah()
        
        if not mk_list:
            MenuDisplay.error("Belum ada mata kuliah")
            MenuDisplay.pause()
            return
        
        # Pilih mata kuliah
        MenuUI.show_list(
            mk_list,
            title="Pilih Mata Kuliah yang Akan Diedit",
            item_format=lambda mk: mk.info()
        )
        
        try:
            idx = MenuInputValidator.get_integer(
                "Pilih: ",
                min_val=1,
                max_val=len(mk_list)
            )
            mk = mk_list[idx - 1]
        except ValueError:
            MenuDisplay.error("Input tidak valid")
            MenuDisplay.pause()
            return
        
        kode_lama = mk.kode_mk
        
        # Input perubahan
        print(f"\nKode MK saat ini: {mk.kode_mk}")
        kode_baru = MenuInputValidator.get_string("Kode MK baru (Enter untuk tidak berubah): ", allow_empty=True)
        
        print(f"Nama MK saat ini: {mk.nama}")
        nama_baru = MenuInputValidator.get_string("Nama MK baru (Enter untuk tidak berubah): ", allow_empty=True)
        
        print(f"SKS saat ini: {mk.sks}")
        sks_str = MenuInputValidator.get_string("SKS baru (Enter untuk tidak berubah): ", allow_empty=True)
        sks_baru = None
        if sks_str:
            try:
                sks_baru = int(sks_str)
            except ValueError:
                MenuDisplay.error("SKS harus berupa angka")
                MenuDisplay.pause()
                return
        
        # Update
        try:
            mk_updated = self.admin_service.edit_mata_kuliah(
                kode_lama,
                nama=nama_baru if nama_baru else None,
                sks=sks_baru,
                deskripsi=None
            )
            
            # Simpan ke database
            update_mata_kuliah(self.conn, mk_updated, kode_lama)
            
            MenuDisplay.success("Mata kuliah berhasil diedit")
        except AdminServiceError as e:
            MenuDisplay.error(str(e))
        
        MenuDisplay.pause()

    def _lihat_semua_mahasiswa(self):
        """Menampilkan semua mahasiswa"""
        MenuDisplay.subheader("Daftar Semua Mahasiswa")
        
        mhs_list = self.state.daftar_mahasiswa
        
        if not mhs_list:
            MenuDisplay.info("Belum ada mahasiswa")
            MenuDisplay.pause()
            return
        
        MenuUI.show_list(
            mhs_list,
            title="Mahasiswa",
            item_format=lambda m: f"{m.nim} - {m.nama} ({m.prodi})"
        )
        MenuDisplay.pause()

    def _lihat_statistik(self):
        """Menampilkan statistik sistem"""
        MenuDisplay.subheader("Statistik Sistem Akademik")
        
        stats = self.admin_service.lihat_statistik_sistem()
        
        print(f"Total Mahasiswa     : {stats['total_mahasiswa']}")
        print(f"Total Dosen         : {stats['total_dosen']}")
        print(f"Total Mata Kuliah   : {stats['total_mata_kuliah']}")
        print(f"Total KRS           : {stats['total_krs']}")
        print(f"Total Presensi      : {stats['total_presensi']}")
        print(f"Total Nilai         : {stats['total_nilai']}")
        
        MenuDisplay.pause()

