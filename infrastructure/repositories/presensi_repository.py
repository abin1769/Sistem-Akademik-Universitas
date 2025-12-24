"""
infrastructure/repositories/presensi_repository.py
Concrete implementation dari BaseRepository untuk Presensi.
"""

from infrastructure.repositories.base_repository import BaseRepository, RepositoryError


class PresensiRepository(BaseRepository):
    """Repository untuk entity Presensi"""
    
    def simpan(self, presensi_obj):
        """
        Simpan Presensi ke database.
        
        Args:
            presensi_obj: Objek Presensi
        
        Raises:
            RepositoryError: Jika query gagal
        """
        try:
            cursor = self.conn.cursor()
            
            query = """
                INSERT INTO presensi (id_dosen, id_mk, tanggal)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (
                presensi_obj.dosen.id,
                presensi_obj.mata_kuliah.id_mk,
                presensi_obj.tanggal
            ))
            
            self.commit()
            return cursor.lastrowid
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal simpan Presensi: {str(e)}")
    
    def cari_by_id(self, presensi_id):
        """Cari Presensi berdasarkan ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM presensi WHERE id_presensi = %s",
                (presensi_id,)
            )
            result = cursor.fetchone()
            return result if result else None
        except RepositoryError:
            return None
    
    def cari_by_dosen(self, dosen_id):
        """Cari presensi berdasarkan dosen ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM presensi WHERE id_dosen = %s",
                (dosen_id,)
            )
            return cursor.fetchall()
        except RepositoryError:
            return []
    
    def cari_by_mata_kuliah(self, mata_kuliah_id):
        """Cari presensi berdasarkan mata kuliah ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM presensi WHERE id_mk = %s",
                (mata_kuliah_id,)
            )
            return cursor.fetchall()
        except RepositoryError:
            return []
    
    def update(self, presensi_obj):
        """Update Presensi di database"""
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE presensi 
                SET tanggal = %s
                WHERE id_presensi = %s
            """
            cursor.execute(query, (
                presensi_obj.tanggal,
                presensi_obj.id
            ))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal update Presensi: {str(e)}")
    
    def hapus(self, presensi_id):
        """Hapus Presensi dari database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM presensi WHERE id_presensi = %s", (presensi_id,))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal hapus Presensi: {str(e)}")
    
    def tambah_hadir(self, presensi_id, mahasiswa_id):
        """Tambahkan mahasiswa ke daftar hadir"""
        try:
            cursor = self.conn.cursor()
            query = """
                INSERT INTO presensi_detail (id_presensi, id_mahasiswa)
                VALUES (%s, %s)
            """
            cursor.execute(query, (presensi_id, mahasiswa_id))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal tambah hadir: {str(e)}")
    
    def tampilkan_semua(self):
        """Tampilkan semua Presensi"""
        try:
            cursor = self.execute_query("SELECT * FROM presensi")
            return cursor.fetchall()
        except RepositoryError:
            return []
