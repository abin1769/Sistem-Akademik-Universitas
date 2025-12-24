"""
infrastructure/repositories/nilai_repository.py
Concrete implementation dari BaseRepository untuk Nilai.
"""

from infrastructure.repositories.base_repository import BaseRepository, RepositoryError


class NilaiRepository(BaseRepository):
    """Repository untuk entity Nilai"""
    
    def simpan(self, nilai_obj):
        """
        Simpan Nilai ke database.
        
        Args:
            nilai_obj: Objek Nilai
        
        Raises:
            RepositoryError: Jika query gagal
        """
        try:
            cursor = self.conn.cursor()
            
            query = """
                INSERT INTO nilai (id_dosen, id_mk, id_mahasiswa, nilai_angka)
                VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (
                nilai_obj.dosen.id,
                nilai_obj.mata_kuliah.id_mk,
                nilai_obj.mahasiswa.id,
                nilai_obj.nilai_angka
            ))
            
            self.commit()
            return cursor.lastrowid
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal simpan Nilai: {str(e)}")
    
    def cari_by_id(self, nilai_id):
        """Cari Nilai berdasarkan ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM nilai WHERE id_nilai = %s",
                (nilai_id,)
            )
            result = cursor.fetchone()
            return result if result else None
        except RepositoryError:
            return None
    
    def cari_by_mahasiswa(self, mahasiswa_id):
        """Cari nilai berdasarkan mahasiswa ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM nilai WHERE id_mahasiswa = %s",
                (mahasiswa_id,)
            )
            return cursor.fetchall()
        except RepositoryError:
            return []
    
    def cari_by_dosen(self, dosen_id):
        """Cari nilai berdasarkan dosen ID"""
        try:
            cursor = self.execute_query(
                "SELECT * FROM nilai WHERE id_dosen = %s",
                (dosen_id,)
            )
            return cursor.fetchall()
        except RepositoryError:
            return []
    
    def update(self, nilai_obj):
        """Update Nilai di database"""
        try:
            cursor = self.conn.cursor()
            query = """
                UPDATE nilai 
                SET nilai_angka = %s
                WHERE id_mahasiswa = %s AND id_mk = %s
            """
            cursor.execute(query, (
                nilai_obj.nilai_angka,
                nilai_obj.mahasiswa.id,
                nilai_obj.mata_kuliah.id_mk
            ))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal update Nilai: {str(e)}")
    
    def hapus(self, nilai_id):
        """Hapus Nilai dari database"""
        try:
            cursor = self.conn.cursor()
            cursor.execute("DELETE FROM nilai WHERE id_nilai = %s", (nilai_id,))
            self.commit()
        except Exception as e:
            self.rollback()
            raise RepositoryError(f"Gagal hapus Nilai: {str(e)}")
    
    def tampilkan_semua(self):
        """Tampilkan semua Nilai"""
        try:
            cursor = self.execute_query("SELECT * FROM nilai")
            return cursor.fetchall()
        except RepositoryError:
            return []
