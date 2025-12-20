# ============================
# SISTEM AKADEMIK (PENGELOLA)
# ============================

from user import Admin, Mahasiswa, Dosen, Login
from akademik import MataKuliah, KRS, Presensi, Nilai
from db import get_connection, simpan_krs, simpan_nilai, simpan_mata_kuliah, update_mata_kuliah


class SistemAkademik:
    def __init__(self):
        self.daftar_admin = []
        self.daftar_mahasiswa = []
        self.daftar_dosen = []
        self.daftar_mk = []
        self.daftar_krs = []
        self.daftar_presensi = []
        self.daftar_nilai = []
        self.next_id_presensi = 1

        # mapping id dari database -> objek Python
        self.dosen_by_id = {}
        self.mahasiswa_by_id = {}
        self.mk_by_id = {}
        self.krs_by_id = {}

        # koneksi ke database
        self.conn = get_connection()

        # kalau koneksi gagal, jangan crash
        if not self.conn:
            print("PERINGATAN: Gagal koneksi ke database. Data hanya ada di memori.")
            return

        # load semua data dari database
        self.load_admin_from_db()
        self.load_dosen_from_db()
        self.load_mahasiswa_from_db()
        self.load_mata_kuliah_from_db()
        self.load_krs_from_db()
        self.load_nilai_from_db()
    
    def load_admin_from_db(self):
        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT a.id_admin, u.id_user, u.nama, u.email, u.password, a.username
                FROM admin a
                JOIN users u ON a.id_user = u.id_user
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            self.daftar_admin = []

            for id_admin, id_user, nama, email, password, username in rows:
                admin = Admin(id_user, nama, email, password, username)
                self.daftar_admin.append(admin)
        except Exception as e:
            print("Gagal load admin dari database:", e)
    
    def load_dosen_from_db(self):
        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT d.id_dosen, u.id_user, u.nama, u.email, u.password,
                       d.nidn, d.departemen
                FROM dosen d
                JOIN users u ON d.id_user = u.id_user
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            self.daftar_dosen = []
            self.dosen_by_id = {}

            for id_dosen, id_user, nama, email, password, nidn, departemen in rows:
                dosen = Dosen(id_dosen, nama, email, password, nidn, departemen)
                self.daftar_dosen.append(dosen)
                self.dosen_by_id[id_dosen] = dosen
        except Exception as e:
            print("Gagal load dosen dari database:", e)

    def load_mahasiswa_from_db(self):
        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT m.id_mahasiswa, u.id_user, u.nama, u.email, u.password,
                       m.nim, m.prodi, m.angkatan
                FROM mahasiswa m
                JOIN users u ON m.id_user = u.id_user
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            self.daftar_mahasiswa = []
            self.mahasiswa_by_id = {}

            for id_mhs, id_user, nama, email, password, nim, prodi, angkatan in rows:
                mhs = Mahasiswa(id_mhs, nama, email, password, nim, prodi)
                self.daftar_mahasiswa.append(mhs)
                self.mahasiswa_by_id[id_mhs] = mhs
        except Exception as e:
            print("Gagal load mahasiswa dari database:", e)

    def load_mata_kuliah_from_db(self):
        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT id_mk, kode_mk, nama_mk, sks, id_dosen
                FROM mata_kuliah
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            self.daftar_mk = []
            self.mk_by_id = {}

            for id_mk, kode_mk, nama_mk, sks, id_dosen in rows:
                dosen_obj = None
                if id_dosen is not None and id_dosen in self.dosen_by_id:
                    dosen_obj = self.dosen_by_id[id_dosen]

                mk = MataKuliah(kode_mk, nama_mk, sks, dosen_obj)
                self.daftar_mk.append(mk)
                self.mk_by_id[id_mk] = mk
        except Exception as e:
            print("Gagal load mata kuliah dari database:", e)

    def load_krs_from_db(self):
        try:
            cursor = self.conn.cursor()

            # 1. Ambil KRS utama
            sql_krs = """
                SELECT id_krs, id_mahasiswa, semester, tahun_ajaran
                FROM krs
            """
            cursor.execute(sql_krs)
            rows_krs = cursor.fetchall()

            self.daftar_krs = []
            self.krs_by_id = {}

            for id_krs, id_mahasiswa, semester, tahun_ajaran in rows_krs:
                mhs_obj = self.mahasiswa_by_id.get(id_mahasiswa)
                if not mhs_obj:
                    # kalau mahasiswa tidak ditemukan di cache, lewati
                    continue
                krs_obj = KRS(mhs_obj, semester, tahun_ajaran)
                self.daftar_krs.append(krs_obj)
                self.krs_by_id[id_krs] = krs_obj

            # 2. Ambil detail mata kuliah KRS
            sql_detail = """
                SELECT id_krs, id_mk
                FROM krs_detail
            """
            cursor.execute(sql_detail)
            rows_detail = cursor.fetchall()
            cursor.close()

            for id_krs, id_mk in rows_detail:
                krs_obj = self.krs_by_id.get(id_krs)
                mk_obj = self.mk_by_id.get(id_mk)
                if krs_obj and mk_obj:
                    krs_obj.tambah_mk(mk_obj)
        except Exception as e:
            print("Gagal load KRS dari database:", e)

    def load_nilai_from_db(self):
        try:
            cursor = self.conn.cursor()
            sql = """
                SELECT id_mahasiswa, id_mk, nilai_angka, nilai_huruf
                FROM nilai
            """
            cursor.execute(sql)
            rows = cursor.fetchall()
            cursor.close()

            self.daftar_nilai = []

            for id_mhs, id_mk, nilai_angka, nilai_huruf in rows:
                mhs_obj = self.mahasiswa_by_id.get(id_mhs)
                mk_obj = self.mk_by_id.get(id_mk)

                if not mhs_obj or not mk_obj:
                    continue

                nilai_obj = Nilai(mhs_obj, mk_obj, float(nilai_angka))
                # override nilai_huruf dengan yang ada di DB (kalau beda)
                nilai_obj.nilai_huruf = nilai_huruf
                self.daftar_nilai.append(nilai_obj)
        except Exception as e:
            print("Gagal load nilai dari database:", e)



    # ------- UTIL USER --------
    def cari_mahasiswa_by_nim(self, nim):
        for m in self.daftar_mahasiswa:
            if m.nim == nim:
                return m
        return None

    def cari_dosen_by_nidn(self, nidn):
        for d in self.daftar_dosen:
            if d.nidn == nidn:
                return d
        return None

    def cari_krs_by_mahasiswa(self, mahasiswa):
        for k in self.daftar_krs:
            if k.mahasiswa == mahasiswa:
                return k
        return None

    # ------- UTIL PRESENSI --------
    def presensi_by_dosen(self, dosen):
        return [p for p in self.daftar_presensi if p.dosen == dosen]

    def presensi_tersedia_untuk_mahasiswa(self, mahasiswa):
        krs = self.cari_krs_by_mahasiswa(mahasiswa)
        if not krs:
            return []
        mk_di_krs = set(krs.daftar_mk)
        hasil = []
        for p in self.daftar_presensi:
            if p.mata_kuliah in mk_di_krs and mahasiswa not in p.daftar_hadir:
                hasil.append(p)
        return hasil

    # ------- UTIL NILAI --------
    def nilai_mahasiswa(self, mahasiswa):
        return [n for n in self.daftar_nilai if n.mahasiswa == mahasiswa]

    def nilai_by_mk_for_dosen(self, dosen, mata_kuliah):
        return [n for n in self.daftar_nilai
                if n.mata_kuliah == mata_kuliah and mata_kuliah.dosen == dosen]

    # ------- MENU LOGIN UTAMA --------
    def login(self):
        print("\n=== SISTEM AKADEMIK ===")
        identifier = input("Masukkan NIM / NIDN / Username Admin: ")
        password = input("Masukkan password: ")

        login_obj = Login(identifier, password)

        try:
            login_obj.validate_input()
        except ValueError as e:
            print("Error:", e)
            return

        role = login_obj.determine_role()

        if role == 'mahasiswa':
            mhs = self.cari_mahasiswa_by_nim(identifier)
            if mhs and mhs.password == password:
                self.menu_mahasiswa(mhs)
            else:
                print("Mahasiswa tidak ditemukan / password salah.")
        elif role == 'dosen':
            dosen = self.cari_dosen_by_nidn(identifier)
            if dosen and dosen.password == password:
                self.menu_dosen(dosen)
            else:
                print("Dosen tidak ditemukan / password salah.")
        else:
            # admin login pakai username "admin"
            admin = None
            for a in self.daftar_admin:
                if a.username == identifier and a.password == password:
                    admin = a
                    break
            if admin:
                self.menu_admin(admin)
            else:
                print("Admin tidak ditemukan / password salah.")

    # ------- MENU ADMIN --------
    def menu_admin(self, admin):
        while True:
            print(f"\n=== MENU ADMIN ({admin.nama}) ===")
            print("1. Lihat semua mata kuliah")
            print("2. Tambah mata kuliah")
            print("3. Edit mata kuliah")
            print("4. Lihat semua mahasiswa")
            print("0. Logout")
            pilih = input("Pilih menu: ")

            if pilih == "1":
                print("\nDaftar Mata Kuliah:")
                for mk in self.daftar_mk:
                    print("-", mk.info())

            elif pilih == "2":
                kode = input("Kode MK: ")
                nama = input("Nama MK: ")
                sks = int(input("SKS: "))
                print("Pilih dosen pengampu:")
                for i, d in enumerate(self.daftar_dosen, start=1):
                    print(f"{i}. {d.nama}")
                idx = int(input("Pilih: ")) - 1
                dosen = self.daftar_dosen[idx]
                mk_baru = MataKuliah(kode, nama, sks, dosen)
                self.daftar_mk.append(mk_baru)
                # ← SIMPAN KE DATABASE
                simpan_mata_kuliah(self.conn, mk_baru)
                print("Mata kuliah berhasil ditambahkan.")

            elif pilih == "3":
                # EDIT KURIKULUM / MATA KULIAH
                if not self.daftar_mk:
                    print("Belum ada mata kuliah.")
                    continue
                print("\nPilih mata kuliah yang akan diedit:")
                for i, mk in enumerate(self.daftar_mk, start=1):
                    print(f"{i}. {mk.info()}")
                idx = int(input("Pilih: ")) - 1
                mk = self.daftar_mk[idx]
                
                # simpan kode lama supaya tahu baris mana yang diupdate di DB
                kode_lama = mk.kode_mk

                print("Kosongkan jika tidak ingin mengubah.")
                kode_baru = input(f"Kode MK baru ({mk.kode_mk}): ")
                nama_baru = input(f"Nama MK baru ({mk.nama_mk}): ")
                sks_baru = input(f"SKS baru ({mk.sks}): ")

                if kode_baru:
                    mk.kode_mk = kode_baru
                if nama_baru:
                    mk.nama_mk = nama_baru
                if sks_baru:
                    mk.sks = int(sks_baru)

                ganti_dosen = input("Ganti dosen pengampu? (y/n): ").lower()
                if ganti_dosen == 'y':
                    print("Pilih dosen:")
                    for i, d in enumerate(self.daftar_dosen, start=1):
                        print(f"{i}. {d.nama}")
                    idx_d = int(input("Pilih: ")) - 1
                    mk.dosen = self.daftar_dosen[idx_d]
                    
                    # ← UPDATE KE DATABASE
                update_mata_kuliah(self.conn, mk, kode_lama)


                print("Mata kuliah berhasil diedit.")

            elif pilih == "4":
                print("\nDaftar Mahasiswa:")
                for m in self.daftar_mahasiswa:
                    print(f"- {m.nim} - {m.nama} ({m.prodi})")

            elif pilih == "0":
                print("Logout admin...")
                break
            else:
                print("Pilihan tidak valid.")

    # ------- MENU MAHASISWA --------
    def menu_mahasiswa(self, mhs):
        while True:
            print(f"\n=== MENU MAHASISWA ({mhs.nama}) ===")
            print("1. Lihat profil")
            print("2. Lihat KRS")
            print("3. Ambil mata kuliah (isi KRS)")
            print("4. Isi presensi")
            print("5. Lihat nilai")
            print("0. Logout")
            pilih = input("Pilih menu: ")

            krs = self.cari_krs_by_mahasiswa(mhs)

            if pilih == "1":
                mhs.tampilkan_profil()
                print("NIM  :", mhs.nim)
                print("Prodi:", mhs.prodi)

            elif pilih == "2":
                if krs:
                    krs.tampilkan_krs()
                else:
                    print("KRS belum tersedia.")

            elif pilih == "3":
                if not krs:
                    print("KRS belum dibuat.")
                    continue

                temp_pilihan = []

                while True:
                    mk_tersedia = [mk for mk in self.daftar_mk if mk not in krs.daftar_mk and mk not in temp_pilihan]
                    if not mk_tersedia:
                        print("\nTidak ada mata kuliah lagi yang bisa diambil.")
                        break

                    print("\nDaftar mata kuliah yang bisa diambil:")
                    for i, mk in enumerate(mk_tersedia, start=1):
                        print(f"{i}. {mk.info()}")
                    print("0. Selesai memilih")

                    pilih_mk = input("Pilih nomor mata kuliah (0 untuk selesai): ")

                    if not pilih_mk.isdigit():
                        print("Input tidak valid.")
                        continue

                    pilih_mk = int(pilih_mk)

                    if pilih_mk == 0:
                        break

                    if 1 <= pilih_mk <= len(mk_tersedia):
                        mk = mk_tersedia[pilih_mk - 1]
                        temp_pilihan.append(mk)
                        print(f"Mata kuliah {mk.kode_mk} ditambahkan ke daftar pilihan sementara.")
                    else:
                        print("Pilihan di luar jangkauan.")

                if temp_pilihan:
                    print("\nMata kuliah yang akan dimasukkan ke KRS:")
                    for mk in temp_pilihan:
                        print("-", mk.info())

                    konfirmasi = input("Yakin simpan ke KRS? (y/n): ").lower()
                    if konfirmasi == 'y':
                        for mk in temp_pilihan:
                            krs.tambah_mk(mk)
                        # SIMPAN KE DATABASE
                        simpan_krs(self.conn, krs, temp_pilihan)
                        print("Mata kuliah berhasil disimpan ke KRS.")
                    else:
                        print("Perubahan KRS dibatalkan.")
                else:
                    print("Tidak ada mata kuliah yang dipilih.")

            elif pilih == "4":
                presensi_list = self.presensi_tersedia_untuk_mahasiswa(mhs)
                if not presensi_list:
                    print("Tidak ada presensi yang bisa diisi.")
                    continue
                print("\nPresensi yang tersedia:")
                for i, p in enumerate(presensi_list, start=1):
                    print(f"{i}. {p.info()}")
                idx = int(input("Pilih presensi yang akan diisi: ")) - 1
                pres = presensi_list[idx]
                pres.isi_hadir(mhs)
                print("Presensi berhasil diisi.")

            elif pilih == "5":
                nilai_list = self.nilai_mahasiswa(mhs)
                if not nilai_list:
                    print("Belum ada nilai.")
                else:
                    print("\nDaftar nilai:")
                    for n in nilai_list:
                        print("-", n.info())

            elif pilih == "0":
                print("Logout mahasiswa...")
                break
            else:
                print("Pilihan tidak valid.")

    # ------- MENU DOSEN --------
    def menu_dosen(self, dosen):
        while True:
            print(f"\n=== MENU DOSEN ({dosen.nama}) ===")
            print("1. Lihat profil")
            print("2. Lihat mata kuliah diampu")
            print("3. Buat presensi")
            print("4. Lihat daftar presensi")
            print("5. Input nilai mahasiswa")
            print("0. Logout")
            pilih = input("Pilih menu: ")

            if pilih == "1":
                dosen.tampilkan_profil()
                print("NIDN      :", dosen.nidn)
                print("Departemen:", dosen.departemen)

            elif pilih == "2":
                print("\nMata kuliah diampu:")
                for mk in self.daftar_mk:
                    if mk.dosen == dosen:
                        print("-", mk.info())

            elif pilih == "3":
                mk_dosen = [mk for mk in self.daftar_mk if mk.dosen == dosen]
                if not mk_dosen:
                    print("Anda belum mengampu mata kuliah.")
                    continue
                print("\nPilih mata kuliah untuk presensi:")
                for i, mk in enumerate(mk_dosen, start=1):
                    print(f"{i}. {mk.info()}")
                idx = int(input("Pilih: ")) - 1
                mk_pilih = mk_dosen[idx]
                tanggal = input("Tanggal presensi (dd-mm-yyyy): ")
                pres = Presensi(self.next_id_presensi, mk_pilih, dosen, tanggal)
                self.next_id_presensi += 1
                self.daftar_presensi.append(pres)
                print("Presensi berhasil dibuka.")

            elif pilih == "4":
                pres_list = self.presensi_by_dosen(dosen)
                if not pres_list:
                    print("Belum ada presensi yang dibuat.")
                    continue
                print("\nDaftar presensi:")
                for p in pres_list:
                    print(p.info(), "- Hadir:", len(p.daftar_hadir), "mahasiswa")

            elif pilih == "5":
                mk_dosen = [mk for mk in self.daftar_mk if mk.dosen == dosen]
                if not mk_dosen:
                    print("Anda belum mengampu mata kuliah.")
                    continue

                print("\nPilih mata kuliah:")
                for i, mk in enumerate(mk_dosen, start=1):
                    print(f"{i}. {mk.info()}")
                idx_mk = int(input("Pilih: ")) - 1
                mk_pilih = mk_dosen[idx_mk]

                mhs_yang_ambil = []
                for krs in self.daftar_krs:
                    if mk_pilih in krs.daftar_mk:
                        mhs_yang_ambil.append(krs.mahasiswa)

                if not mhs_yang_ambil:
                    print("Belum ada mahasiswa yang mengambil mata kuliah ini.")
                    continue

                print("\nMahasiswa yang mengambil mata kuliah ini:")
                for i, m in enumerate(mhs_yang_ambil, start=1):
                    print(f"{i}. {m.nim} - {m.nama}")

                idx_mhs = int(input("Pilih mahasiswa: ")) - 1
                m_pilih = mhs_yang_ambil[idx_mhs]

                nilai_angka = float(input("Masukkan nilai angka (0-100): "))
                nilai_obj = Nilai(m_pilih, mk_pilih, nilai_angka)
                self.daftar_nilai.append(nilai_obj)
                simpan_nilai(self.conn, nilai_obj)
                print("Nilai berhasil disimpan:", nilai_obj.info())

            elif pilih == "0":
                print("Logout dosen...")
                break
            else:
                print("Pilihan tidak valid.")
