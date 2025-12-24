# Sistem Akademik (CLI) — Clean Architecture

Aplikasi **Sistem Akademik** berbasis **terminal/CLI** untuk simulasi proses akademik end-to-end: mulai dari **login**, **pengelolaan mata kuliah**, **pengisian KRS**, **presensi**, sampai **input & melihat nilai**.

Project ini sudah dimigrasikan ke **Clean Architecture** (Domain / Application / Infrastructure / Presentation) agar mudah dipahami saat presentasi dan mudah dikembangkan.

Dokumentasi presentasi super-detail (per folder/file/metode): lihat `DOKUMENTASI_PRESENTASI_DETAIL.md`.

---

## Fitur Utama

### Berdasarkan Role

**Admin**
- Lihat semua mata kuliah
- Tambah mata kuliah (pilih dosen pengampu)
- Edit mata kuliah
- Lihat semua mahasiswa
- Lihat statistik sistem (jumlah mahasiswa/dosen/mk/krs/presensi/nilai)

**Dosen**
- Lihat profil
- Lihat mata kuliah yang diampu
- Buat presensi per mata kuliah + tanggal
- Lihat ringkasan presensi
- Input nilai mahasiswa untuk mata kuliah yang diampu

**Mahasiswa**
- Lihat profil
- Lihat KRS
- Ambil mata kuliah (menambah ke KRS)
- Isi presensi (hanya untuk mata kuliah yang diambil di KRS)
- Lihat nilai + hitung IPK

### Aturan/Validasi Penting
- Password minimal 6 karakter
- Role otomatis dideteksi dari identifier:
	- NIM 9 digit → mahasiswa
	- NIDN 8 digit → dosen
	- lainnya → admin
- KRS tidak boleh duplikat mata kuliah
- Total SKS maksimal 24 (saat ambil KRS)
- Nilai angka dibatasi 0–100
- Presensi: mencegah input hadir dua kali

---

## Prasyarat

- Python 3.12+
- MySQL Server (contoh: XAMPP)
- Database bernama `siak`

### Dependency Python (DB driver)

Project memakai `mysql.connector` (paket: `mysql-connector-python`). Install:

```bash
pip install mysql-connector-python
```

Catatan: `requirements.txt` berisi panduan dependency (tidak memaksa instal otomatis).

---

## Setup Database

1. Jalankan MySQL (misalnya XAMPP Control Panel).
2. Buat database:

```sql
CREATE DATABASE siak;
```

3. Import schema/data dari file `siak.sql` (via phpMyAdmin atau CLI).

---

## Konfigurasi Koneksi DB

File koneksi ada di `infrastructure/database/connection.py`:

- host: `localhost`
- port: `3306`
- user: `root`
- password: `""` (kosong)
- database: `siak`

Kalau setting MySQL kamu beda, ubah parameter di fungsi `get_connection()`.

---

## Cara Menjalankan Aplikasi

Dari root project:

```bash
python main.py
```

Alur saat running:
1. App inisialisasi state + koneksi DB
2. Load data awal via loader
3. Minta login (identifier + password)
4. Route ke menu sesuai role

---

## Alur Sistem (Flow) — Versi Presentasi

1. **Start**: `main.py` membuat instance `SistemAkademik`.
2. **Bootstrap**: `app.py`:
	- membuat `AppState` (in-memory state)
	- koneksi DB via `infrastructure/database/connection.py`
	- load data awal via `loaders/db_loaders.py`
3. **Login**: `application/use_cases/login.py`:
	- `validate_input()` → cek kosong & minimal password
	- `determine_role()` → menentukan role dari format identifier
4. **Menu**: `presentation/menus/*Menu.py` menjalankan loop UI.
5. **Business Logic**: menu memanggil `domain/services/*_service.py`.
6. **Persist (jika ada)**: beberapa aksi memanggil `infrastructure/database/helpers.py`.

---

## Struktur Folder (Ringkas)

```
domain/           # Business entities + business services
application/      # DTO + use cases (contoh: Login)
infrastructure/   # Database connection/helpers + repositories
presentation/     # UI CLI menus + commands + UI helper
loaders/          # Loader untuk load data dari DB ke memory (AppState)
utils/            # Logger & error handling
app.py            # Orchestrator (dependency injection + routing)
main.py           # Entry point
```

Untuk breakdown lengkap sampai level metode: baca `DOKUMENTASI_PRESENTASI_DETAIL.md`.

---

## Desain & Pola (Design Patterns) yang Dipakai

- **Clean Architecture**
	- Domain: entity + aturan bisnis (services)
	- Application: use case (contoh login) + DTO
	- Infrastructure: detail teknis DB + repository
	- Presentation: UI terminal

- **Command Pattern**
	- File: `presentation/commands/commands.py`
	- Tujuan: membungkus aksi menu sebagai objek command (`execute()`, `undo()`).

- **Strategy + Factory (Grading)**
	- File: `domain/entities/grading_strategy.py`
	- Tujuan: konversi nilai bisa diganti skala (standard/strict/lenient) tanpa ubah code lain.

- **Repository Pattern (arah konsistensi data access)**
	- File: `infrastructure/repositories/*.py`
	- Tujuan: abstraksi operasi DB (simpan/cari/update/hapus).

- **Singleton Logger**
	- File: `utils/logger.py`
	- Tujuan: satu instance logger untuk seluruh aplikasi.

---

## Testing (Smoke Test Migrasi)

Untuk memastikan seluruh import layer berjalan:

```bash
python test_migration.py
```

---

## Data Login Dummy (Untuk Testing)

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

- Data login di README ini adalah **dummy data untuk testing** — jangan dipakai di produksi.
- Pastikan MySQL/XAMPP sudah running dan database `siak` sudah di-import dari `siak.sql`.
- Konfigurasi koneksi ada di `infrastructure/database/connection.py`.
- Catatan teknis: beberapa fungsi simpan/update di `infrastructure/database/helpers.py` masih stub (`pass`).

---

## Troubleshooting

### 1) Error: `ModuleNotFoundError` saat menjalankan
- Pastikan menjalankan perintah dari root folder project (folder yang berisi `main.py`).

### 2) Error: gagal koneksi database
- Pastikan MySQL berjalan dan database `siak` ada.
- Cek user/password/port di `infrastructure/database/connection.py`.
- Pastikan sudah install driver: `pip install mysql-connector-python`.

### 3) Catatan implementasi DB helper
Beberapa fungsi simpan/update di `infrastructure/database/helpers.py` masih stub (`pass`).
Kalau fitur simpan belum bekerja penuh, itu area yang perlu dilengkapi query INSERT/UPDATE.

### 4) App jalan tapi fitur tertentu error
- Kemungkinan ada perbedaan bentuk data antara entity/service/menu (misal parameter constructor).
- Untuk bahan presentasi + detail teknis, lihat `DOKUMENTASI_PRESENTASI_DETAIL.md` bagian “Catatan Teknis”.