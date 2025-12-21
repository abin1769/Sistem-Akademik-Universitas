# db.py
import mysql.connector
from mysql.connector import Error


# -----------------------------
# KONEKSI KE DATABASE
# -----------------------------
def get_connection():
    """
    Mengembalikan object koneksi ke MySQL (XAMPP).
    SESUAIKAN:
        - user
        - password
        - database
    dengan setting di XAMPP / phpMyAdmin kalian.
    """
    try:
        conn = mysql.connector.connect(
            host="localhost",
            port=3306,
            user="root",          # default XAMPP
            password="",          # kalau pakai password, ganti di sini
            database="siak"
        )
        if conn.is_connected():
            return conn
    except Error as e:
        print("Gagal koneksi ke database:", e)
        return None


# -----------------------------
# HELPER FUNGSI UMUM
# -----------------------------
def get_mahasiswa_id_by_nim(conn, nim):
    cursor = conn.cursor()
    cursor.execute("SELECT id_mahasiswa FROM mahasiswa WHERE nim = %s", (nim,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_mk_id_by_kode(conn, kode_mk):
    cursor = conn.cursor()
    cursor.execute("SELECT id_mk FROM mata_kuliah WHERE kode_mk = %s", (kode_mk,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


def get_dosen_id_by_nidn(conn, nidn):
    cursor = conn.cursor()
    cursor.execute("SELECT id_dosen FROM dosen WHERE nidn = %s", (nidn,))
    row = cursor.fetchone()
    cursor.close()
    return row[0] if row else None


# -----------------------------
# SIMPAN / EDIT MATA KULIAH
# -----------------------------
def simpan_mata_kuliah(conn, mk):
    """
    Insert 1 mata kuliah baru ke tabel mata_kuliah.
    mk : objek MataKuliah
    """
    if conn is None:
        print("Koneksi database tidak tersedia.")
        return

    cursor = conn.cursor()

    # ambil id_dosen berdasarkan NIDN dari objek Dosen
    id_dosen = None
    if mk.dosen is not None:
        id_dosen = get_dosen_id_by_nidn(conn, mk.dosen.nidn)

    # NOTE:
    # jika tabel mata_kuliah KAMU tidak punya kolom id_dosen,
    # pakai query tanpa id_dosen (hapus bagian itu).
    sql = """
        INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, id_dosen)
        VALUES (%s, %s, %s, %s)
    """
    data = (mk.kode_mk, mk.nama_mk, mk.sks, id_dosen)

    try:
        cursor.execute(sql, data)
        conn.commit()
        print("Mata kuliah berhasil disimpan ke database.")
    except Error as e:
        print("Gagal menyimpan mata kuliah:", e)
    finally:
        cursor.close()


def update_mata_kuliah(conn, mk, kode_lama):
    """
    Update data mata kuliah di tabel mata_kuliah.
    mk        : objek MataKuliah (data terbaru)
    kode_lama : kode MK sebelum diedit (dipakai di WHERE)
    """
    if conn is None:
        print("Koneksi database tidak tersedia.")
        return

    cursor = conn.cursor()

    id_dosen = None
    if mk.dosen is not None:
        id_dosen = get_dosen_id_by_nidn(conn, mk.dosen.nidn)

    sql = """
        UPDATE mata_kuliah
        SET kode_mk = %s,
            nama_mk = %s,
            sks     = %s,
            id_dosen = %s
        WHERE kode_mk = %s
    """
    data = (mk.kode_mk, mk.nama_mk, mk.sks, id_dosen, kode_lama)

    try:
        cursor.execute(sql, data)
        conn.commit()
        if cursor.rowcount > 0:
            print("Mata kuliah berhasil diupdate di database.")
        else:
            print("Mata kuliah tidak ditemukan di database (tidak ada yang diupdate).")
    except Error as e:
        print("Gagal mengupdate mata kuliah:", e)
    finally:
        cursor.close()


#hapus MK
def hapus_mata_kuliah(conn, kode_mk):
    """
    Menghapus mata kuliah dari tabel mata_kuliah berdasarkan kode_mk.
    WARNING: perhatikan relasi dengan krs_detail / nilai.
    """
    if conn is None:
        print("Koneksi database tidak tersedia.")
        return

    cursor = conn.cursor()
    sql = "DELETE FROM mata_kuliah WHERE kode_mk = %s"
    try:
        cursor.execute(sql, (kode_mk,))
        conn.commit()
        print("Mata kuliah berhasil dihapus dari database.")
    except Error as e:
        print("Gagal menghapus mata kuliah:", e)
    finally:
        cursor.close()


# -----------------------------
# SIMPAN KRS
# -----------------------------
def simpan_krs(conn, krs_obj, mk_list):
    """
    Menyimpan 1 KRS ke tabel krs + krs_detail.
    """
    if conn is None:
        print("Koneksi database tidak tersedia.")
        return

    cursor = conn.cursor()

    nim = krs_obj.mahasiswa.nim
    id_mahasiswa = get_mahasiswa_id_by_nim(conn, nim)

    if id_mahasiswa is None:
        print(f"Mahasiswa dengan NIM {nim} belum ada di tabel 'mahasiswa'.")
        cursor.close()
        return

    sql_krs = """
        INSERT INTO krs (id_mahasiswa, semester, tahun_ajaran)
        VALUES (%s, %s, %s)
    """
    data_krs = (id_mahasiswa, krs_obj.semester, krs_obj.tahun_ajaran)
    cursor.execute(sql_krs, data_krs)
    id_krs = cursor.lastrowid

    sql_krs_detail = """
        INSERT INTO krs_detail (id_krs, id_mk)
        VALUES (%s, %s)
    """

    for mk in mk_list:
        id_mk = get_mk_id_by_kode(conn, mk.kode_mk)
        if id_mk is None:
            print(f"PERINGATAN: MK dengan kode {mk.kode_mk} belum ada di tabel 'mata_kuliah'. Dilewati.")
            continue
        cursor.execute(sql_krs_detail, (id_krs, id_mk))

    conn.commit()
    cursor.close()
    print("KRS berhasil disimpan ke database.")


# -----------------------------
# SIMPAN NILAI
# -----------------------------
def simpan_nilai(conn, nilai_obj):
    """
    Menyimpan nilai ke tabel 'nilai'.
    """
    if conn is None:
        print("Koneksi database tidak tersedia.")
        return

    cursor = conn.cursor()

    nim = nilai_obj.mahasiswa.nim
    kode_mk = nilai_obj.mata_kuliah.kode_mk

    id_mahasiswa = get_mahasiswa_id_by_nim(conn, nim)
    id_mk = get_mk_id_by_kode(conn, kode_mk)

    if id_mahasiswa is None or id_mk is None:
        print("Data mahasiswa / mata kuliah belum ada di database.")
        cursor.close()
        return

    sql_nilai = """
        INSERT INTO nilai (id_mahasiswa, id_mk, nilai_angka, nilai_huruf)
        VALUES (%s, %s, %s, %s)
    """
    data_nilai = (
        id_mahasiswa,
        id_mk,
        nilai_obj.nilai_angka,
        nilai_obj.nilai_huruf
    )

    cursor.execute(sql_nilai, data_nilai)
    conn.commit()
    cursor.close()
    print("Nilai berhasil disimpan ke database.")


# -----------------------------
# TEST SINGKAT (opsional)
# -----------------------------
if __name__ == "__main__":
    conn = get_connection()
    if conn:
        print("Koneksi OK ke database 'sistem_akademik'.")
        conn.close()
