"""
infrastructure/repositories/mata_kuliah_repository.py
Concrete implementation dari BaseRepository untuk Mata Kuliah.
"""

from infrastructure.repositories.base_repository import BaseRepository, RepositoryError


class MataKuliahRepository(BaseRepository):
    """Repository untuk entity MataKuliah"""

    def simpan(self, mk_obj):
        """Simpan mata kuliah ke database."""
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, id_dosen)
                VALUES (%s, %s, %s, %s)
            """
            id_dosen = getattr(getattr(mk_obj, "dosen", None), "id", None)
            cursor.execute(query, (mk_obj.kode_mk, mk_obj.nama_mk, mk_obj.sks, id_dosen))
            self.commit()
            mk_obj.id_mk = cursor.lastrowid
            return mk_obj.id_mk
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal simpan MataKuliah: {str(e)}")

    def cari_by_id(self, id_mk):
        try:
            cursor = self.execute_query("SELECT * FROM mata_kuliah WHERE id_mk = %s", (id_mk,))
            return cursor.fetchone()
        except RepositoryError:
            return None

    def update(self, mk_obj, kode_lama=None):
        """Update mata kuliah (pakai id_mk jika ada; fallback ke kode_lama/kode_mk)."""
        try:
            cursor = self.conn.cursor()
            id_dosen = getattr(getattr(mk_obj, "dosen", None), "id", None)

            if getattr(mk_obj, "id_mk", None) is not None:
                query = """
                    UPDATE mata_kuliah
                    SET kode_mk = %s, nama_mk = %s, sks = %s, id_dosen = %s
                    WHERE id_mk = %s
                """
                params = (mk_obj.kode_mk, mk_obj.nama_mk, mk_obj.sks, id_dosen, mk_obj.id_mk)
            else:
                where_kode = kode_lama or mk_obj.kode_mk
                query = """
                    UPDATE mata_kuliah
                    SET kode_mk = %s, nama_mk = %s, sks = %s, id_dosen = %s
                    WHERE kode_mk = %s
                """
                params = (mk_obj.kode_mk, mk_obj.nama_mk, mk_obj.sks, id_dosen, where_kode)

            cursor.execute(query, params)
            self.commit()
            return cursor.rowcount
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal update MataKuliah: {str(e)}")

    def hapus(self, id_or_kode):
        """Hapus mata kuliah berdasarkan id_mk atau kode_mk."""
        try:
            cursor = self.conn.cursor()
            if isinstance(id_or_kode, int):
                cursor.execute("DELETE FROM mata_kuliah WHERE id_mk = %s", (id_or_kode,))
            else:
                cursor.execute("DELETE FROM mata_kuliah WHERE kode_mk = %s", (id_or_kode,))
            self.commit()
            return cursor.rowcount
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal hapus MataKuliah: {str(e)}")

    def tampilkan_semua(self):
        try:
            cursor = self.execute_query("SELECT * FROM mata_kuliah")
            return cursor.fetchall()
        except RepositoryError:
            return []
