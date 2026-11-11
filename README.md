
# Digital Guestbook

## Deskripsi
Digital Guestbook merupakan aplikasi buku tamu digital berbasis web yang digunakan untuk mencatat data pengunjung secara online.

## Teknologi yang Digunakan
- Ubuntu Linux 24.04
- Python
- HTML, CSS, JavaScript
- Nginx
- Docker
- Docker Compose

## Fitur
- Menambahkan data pengunjung
- Melihat daftar pengunjung
- Menghapus data pengunjung
- Penyimpanan data menggunakan Docker Named Volume

## Arsitektur
- Frontend menggunakan Nginx
- Backend menggunakan Python
- Komunikasi melalui REST API
- Container dihubungkan menggunakan Docker Bridge Network

## Cara Menjalankan
Jalankan perintah:

```bash
docker compose up -d --build
```

Buka aplikasi melalui:

http://localhost:8080

## Pengujian
Aplikasi telah diuji menggunakan fungsi GET, POST, DELETE serta pengujian Data Persistence.
