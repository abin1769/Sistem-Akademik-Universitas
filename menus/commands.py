"""
menus/commands.py
Command Pattern implementation untuk menu actions.
Membuat setiap menu action sebagai command yang bisa di-execute dan undo.
"""

from abc import ABC, abstractmethod


class Command(ABC):
    """Abstract base class untuk semua commands"""
    
    @abstractmethod
    def execute(self):
        """Execute command"""
        pass
    
    @abstractmethod
    def undo(self):
        """Undo command (optional)"""
        pass
    
    @abstractmethod
    def get_name(self):
        """Get command name untuk display"""
        pass


# ============ Mahasiswa Commands ============

class LihatProfilCommand(Command):
    """Command untuk lihat profil mahasiswa"""
    
    def __init__(self, mahasiswa):
        self.mahasiswa = mahasiswa
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay
        MenuDisplay.subheader("Profil Mahasiswa")
        self.mahasiswa.tampilkan_profil()
        print(f"NIM  : {self.mahasiswa.nim}")
        print(f"Prodi: {self.mahasiswa.prodi}")
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Profil"


class LihatKRSCommand(Command):
    """Command untuk lihat KRS mahasiswa"""
    
    def __init__(self, mahasiswa, mahasiswa_service):
        self.mahasiswa = mahasiswa
        self.mahasiswa_service = mahasiswa_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay
        MenuDisplay.subheader("KRS")
        
        krs_info = self.mahasiswa_service.lihat_krs(self.mahasiswa)
        if not krs_info:
            MenuDisplay.info("KRS belum tersedia")
            MenuDisplay.pause()
            return
        
        krs = self.mahasiswa_service.cari_krs_by_mahasiswa(self.mahasiswa)
        krs.tampilkan_krs()
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat KRS"


class IsiPresensiCommand(Command):
    """Command untuk isi presensi mahasiswa"""
    
    def __init__(self, mahasiswa, mahasiswa_service):
        self.mahasiswa = mahasiswa
        self.mahasiswa_service = mahasiswa_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay, MenuInputValidator, MenuUI
        MenuDisplay.subheader("Isi Presensi")
        
        presensi_list = self.mahasiswa_service.lihat_presensi_tersedia(self.mahasiswa)
        if not presensi_list:
            MenuDisplay.info("Tidak ada presensi yang bisa diisi")
            MenuDisplay.pause()
            return
        
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
            pres.isi_hadir(self.mahasiswa)
            MenuDisplay.success("Presensi berhasil diisi")
        except (ValueError, IndexError):
            MenuDisplay.error("Input tidak valid")
        
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Isi Presensi"


class LihatNilaiCommand(Command):
    """Command untuk lihat nilai mahasiswa"""
    
    def __init__(self, mahasiswa, mahasiswa_service):
        self.mahasiswa = mahasiswa
        self.mahasiswa_service = mahasiswa_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay
        MenuDisplay.subheader("Daftar Nilai")
        
        nilai_list = self.mahasiswa_service.lihat_nilai(self.mahasiswa)
        if not nilai_list:
            MenuDisplay.info("Belum ada nilai")
            MenuDisplay.pause()
            return
        
        for n_info in nilai_list:
            print(f"• {n_info['mata_kuliah']}: {n_info['nilai_angka']} ({n_info['nilai_huruf']})")
        
        ipk = self.mahasiswa_service.hitung_ipk(self.mahasiswa)
        MenuDisplay.separator()
        print(f"IPK: {ipk}")
        
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Nilai"


# ============ Dosen Commands ============

class LihatMatkulDiamuCommand(Command):
    """Command untuk lihat mata kuliah yang diampu dosen"""
    
    def __init__(self, dosen, state):
        self.dosen = dosen
        self.state = state
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay, MenuUI
        MenuDisplay.subheader("Mata Kuliah Diampu")
        
        mk_dosen = [mk for mk in self.state.daftar_mk if mk.dosen == self.dosen]
        
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
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Mata Kuliah Diampu"


class LihatDaftarPresensiCommand(Command):
    """Command untuk lihat daftar presensi dosen"""
    
    def __init__(self, dosen, dosen_service):
        self.dosen = dosen
        self.dosen_service = dosen_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay
        MenuDisplay.subheader("Daftar Presensi")
        
        pres_list = self.dosen_service.lihat_presensi_by_dosen(self.dosen)
        
        if not pres_list:
            MenuDisplay.info("Belum ada presensi yang dibuat")
            MenuDisplay.pause()
            return
        
        summary = self.dosen_service.lihat_presensi_summary(self.dosen)
        for i, s in enumerate(summary, 1):
            print(f"{i}. {s['mata_kuliah']} ({s['tanggal']}) - {s['jumlah_hadir']} hadir")
        
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Daftar Presensi"


# ============ Admin Commands ============

class LihatSemuaMataKuliahCommand(Command):
    """Command untuk lihat semua mata kuliah"""
    
    def __init__(self, admin_service):
        self.admin_service = admin_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay, MenuUI
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
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Semua Mata Kuliah"


class LihatSemuaMahasiswaCommand(Command):
    """Command untuk lihat semua mahasiswa"""
    
    def __init__(self, state):
        self.state = state
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay, MenuUI
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
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Semua Mahasiswa"


class LihatStatistikCommand(Command):
    """Command untuk lihat statistik sistem"""
    
    def __init__(self, admin_service):
        self.admin_service = admin_service
    
    def execute(self):
        from menus.menu_ui_helper import MenuDisplay
        MenuDisplay.subheader("Statistik Sistem Akademik")
        
        stats = self.admin_service.lihat_statistik_sistem()
        
        print(f"Total Mahasiswa     : {stats['total_mahasiswa']}")
        print(f"Total Dosen         : {stats['total_dosen']}")
        print(f"Total Mata Kuliah   : {stats['total_mata_kuliah']}")
        print(f"Total KRS           : {stats['total_krs']}")
        print(f"Total Presensi      : {stats['total_presensi']}")
        print(f"Total Nilai         : {stats['total_nilai']}")
        
        MenuDisplay.pause()
    
    def undo(self):
        pass
    
    def get_name(self):
        return "Lihat Statistik"


class CommandInvoker:
    """Invoker untuk execute commands"""
    
    def __init__(self):
        self.commands = {}
        self.last_command = None
    
    def register_command(self, key, command):
        """Register command dengan key"""
        self.commands[key] = command
    
    def execute(self, key):
        """Execute command berdasarkan key"""
        if key not in self.commands:
            raise ValueError(f"Command '{key}' tidak ditemukan")
        
        command = self.commands[key]
        command.execute()
        self.last_command = command
    
    def undo_last(self):
        """Undo command terakhir"""
        if self.last_command:
            self.last_command.undo()
    
    def get_available_commands(self):
        """Get daftar available commands"""
        return {key: cmd.get_name() for key, cmd in self.commands.items()}
