"""
db/base_repository.py
Base class untuk semua repository.
Implementasi Repository Pattern untuk abstraksi database.
"""

from abc import ABC, abstractmethod


class BaseRepository(ABC):
    """
    Abstract base class untuk semua repository.
    Memastikan interface konsisten untuk semua operasi database.
    """
    
    def __init__(self, conn):
        """
        Args:
            conn: Database connection object
        """
        self.conn = conn
    
    @abstractmethod
    def simpan(self, obj):
        """Simpan object ke database"""
        pass
    
    @abstractmethod
    def cari_by_id(self, id):
        """Cari object berdasarkan ID"""
        pass
    
    @abstractmethod
    def update(self, obj):
        """Update object di database"""
        pass
    
    @abstractmethod
    def hapus(self, obj):
        """Hapus object dari database"""
        pass
    
    @abstractmethod
    def tampilkan_semua(self):
        """Tampilkan semua data"""
        pass
    
    def execute_query(self, query, params=None):
        """
        Execute raw SQL query.
        
        Args:
            query: SQL query string
            params: Query parameters (tuple or dict)
        
        Returns:
            Query result
        """
        try:
            cursor = self.conn.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            return cursor
        except Exception as e:
            raise RepositoryError(f"Database error: {str(e)}")
    
    def commit(self):
        """Commit transaction"""
        try:
            self.conn.commit()
        except Exception as e:
            raise RepositoryError(f"Commit error: {str(e)}")
    
    def rollback(self):
        """Rollback transaction"""
        try:
            self.conn.rollback()
        except Exception as e:
            raise RepositoryError(f"Rollback error: {str(e)}")


class RepositoryError(Exception):
    """Custom exception untuk repository operations"""
    pass
