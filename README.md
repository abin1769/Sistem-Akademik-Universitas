# SISTEM AKADEMIK - DATA LOGIN DUMMY

## Data Login untuk Testing

Sistem ini memiliki 3 tipe user dengan cara login yang berbeda:

### 1. ADMIN (Login dengan Username)
Admin login menggunakan **username** dan **password**.

| Username | Password | Nama | Email |
|----------|----------|------|-------|
| admin | admin123 | Admin Sistem | admin@univ.ac.id |
| superadmin | superpass123 | Super Admin | superadmin@univ.ac.id |

**Cara Login Admin:**
- Identifier: `admin` atau `superadmin`
- Password: sesuai tabel di atas
- Minimal password: 6 karakter

---

### 2. DOSEN/PENGAJAR (Login dengan NIDN)
Dosen login menggunakan **NIDN** (8 digit angka) dan **password**.

| NIDN | Password | Nama | Departemen |
|------|----------|------|-----------|
| 12345678 | dosen123 | Dr. Budi Santoso | Teknik Informatika |
| 87654321 | dosen456 | Prof. Siti Nurhaliza | Sistem Informasi |
| 11223344 | dosen789 | Dr. Ahmad Hidayat | Teknik Komputer |

**Cara Login Dosen:**
- Identifier: `12345678` (NIDN - 8 digit)
- Password: sesuai tabel di atas
- Minimal password: 6 karakter

---

### 3. MAHASISWA/SISWA (Login dengan NIM)
Mahasiswa login menggunakan **NIM** (9 digit angka) dan **password**.

| NIM | Password | Nama | Program Studi | Angkatan |
|-----|----------|------|--------------|----------|
| 230000001 | mhs123450 | Andi Wijaya | Teknik Informatika | 2022 |
| 987654321 | mahasiswa2 | Siti Rahayu | Teknik Informatika | 2022 |
| 456789123 | mahasiswa3 | Rudi Hermawan | Sistem Informasi | 2023 |
| 789123456 | mahasiswa4 | Dewi Lestari | Teknik Komputer | 2023 |

**Cara Login Mahasiswa:**
- Identifier: `123456789` (NIM - 9 digit)
- Password: sesuai tabel di atas
- Minimal password: 6 karakter

---

## Aturan Login

1. **Admin**: Username (non-numeric) + Password
2. **Dosen**: NIDN (8 digit numeric) + Password
3. **Mahasiswa**: NIM (9 digit numeric) + Password

Sistem akan otomatis mendeteksi tipe user berdasarkan format identifier yang dimasukkan.

---

## Menu Akses Sesuai Role

### Menu Admin
- Lihat semua mata kuliah
- Tambah mata kuliah baru
- Edit mata kuliah
- Lihat semua mahasiswa

### Menu Dosen
- Lihat profil
- Lihat daftar mata kuliah yang diampu
- Isi presensi untuk mata kuliah
- Input nilai mahasiswa
- Lihat mahasiswa yang terdaftar

### Menu Mahasiswa
- Lihat profil
- Lihat KRS (Kartu Rencana Studi)
- Ambil mata kuliah (isi KRS)
- Isi presensi
- Lihat nilai

---

## Catatan Penting

- **Password minimal 6 karakter** untuk semua user
- Data ini adalah **dummy data untuk testing** - JANGAN gunakan di produksi
- Sebelum pakai, pastikan database MySQL/XAMPP sudah running dan sudah ada database `siak`
- Koneksi database di db.py - sesuaikan username/password MySQL Anda 