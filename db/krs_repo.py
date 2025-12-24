from db.helpers import get_mahasiswa_id_by_nim, get_mk_id_by_kode

def simpan_krs(conn, krs_obj, mk_list):
    if conn is None:
        return

    cursor = conn.cursor()

    id_mahasiswa = get_mahasiswa_id_by_nim(conn, krs_obj.mahasiswa.nim)
    if id_mahasiswa is None:
        cursor.close()
        return

    sql_krs = """
        INSERT INTO krs (id_mahasiswa, semester, tahun_ajaran)
        VALUES (%s, %s, %s)
    """
    cursor.execute(sql_krs, (id_mahasiswa, krs_obj.semester, krs_obj.tahun_ajaran))
    id_krs = cursor.lastrowid

    sql_detail = """
        INSERT INTO krs_detail (id_krs, id_mk)
        VALUES (%s, %s)
    """

    for mk in mk_list:
        id_mk = get_mk_id_by_kode(conn, mk.kode_mk)
        if id_mk:
            cursor.execute(sql_detail, (id_krs, id_mk))

    conn.commit()
    cursor.close()
