# 🌐 Web Server TCP dengan Socket Programming

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.9+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Socket.io](https://img.shields.io/badge/Socket.io-010101?style=for-the-badge&logo=socket.io&logoColor=white)](https://socket.io/)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
[![HTML5](https://img.shields.io/badge/HTML5-E34C26?style=for-the-badge&logo=html5&logoColor=white)](https://html.spec.whatwg.org/)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)](https://www.w3.org/Style/CSS/)

<p align="center">
  <strong>Tugas Besar Jaringan Komputer - Kelompok 3</strong><br>
  Implementasi web server berbasis TCP dengan socket programming untuk menangani request HTTP
</p>
</div>

---

## 📋 Daftar Isi
- [🌟 Overview](#-overview)
- [✨ Fitur Utama](#-fitur-utama)
- [🛠️ Teknologi](#️-teknologi)
- [📁 Struktur Proyek](#-struktur-proyek)
- [⚙️ Instalasi & Setup](#️-instalasi--setup)
- [🚀 Cara Penggunaan](#-cara-penggunaan)
- [📖 Dokumentasi API](#-dokumentasi-api)
- [🌐 Antarmuka Web](#-antarmuka-web)
- [🎯 Spesifikasi Tugas](#-spesifikasi-tugas)
- [👥 Tim Pengembang](#-tim-pengembang)
- [📝 Lisensi](#-lisensi)

---

## 🌟 Overview

Proyek ini merupakan implementasi web server berbasis TCP menggunakan socket programming dalam Python. Server dapat menangani permintaan HTTP, melayani file statis, dan mengelola beberapa koneksi secara bersamaan menggunakan multithreading. Proyek ini juga menyertakan client HTTP untuk testing dan antarmuka web interaktif dengan tema jaringan komputer.

---

## ✨ Fitur Utama

### Server Features
- 🔌 **TCP Socket Server**: Implementasi server TCP menggunakan socket programming
- 🧵 **Multithreading**: Menangani beberapa koneksi client secara bersamaan
- 📁 **File Serving**: Melayani file HTML, CSS, JavaScript, dan gambar
- 🚫 **Custom 404 Page**: Halaman error 404 kustom yang menarik
- 📝 **HTTP Parsing**: Parse dan handle HTTP GET requests
- 🔍 **MIME Type Detection**: Deteksi otomatis content type berdasarkan ekstensi file

### Client Features
- 📡 **HTTP Client**: Client sederhana untuk testing server
- 📋 **Response Display**: Menampilkan header dan body response
- ⏱️ **Timeout Handling**: Handling timeout untuk koneksi yang lambat

### Web Interface Features
- 🌙 **Dark/Light Mode**: Toggle tema gelap/terang
- 👥 **Team Profiles**: Card interaktif untuk profil anggota tim
- ✨ **Network Animations**: Animasi bertema jaringan komputer
- 📱 **Responsive Design**: Desain yang responsif untuk berbagai perangkat
- 🎭 **Modal Dialogs**: Detail profil dengan modal yang elegan

---

## 🛠️ Teknologi

<table>
  <tr>
    <td>
      <h3>Backend</h3>
      <ul>
        <li>Python 3.9+</li>
        <li>Socket Programming</li>
        <li>Threading</li>
        <li>HTTP Protocol</li>
      </ul>
    </td>
    <td>
      <h3>Frontend</h3>
      <ul>
        <li>HTML5</li>
        <li>CSS3 (dengan animasi)</li>
        <li>JavaScript (ES6+)</li>
        <li>Font Awesome Icons</li>
      </ul>
    </td>
  </tr>
</table>

---

## 📁 Struktur Proyek

```
tugas-besar-jarkom/
├── server.py            # Main web server implementation
├── client.py            # HTTP client untuk testing
├── klien.py            # Versi client dalam bahasa Indonesia
├── page.html           # Homepage dengan profil tim
├── 404.html            # Custom 404 error page
├── control.js          # JavaScript untuk interaksi UI
├── design.css          # Styling untuk website
├── *.jpg               # Foto profil anggota tim
└── README.md           # Dokumentasi proyek
```

---

## ⚙️ Instalasi & Setup

### Prerequisites
- Python 3.9 atau lebih tinggi
- Web browser modern (Chrome, Firefox, Safari, Edge)

### Instalasi
1. Clone repository
```bash
git clone https://github.com/username/tugas-besar-jarkom.git
cd tugas-besar-jarkom
```

2. Tidak ada dependencies tambahan yang diperlukan. Server menggunakan library standard Python.

---

## 🚀 Cara Penggunaan

### Menjalankan Server

1. Jalankan server pada port default (6789):
```bash
python server.py
```

2. Atau jalankan pada port custom:
```bash
python server.py 8080
```

3. Server akan berjalan di `http://localhost:6789` (atau port yang Anda pilih)

### Menjalankan Client

Untuk testing server menggunakan client:

```bash
python client.py localhost 6789 page.html
```

Format command:
```bash
python client.py <server_host> <server_port> <filename>
```

### Mengakses Web Interface

1. Buka browser
2. Akses `http://localhost:6789/page.html`
3. Atau akses `http://localhost:6789/` (akan redirect ke page.html)

---

## 📖 Dokumentasi API

### HTTP Request Format
```http
GET /filename HTTP/1.1
Host: localhost:6789
Connection: close
```

### HTTP Response Format
```http
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 1234
Connection: close

[Content Body]
```

### Status Codes
- `200 OK`: File berhasil ditemukan dan dikirim
- `404 Not Found`: File tidak ditemukan (menampilkan 404.html)
- `501 Not Implemented`: Method selain GET tidak didukung

### MIME Types Support
- `.html`: text/html
- `.css`: text/css
- `.js`: application/javascript
- `.jpg/.jpeg`: image/jpeg
- `.png`: image/png

---

## 🌐 Antarmuka Web

### Halaman Utama (page.html)
- Hero section dengan animasi network
- Profile cards untuk anggota tim
- Dark/Light mode toggle
- Responsive layout

### Halaman 404 (404.html)
- Custom error page dengan animasi
- Network-themed design
- Link kembali ke homepage

### Fitur Interaktif
- **Profile Cards**: Klik untuk melihat detail lengkap
- **Theme Toggle**: Switch antara dark dan light mode
- **Smooth Animations**: Transisi dan efek hover yang halus
- **Toast Notifications**: Notifikasi saat server berhasil diakses

---

## 🎯 Spesifikasi Tugas

Proyek ini memenuhi semua spesifikasi tugas:

✅ **Server TCP dengan Socket Programming**
- Menerima dan parsing HTTP request
- Mengambil file dari sistem file
- Membuat HTTP response dengan header yang sesuai

✅ **Handling File Not Found**
- Mengirim HTTP 404 response
- Menampilkan custom 404 page

✅ **Multithreading**
- Thread utama listening di port tertentu
- Thread terpisah untuk setiap koneksi client
- Melayani beberapa request secara simultan

✅ **HTTP Client untuk Testing**
- Koneksi TCP ke server
- Mengirim HTTP GET request
- Menampilkan response dari server

---

## 👥 Tim Pengembang

<div align="center">
<table>
  <tr>
    <td align="center">
      <h3>Syahril Arfian Almazril</h3>
      <p>NIM: 103032300013</p>
    </td>
    <td align="center">
      <h3>Nauval Yusriya Athala</h3>
      <p>NIM: 103032300xxx</p>
    </td>
    <td align="center">
      <h3>Muhammad Arief Ridwan Syah</h3>
      <p>NIM: 103032300xxx</p>
    </td>
  </tr>
</table>

**Kelas**: IT-47-04  
**Mata Kuliah**: Jaringan Komputer  
**Universitas**: Telkom University
</div>

---

## 📝 Lisensi

<div align="center">
  
© 2025 Kelompok 3 - Tugas Besar Jaringan Komputer  
Telkom University

</div>
