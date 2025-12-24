"""
menus/MahasiswaMenu.py
Menu untuk mahasiswa.
Menampilkan menu operasi: KRS, Presensi, Nilai.
"""

from db.krs_repo import simpan_krs
from menus.menu_ui_helper import MenuDisplay, MenuInputValidator, MenuUI
from services.mahasiswa_service import MahasiswaService, MahasiswaServiceError


class MahasiswaMenu:
    """Menu interface untuk mahasiswa"""
    
    def __init__(self, state, service, conn):
        """
        Args:
            state: AppState object
            service: AkademikService atau MahasiswaService
            conn: Database connection
        """
        self.state = state
        self.service = service
        self.conn = conn
        self.mahasiswa_service = MahasiswaService(state)

    def run(self, mhs):
        """
        Main menu loop untuk mahasiswa.
        
        Args:
            mhs: Objek Mahasiswa yang login
        """
        while True:
            self._display_menu(mhs)
            pilih = MenuInputValidator.get_string("Pilihan: ")

            try:
                if pilih == "1":
                    self._lihat_profil(mhs)
                elif pilih == "2":
                    self._lihat_krs(mhs)
                elif pilih == "3":
                    self._ambil_mata_kuliah(mhs)
                elif pilih == "4":
                    self._isi_presensi(mhs)
                elif pilih == "5":
                    self._lihat_nilai(mhs)
                elif pilih == "0":
                    print("Logout mahasiswa...")
                    break
                else:
                    MenuDisplay.error("Pilihan tidak valid")
            except MahasiswaServiceError as e:
                MenuDisplay.error(str(e))
            except Exception as e:
                MenuDisplay.error(f"Terjadi kesalahan: {str(e)}")

    def _display_menu(self, mhs):
        """Tampilkan menu utama mahasiswa"""
        MenuDisplay.header(f"MENU MAHASISWA ({mhs.nama})")
        print("1. Lihat profil")
        print("2. Lihat KRS")
        print("3. Ambil mata kuliah (isi KRS)")
        print("4. Isi presensi")
        print("5. Lihat nilai")
        print("0. Logout")

    def _lihat_profil(self, mhs):
        """Menampilkan profil mahasiswa"""
        MenuDisplay.subheader("Profil Mahasiswa")
        mhs.tampilkan_profil()
        print(f"NIM  : {mhs.nim}")
        print(f"Prodi: {mhs.prodi}")
        MenuDisplay.pause()

    def _lihat_krs(self, mhs):
        """Menampilkan KRS mahasiswa"""
        MenuDisplay.subheader("KRS")
        
        krs_info = self.mahasiswa_service.lihat_krs(mhs)
        if not krs_info:
            MenuDisplay.info("KRS belum tersedia")
            MenuDisplay.pause()
            return
        
        krs = self.mahasiswa_service.cari_krs_by_mahasiswa(mhs)
        krs.tampilkan_krs()
        MenuDisplay.pause()

    def _ambil_mata_kuliah(self, mhs):
        """Menu untuk ambil/menambah mata kuliah ke KRS"""
        krs = self.mahasiswa_service.cari_krs_by_mahasiswa(mhs)
        if not krs:
            MenuDisplay.error("KRS belum dibuat")
            MenuDisplay.pause()
            return

        temp_pilihan = []
        
        while True:
            # Filter mata kuliah yang belum diambil
            mk_tersedia = [
                mk for mk in self.state.daftar_mk 
                if mk not in krs.daftar_mk and mk not in temp_pilihan
            ]
            
            if not mk_tersedia:
                MenuDisplay.info("Tidak ada mata kuliah lagi yang bisa diambil")
                break

            # Tampilkan daftar mata kuliah tersedia
            MenuUI.show_list(
                mk_tersedia,
                title="Daftar Mata Kuliah Tersedia",
                item_format=lambda mk: mk.info()
            )
            print("0. Selesai memilih")
            
            try:
                pilih_mk = MenuInputValidator.get_integer(
                    "Pilih nomor mata kuliah (0 untuk selesai): ",
                    min_val=0,
                    max_val=len(mk_tersedia)
                )
                
                if pilih_mk == 0:
                    break
                
                mk = mk_tersedia[pilih_mk - 1]
                temp_pilihan.append(mk)
                MenuDisplay.success(f"Mata kuliah {mk.kode_mk} ditambahkan ke daftar pilihan")
            except ValueError:
                MenuDisplay.error("Input tidak valid")

        if temp_pilihan:
            # Tampilkan preview
            MenuDisplay.subheader("Mata Kuliah yang akan disimpan ke KRS")
            for i, mk in enumerate(temp_pilihan, 1):
                print(f"{i}. {mk.info()}")
            
            # Konfirmasi
            if MenuInputValidator.confirm_action("Yakin simpan ke KRS? (y/n): "):
                try:
                    for mk in temp_pilihan:
                        krs.tambah_mk(mk)
                    # Simpan ke database
                    simpan_krs(self.conn, krs, temp_pilihan)
                    MenuDisplay.success("Mata kuliah berhasil disimpan ke KRS")
                except Exception as e:
                    MenuDisplay.error(f"Gagal menyimpan KRS: {str(e)}")
                    krs.daftar_mk = krs.daftar_mk[:-len(temp_pilihan)]  # Rollback
            else:
                MenuDisplay.warning("Perubahan KRS dibatalkan")
        else:
            MenuDisplay.info("Tidak ada mata kuliah yang dipilih")
        
        MenuDisplay.pause()

    def _isi_presensi(self, mhs):
        """Menu untuk isi presensi mahasiswa"""
        MenuDisplay.subheader("Isi Presensi")
        
        presensi_list = self.mahasiswa_service.lihat_presensi_tersedia(mhs)
        if not presensi_list:
            MenuDisplay.info("Tidak ada presensi yang bisa diisi")
            MenuDisplay.pause()
            return
        
        # Tampilkan daftar presensi tersedia
        MenuUI.show_list(
            presensi_list,
            title="Presensi Tersedia",
            item_format=lambda p: p.info()
        )
        
        try:
            idx = MenuInputValidator.get_integer(
                "Pilih presensi yang akan diisi: ",
                min_val=1,
                max_val=len(presensi_list)
            )
            
            pres = presensi_list[idx - 1]
            pres.isi_hadir(mhs)
            MenuDisplay.success("Presensi berhasil diisi")
        except (ValueError, IndexError):
            MenuDisplay.error("Input tidak valid")
        
        MenuDisplay.pause()

    def _lihat_nilai(self, mhs):
        """Menu untuk lihat nilai mahasiswa"""
        MenuDisplay.subheader("Daftar Nilai")
        
        nilai_list = self.mahasiswa_service.lihat_nilai(mhs)
        if not nilai_list:
            MenuDisplay.info("Belum ada nilai")
            MenuDisplay.pause()
            return
        
        # Tampilkan nilai dalam format table
        for n_info in nilai_list:
            print(f"• {n_info['mata_kuliah']}: {n_info['nilai_angka']} ({n_info['nilai_huruf']})")
        
        # Tampilkan IPK
        ipk = self.mahasiswa_service.hitung_ipk(mhs)
        MenuDisplay.separator()
        print(f"IPK: {ipk}")
        
        MenuDisplay.pause()
