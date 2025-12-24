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


# Database persistence functions (stub implementations for migration)
def simpan_mata_kuliah(conn, mk):
    """Simpan mata kuliah ke database (stub)"""
    pass


def update_mata_kuliah(conn, mk):
    """Update mata kuliah ke database (stub)"""
    pass


def simpan_krs(conn, krs, daftar_mk=None):
    """Simpan KRS ke database (stub)"""
    pass


def simpan_nilai(conn, nilai):
    """Simpan nilai ke database (stub)"""
    pass
