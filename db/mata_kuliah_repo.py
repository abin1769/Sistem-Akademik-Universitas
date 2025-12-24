from db.helpers import get_dosen_id_by_nidn

def simpan_mata_kuliah(conn, mk):
    if conn is None:
        return

    cursor = conn.cursor()

    id_dosen = None
    if mk.dosen:
        id_dosen = get_dosen_id_by_nidn(conn, mk.dosen.nidn)

    sql = """
        INSERT INTO mata_kuliah (kode_mk, nama_mk, sks, id_dosen)
        VALUES (%s, %s, %s, %s)
    """
    data = (mk.kode_mk, mk.nama_mk, mk.sks, id_dosen)

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()


def update_mata_kuliah(conn, mk, kode_lama):
    if conn is None:
        return

    cursor = conn.cursor()

    id_dosen = None
    if mk.dosen:
        id_dosen = get_dosen_id_by_nidn(conn, mk.dosen.nidn)

    sql = """
        UPDATE mata_kuliah
        SET kode_mk=%s, nama_mk=%s, sks=%s, id_dosen=%s
        WHERE kode_mk=%s
    """
    data = (mk.kode_mk, mk.nama_mk, mk.sks, id_dosen, kode_lama)

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()
