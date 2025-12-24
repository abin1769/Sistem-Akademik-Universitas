# ============================
# MAIN PROGRAM
# ===============================

from app import SistemAkademik

if __name__ == "__main__":
    sistem = SistemAkademik()

    while True:
        sistem.login()
        lagi = input("\nIngin login lagi? (y/n): ").lower()
        if lagi == 'n':
            print("Keluar dari sistem.")
            break
        elif lagi != 'y':
            print("Input tidak valid. Keluar dari sistem.")
            break
            