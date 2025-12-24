"""
infrastructure/repositories/krs_repository.py
Concrete implementation dari BaseRepository untuk KRS.
"""

from infrastructure.repositories.base_repository import BaseRepository, RepositoryError
from domain.entities.krs import KRS


class KRSRepository(BaseRepository):
    """Repository untuk entity KRS"""
    
    def simpan(self, krs_obj):
        """
        Simpan KRS ke database.
        
        Args:
            krs_obj: Objek KRS
        
        Raises:
            RepositoryError: Jika query gagal
        """
        try:
            cursor = self.conn.cursor()
            
            # Insert KRS header
            query = """
                INSERT INTO krs (id_mahasiswa, semester, tahun_ajaran)
                VALUES (%s, %s, %s)
            """
            cursor.execute(query, (
                krs_obj.mahasiswa.id,
                1,  # Semester (default 1)
                '2025/2026'  # Tahun ajaran
            ))
            
            krs_id = cursor.lastrowid
            
            # Insert KRS detail
            for mk in krs_obj.daftar_mk:
                detail_query = """
                    INSERT INTO krs_detail (id_krs, id_mk)
                    VALUES (%s, %s)
                """
                cursor.execute(detail_query, (krs_id, mk.id_mk))
            
            self.commit()
            return krs_id
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal simpan KRS: {str(e)}")
    
    def cari_by_id(self, krs_id):
        """Cari KRS berdasarkan ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM krs WHERE id_krs = %s",
                (krs_id,)
            )
            result = cursor.fetchone()
            return result if result else None
        except RepositoryError:
            return None
    
    def update(self, krs_obj):
        """Update KRS di database"""
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE krs SET semester = %s, tahun_ajaran = %s
                WHERE id_mahasiswa = %s
            """
            cursor.execute(query, (1, '2025/2026', krs_obj.mahasiswa.id))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal update KRS: {str(e)}")
    
    def hapus(self, krs_id):
        """Hapus KRS dari database"""
        try:
            cursor = self.conn.cursor()
            
            # Delete KRS detail terlebih dahulu
            cursor.execute("DELETE FROM krs_detail WHERE id_krs = %s", (krs_id,))
            
            # Delete KRS
            cursor.execute("DELETE FROM krs WHERE id_krs = %s", (krs_id,))
            
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal hapus KRS: {str(e)}")
    
    def tampilkan_semua(self):
        """Tampilkan semua KRS"""
        try:
            cursor = self.execute_query("SELECT * FROM krs")
            return cursor.fetchall()
        except RepositoryError:
            return []
