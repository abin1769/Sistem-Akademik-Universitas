from db.helpers import get_mahasiswa_id_by_nim, get_mk_id_by_kode

def simpan_nilai(conn, nilai_obj):
    if conn is None:
        return

    cursor = conn.cursor()

    id_mahasiswa = get_mahasiswa_id_by_nim(conn, nilai_obj.mahasiswa.nim)
    id_mk = get_mk_id_by_kode(conn, nilai_obj.mata_kuliah.kode_mk)

    if id_mahasiswa is None or id_mk is None:
        cursor.close()
        return

    sql = """
        INSERT INTO nilai (id_mahasiswa, id_mk, nilai_angka, nilai_huruf)
        VALUES (%s, %s, %s, %s)
    """
    data = (
        id_mahasiswa,
        id_mk,
        nilai_obj.nilai_angka,
        nilai_obj.nilai_huruf
    )

    cursor.execute(sql, data)
    conn.commit()
    cursor.close()

