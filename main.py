# ============================
# MAIN PROGRAM
# ============================

from siak import SistemAkademik

if __name__ == "__main__":
    sistem = SistemAkademik()

    while True:
        sistem.login()
        lagi = input("\nIngin login lagi? (y/n): ").lower()
        if lagi != 'y':
            print("Keluar dari sistem.")
            break