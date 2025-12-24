"""
akademik/grading_strategy.py
Strategy Pattern untuk flexible grading logic.
Mengganti hardcoded konversi nilai di Nilai class.
"""

from abc import ABC, abstractmethod


class GradingStrategy(ABC):
    """Abstract base class untuk strategi grading"""
    
    @abstractmethod
    def konversi_nilai(self, nilai_angka):
        """
        Konversi nilai angka ke nilai huruf.
        
        Args:
            nilai_angka: Nilai dalam bentuk angka (0-100)
        
        Returns:
            Nilai huruf (A, B+, B, dll) dan bobot angka
        """
        pass
    
    @abstractmethod
    def get_description(self):
        """Deskripsi dari strategi grading"""
        pass


class StandardGradingStrategy(GradingStrategy):
    """
    Strategi grading standar.
    - A: 80-100
    - B+: 75-79
    - B: 70-74
    - C+: 65-69
    - C: 60-64
    - D: 50-59
    - E: <50
    """
    
    def konversi_nilai(self, nilai_angka):
        """Konversi nilai menggunakan skala standar"""
        if nilai_angka >= 80:
            return 'A', 4.0
        elif nilai_angka >= 75:
            return 'A-', 3.7
        elif nilai_angka >= 70:
            return 'B+', 3.3
        elif nilai_angka >= 65:
            return 'B', 3.0
        elif nilai_angka >= 60:
            return 'B-', 2.7
        elif nilai_angka >= 55:
            return 'C+', 2.3
        elif nilai_angka >= 50:
            return 'C', 2.0
        elif nilai_angka >= 45:
            return 'C-', 1.7
        elif nilai_angka >= 40:
            return 'D+', 1.3
        elif nilai_angka >= 35:
            return 'D', 1.0
        else:
            return 'E', 0.0
    
    def get_description(self):
        return "Skala Standar (A=80+, B+=75+, B=70+, C+=65+, C=60+, D+=40+, E=<35)"


class StrictGradingStrategy(GradingStrategy):
    """
    Strategi grading ketat.
    - A: 85-100
    - B+: 80-84
    - B: 75-79
    - C+: 70-74
    - C: 65-69
    - D: 50-64
    - E: <50
    """
    
    def konversi_nilai(self, nilai_angka):
        """Konversi nilai menggunakan skala ketat"""
        if nilai_angka >= 85:
            return 'A', 4.0
        elif nilai_angka >= 80:
            return 'B+', 3.3
        elif nilai_angka >= 75:
            return 'B', 3.0
        elif nilai_angka >= 70:
            return 'B-', 2.7
        elif nilai_angka >= 65:
            return 'C+', 2.3
        elif nilai_angka >= 60:
            return 'C', 2.0
        elif nilai_angka >= 55:
            return 'C-', 1.7
        elif nilai_angka >= 50:
            return 'D', 1.0
        else:
            return 'E', 0.0
    
    def get_description(self):
        return "Skala Ketat (A=85+, B+=80+, B=75+, C+=70+, C=65+, D=50+, E=<50)"


class LenientGradingStrategy(GradingStrategy):
    """
    Strategi grading lenient.
    - A: 75-100
    - B+: 70-74
    - B: 65-69
    - C+: 60-64
    - C: 55-59
    - D: 45-54
    - E: <45
    """
    
    def konversi_nilai(self, nilai_angka):
        """Konversi nilai menggunakan skala lenient"""
        if nilai_angka >= 75:
            return 'A', 4.0
        elif nilai_angka >= 70:
            return 'B+', 3.3
        elif nilai_angka >= 65:
            return 'B', 3.0
        elif nilai_angka >= 60:
            return 'B-', 2.7
        elif nilai_angka >= 55:
            return 'C+', 2.3
        elif nilai_angka >= 50:
            return 'C', 2.0
        elif nilai_angka >= 45:
            return 'C-', 1.7
        elif nilai_angka >= 40:
            return 'D+', 1.3
        elif nilai_angka >= 35:
            return 'D', 1.0
        else:
            return 'E', 0.0
    
    def get_description(self):
        return "Skala Lenient (A=75+, B+=70+, B=65+, C+=60+, C=55+, D+=40+, E=<35)"


class GradingFactory:
    """Factory untuk membuat grading strategy instances"""
    
    _strategies = {
        'standard': StandardGradingStrategy,
        'strict': StrictGradingStrategy,
        'lenient': LenientGradingStrategy
    }
    
    @classmethod
    def create_strategy(cls, strategy_type='standard'):
        """
        Buat strategy berdasarkan tipe.
        
        Args:
            strategy_type: Tipe strategi ('standard', 'strict', 'lenient')
        
        Returns:
            GradingStrategy instance
        
        Raises:
            ValueError: Jika strategy_type tidak dikenal
        """
        if strategy_type not in cls._strategies:
            raise ValueError(
                f"Strategy tidak dikenal: {strategy_type}. "
                f"Pilihan: {', '.join(cls._strategies.keys())}"
            )
        return cls._strategies[strategy_type]()
    
    @classmethod
    def get_available_strategies(cls):
        """Dapatkan daftar strategi yang tersedia"""
        return list(cls._strategies.keys())
