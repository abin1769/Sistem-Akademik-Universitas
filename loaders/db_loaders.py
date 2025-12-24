# loaders/db_loader.py
from application.dto.admin import Admin
from application.dto.mahasiswa import Mahasiswa
from application.dto.dosen import Dosen
from domain.entities.matakuliah import MataKuliah
from domain.entities.krs import KRS
from domain.entities.nilai import Nilai

class DBLoader:
    def __init__(self, conn):
        self.conn = conn

    def load_all(self, state):
        # state adalah object yang nyimpen daftar_* dan mapping *_by_id
        self.load_admin(state)
        self.load_dosen(state)
        self.load_mahasiswa(state)
        self.load_mata_kuliah(state)
        self.load_krs(state)
        self.load_nilai(state)

    def load_admin(self, state):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT a.id_admin, u.id_user, u.nama, u.email, u.password, a.username
            FROM admin a
            JOIN users u ON a.id_user = u.id_user
        """)
        rows = cursor.fetchall()
        cursor.close()

        state.daftar_admin = []
        for id_admin, id_user, nama, email, password, username in rows:
            state.daftar_admin.append(Admin(id_user, nama, email, password, username))

    def load_dosen(self, state):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT d.id_dosen, u.id_user, u.nama, u.email, u.password,
                   d.nidn, d.departemen
            FROM dosen d
            JOIN users u ON d.id_user = u.id_user
        """)
        rows = cursor.fetchall()
        cursor.close()

        state.daftar_dosen = []
        state.dosen_by_id = {}
        for id_dosen, id_user, nama, email, password, nidn, departemen in rows:
            dosen = Dosen(id_dosen, nama, email, password, nidn, departemen)
            state.daftar_dosen.append(dosen)
            state.dosen_by_id[id_dosen] = dosen

    def load_mahasiswa(self, state):
        cursor = self.conn.cursor()
        cursor.execute("""
            SELECT m.id_mahasiswa, u.id_user, u.nama, u.email, u.password,
                   m.nim, m.prodi, m.angkatan
            FROM mahasiswa m
            JOIN users u ON m.id_user = u.id_user
        """)
        rows = cursor.fetchall()
        cursor.close()

        state.daftar_mahasiswa = []
        state.mahasiswa_by_id = {}
        for id_mhs, id_user, nama, email, password, nim, prodi, angkatan in rows:
            mhs = Mahasiswa(id_mhs, nama, email, password, nim, prodi)
            state.daftar_mahasiswa.append(mhs)
            state.mahasiswa_by_id[id_mhs] = mhs

    def load_mata_kuliah(self, state):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_mk, kode_mk, nama_mk, sks, id_dosen FROM mata_kuliah")
        rows = cursor.fetchall()
        cursor.close()

        state.daftar_mk = []
        state.mk_by_id = {}
        for id_mk, kode_mk, nama_mk, sks, id_dosen in rows:
            dosen_obj = state.dosen_by_id.get(id_dosen)
            mk = MataKuliah(kode_mk, nama_mk, sks, dosen_obj)
            state.daftar_mk.append(mk)
            state.mk_by_id[id_mk] = mk

    def load_krs(self, state):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_krs, id_mahasiswa, semester, tahun_ajaran FROM krs")
        rows_krs = cursor.fetchall()

        state.daftar_krs = []
        state.krs_by_id = {}
        for id_krs, id_mahasiswa, semester, tahun_ajaran in rows_krs:
            mhs_obj = state.mahasiswa_by_id.get(id_mahasiswa)
            if not mhs_obj:
                continue
            krs_obj = KRS(mhs_obj, semester, tahun_ajaran)
            state.daftar_krs.append(krs_obj)
            state.krs_by_id[id_krs] = krs_obj

        cursor.execute("SELECT id_krs, id_mk FROM krs_detail")
        rows_detail = cursor.fetchall()
        cursor.close()

        for id_krs, id_mk in rows_detail:
            krs_obj = state.krs_by_id.get(id_krs)
            mk_obj = state.mk_by_id.get(id_mk)
            if krs_obj and mk_obj:
                krs_obj.tambah_mk(mk_obj)

    def load_nilai(self, state):
        cursor = self.conn.cursor()
        cursor.execute("SELECT id_mahasiswa, id_mk, nilai_angka, nilai_huruf FROM nilai")
        rows = cursor.fetchall()
        cursor.close()

        state.daftar_nilai = []
        for id_mhs, id_mk, nilai_angka, nilai_huruf in rows:
            mhs_obj = state.mahasiswa_by_id.get(id_mhs)
            mk_obj = state.mk_by_id.get(id_mk)
            if not mhs_obj or not mk_obj:
                continue
            nilai_obj = Nilai(mhs_obj, mk_obj, float(nilai_angka))
            nilai_obj.nilai_huruf = nilai_huruf
            state.daftar_nilai.append(nilai_obj)
