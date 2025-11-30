Demoblaze Automation Framework 🚀

Framework automation testing berbasis Python dan Selenium untuk website Demoblaze. Framework ini menggunakan design pattern Page Object Model (POM) dan dilengkapi dengan pelaporan HTML otomatis serta penanganan screenshot.


🌟 Fitur Utama

Page Object Model: Struktur kode rapi dan modular.
Robustness: Menangani flaky tests dengan Explicit Waits dan Retry Logic.
Dynamic Data: Generator username unik untuk menghindari konflik data.
Auto-Reporting:
Generate HTML Report.
Screenshot otomatis saat test gagal.
Otomatis membuka report di browser setelah selesai.
(Opsional) Mengirim report via Email.
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





