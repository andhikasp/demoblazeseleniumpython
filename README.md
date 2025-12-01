Demoblaze Automation Framework 🚀

Submission for QA Engineer Technical Assignment - Part 3 (Automation Project)

Repository ini berisi solusi automation testing untuk platform E-Commerce. Project ini dibangun menggunakan Python dan Selenium WebDriver dengan pendekatan Page Object Model (POM) untuk memastikan kode yang bersih, modular, dan mudah dipelihara.

📋 1. Overview Solusi

Solusi ini dirancang untuk mengotomatisasi Critical User Journey pada aplikasi E-Commerce. Arsitektur framework dipilih untuk memenuhi standar industri modern dengan fokus pada scalability dan reliability.

Tech Stack: Python 3.x, Selenium 4, Pytest.

Design Pattern: Page Object Model (POM) — Memisahkan logic test dari elemen UI.

Reporting: HTML Report terintegrasi dengan screenshot otomatis pada step yang gagal.

Data Strategy: Penggunaan data dinamis (Random Generator) untuk User Registration agar test dapat dijalankan berulang kali (Idempotent).

⚠️ 2. Challenges & Key Decisions

Berdasarkan analisis terhadap instruksi soal dan environment yang tersedia, berikut adalah keputusan strategis yang diambil:

A. Perubahan Target Aplikasi 

Challenge: Instruksi soal meminta otomatisasi untuk "User Registration Flow". Namun, environment yang disediakan (saucedemo.com) adalah website demo statis yang tidak memiliki fitur pendaftaran user.

Decision: Saya memutuskan untuk menggunakan Demoblaze.com sebagai System Under Test pengganti. Platform ini memiliki fitur E-Commerce lengkap (Sign Up, Login, Cart, Purchase), sehingga memungkinkan saya untuk mendemonstrasikan kemampuan scripting registrasi sesuai persyaratan soal.

B. Lingkup API Testing

Challenge: Instruksi soal menyediakan environment API (jsonplaceholder), namun pada Bagian 3 (Automation) tidak ada instruksi eksplisit untuk membuat script API, hanya fokus pada UI Flow (Register, Login, Cart).

Decision: Fokus repository ini adalah UI/Web Automation. Strategi pengujian API telah saya jelaskan secara konseptual pada dokumen Test Strategy (Bagian 1) sebagai layer pengujian backend, namun tidak diimplementasikan dalam kode repository ini agar tetap sesuai dengan scope waktu pengerjaan (3 hari).

C. Isu Keamanan Browser 

Challenge: Chrome modern mendeteksi interaksi Selenium sebagai potensi "Data Breach" saat login, memunculkan popup hitam yang mengganggu test.

Decision: Mengimplementasikan mode Incognito dan menonaktifkan fitur keamanan spesifik (PasswordLeakDetection) melalui ChromeOptions di conftest.py untuk memastikan kestabilan test.

📝 3. Assumptions 

Network Stability: Diasumsikan koneksi internet stabil. Namun, framework sudah dilengkapi dengan Explicit Waits untuk menangani network latency yang wajar.

Environment: Website Demoblaze dianggap sebagai environment "Staging". Data yang dibuat (User baru) dianggap data sampah (dummy) yang aman untuk dibuat terus-menerus.

Browser: Pengujian difokuskan pada Google Chrome (sesuai standar pasar terbesar), namun struktur kode memungkinkan ekstensi mudah ke Firefox/Edge.


🌟 Fitur Utama

Page Object Model: Struktur kode rapi dan modular.
Robustness: Menangani flaky tests dengan Explicit Waits dan Retry Logic.
Dynamic Data: Generator username unik untuk menghindari konflik data.
Auto-Reporting:
Generate HTML Report.
Screenshot otomatis saat test gagal.
Otomatis membuka report di browser setelah selesai.
Smart Cleanup: Membersihkan folder screenshot lama sebelum test berjalan.
Incognito Mode: Menjalankan test di mode aman tanpa cache/history.

⚙️ Instalasi

1. Clone Repository
- git clone https://github.com/andhikasp/demoblazeseleniumpython.git
- cd demoblazeseleniumpython

2. Buat Virtual Environment

# Windows:
- python -m venv venv
- .\venv\Scripts\activate
Troubleshooting Windows:
Jika muncul error "running scripts is disabled", jalankan perintah berikut di PowerShell (Run as Administrator), lalu coba aktivasi lagi:
- Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
Setelah berhasil, jalankan aktivasi kembali:
- .\venv\Scripts\Activate.ps1


# Mac/Linux:
python3 -m venv venv
source venv/bin/activate


3. Install Dependencies

pip install -r requirements.txt



🚀 Cara Menjalankan Test

1. Menjalankan Semua Test (Urut)

Gunakan perintah ini untuk menjalankan semua test case, menghasilkan report, dan membukanya otomatis.

- pytest -v --html=reports/report.html 


2. Menjalankan Test Tertentu

Gunakan -k diikuti kata kunci nama test.

- pytest -k "test_sign_in_registered_user" 


3. Headless Mode (Tanpa UI Browser)

Cocok untuk dijalankan di CI/CD (Jenkins/GitLab).

pytest --headless --html=reports/report.html 





