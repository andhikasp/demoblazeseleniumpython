# 🚀 Demoblaze Automation Framework

> Submission for QA Engineer Technical Assignment - Part 3 (Automation Project)

[![Python](https://img.shields.io/badge/Python-3.x-blue.svg)](https://www.python.org/)
[![Selenium](https://img.shields.io/badge/Selenium-4.16.0-green.svg)](https://www.selenium.dev/)
[![Pytest](https://img.shields.io/badge/Pytest-7.4.3-orange.svg)](https://docs.pytest.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Repository ini berisi solusi automation testing untuk platform E-Commerce. Project ini dibangun menggunakan **Python** dan **Selenium WebDriver** dengan pendekatan **Page Object Model (POM)** untuk memastikan kode yang bersih, modular, dan mudah dipelihara.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Project Structure](#-project-structure)
- [Prerequisites](#-prerequisites)
- [Installation](#-installation)
- [Usage](#-usage)
- [Test Cases](#-test-cases)
- [Challenges & Decisions](#-challenges--decisions)
- [Assumptions](#-assumptions)
- [Contributing](#-contributing)
- [License](#-license)

---

## 📋 Overview

Solusi ini dirancang untuk mengotomatisasi **Critical User Journey** pada aplikasi E-Commerce. Arsitektur framework dipilih untuk memenuhi standar industri modern dengan fokus pada **scalability** dan **reliability**.

### Key Highlights

- ✅ **Page Object Model (POM)** - Memisahkan logic test dari elemen UI
- ✅ **Dynamic Data Generation** - Random generator untuk User Registration (Idempotent)
- ✅ **Auto-Reporting** - HTML Report dengan screenshot otomatis pada test yang gagal
- ✅ **Robust Error Handling** - Explicit Waits dan Retry Logic untuk menangani flaky tests
- ✅ **CI/CD Ready** - Support untuk headless mode

---

## 🌟 Features

| Feature | Description |
|---------|-------------|
| **Page Object Model** | Struktur kode rapi dan modular untuk maintainability |
| **Robustness** | Menangani flaky tests dengan Explicit Waits dan Retry Logic |
| **Dynamic Data** | Generator username unik untuk menghindari konflik data |
| **Auto-Reporting** | Generate HTML Report dengan screenshot otomatis |
| **Smart Cleanup** | Membersihkan folder screenshot lama sebelum test berjalan |
| **Incognito Mode** | Menjalankan test di mode aman tanpa cache/history |
| **Headless Support** | Dapat dijalankan tanpa UI browser untuk CI/CD |

---

## 🛠 Tech Stack

- **Language**: Python 3.x
- **Testing Framework**: Pytest 7.4.3
- **Web Automation**: Selenium 4.16.0
- **Driver Management**: WebDriver Manager 4.0.1
- **Reporting**: Pytest HTML 4.1.1
- **Test Ordering**: Pytest Ordering 0.6

---

## 📁 Project Structure

```
demoblazeseleniumpython/
│
├── helpers/                 # Helper utilities
│   ├── __init__.py
│   └── helpers.py          # Driver setup, screenshots, report management
│
├── pages/                   # Page Object Model classes
│   ├── __init__.py
│   ├── base_page.py        # Base class for all pages
│   ├── dashboard_page.py   # Dashboard page actions
│   ├── product_page.py     # Product page actions
│   └── cart_page.py        # Cart page actions
│
├── tests/                   # Test cases
│   ├── __init__.py
│   ├── test_01_sign_up.py  # User registration tests
│   ├── test_02_login.py    # User login tests
│   └── test_03_add_to_cart.py  # Shopping cart tests
│
├── data/                    # Test data
│   ├── __init__.py
│   └── test_data.py        # Test data generators
│
├── screenshots/             # Screenshots on test failures
├── reports/                 # HTML test reports
│
├── conftest.py             # Pytest configuration & fixtures
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 📋 Prerequisites

Sebelum memulai, pastikan Anda telah menginstall:

- **Python 3.7+** ([Download Python](https://www.python.org/downloads/))
- **Google Chrome Browser** (untuk WebDriver)
- **Git** (untuk clone repository)

---

## ⚙️ Installation

### 1. Clone Repository

```bash
git clone https://github.com/andhikasp/demoblazeseleniumpython.git
cd demoblazeseleniumpython
```

### 2. Create Virtual Environment

**Windows:**
```powershell
python -m venv venv
.\venv\Scripts\activate
```

> **Troubleshooting Windows:**  
> Jika muncul error "running scripts is disabled", jalankan perintah berikut di PowerShell (Run as Administrator):
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```
> Setelah berhasil, jalankan aktivasi kembali:
> ```powershell
> .\venv\Scripts\Activate.ps1
> ```

**Mac/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🚀 Usage

### Menjalankan Semua Test

Menjalankan semua test case dengan urutan yang sudah ditentukan, menghasilkan HTML report, dan membukanya otomatis di browser:

```bash
pytest -v --html=reports/report.html
```

### Menjalankan Test Tertentu

Gunakan flag `-k` diikuti dengan kata kunci nama test:

```bash
pytest -k "test_sign_in_registered_user" -v
```

### Headless Mode

Menjalankan test tanpa membuka UI browser (cocok untuk CI/CD seperti Jenkins/GitLab):

```bash
pytest --headless --html=reports/report.html -v
```

### Menjalankan Test dengan Custom URL

```bash
pytest --url="https://www.demoblaze.com/" --html=reports/report.html -v
```

### Menjalankan Test Tertentu dengan Urutan

Test sudah dikonfigurasi dengan `pytest-ordering` untuk memastikan urutan eksekusi:

```bash
pytest tests/test_01_sign_up.py tests/test_02_login.py tests/test_03_add_to_cart.py -v
```

---

## 🧪 Test Cases

| Test File | Description | Test Cases |
|-----------|-------------|------------|
| `test_01_sign_up.py` | User Registration | - Sign up dengan user baru<br>- Validasi form registration |
| `test_02_login.py` | User Authentication | - Login dengan user terdaftar<br>- Validasi login berhasil |
| `test_03_add_to_cart.py` | Shopping Cart | - Menambahkan produk ke cart<br>- Validasi cart items |

---

## ⚠️ Challenges & Decisions

Berdasarkan analisis terhadap instruksi soal dan environment yang tersedia, berikut adalah keputusan strategis yang diambil:

### A. Perubahan Target Aplikasi

**Challenge:**  
Instruksi soal meminta otomatisasi untuk "User Registration Flow". Namun, environment yang disediakan (saucedemo.com) adalah website demo statis yang tidak memiliki fitur pendaftaran user.

**Decision:**  
Menggunakan **Demoblaze.com** sebagai System Under Test pengganti. Platform ini memiliki fitur E-Commerce lengkap (Sign Up, Login, Cart, Purchase), sehingga memungkinkan untuk mendemonstrasikan kemampuan scripting registrasi sesuai persyaratan soal.

### B. Lingkup API Testing

**Challenge:**  
Instruksi soal menyediakan environment API (jsonplaceholder), namun pada Bagian 3 (Automation) tidak ada instruksi eksplisit untuk membuat script API, hanya fokus pada UI Flow (Register, Login, Cart).

**Decision:**  
Fokus repository ini adalah **UI/Web Automation**. Strategi pengujian API telah dijelaskan secara konseptual pada dokumen Test Strategy (Bagian 1) sebagai layer pengujian backend, namun tidak diimplementasikan dalam kode repository ini agar tetap sesuai dengan scope waktu pengerjaan (3 hari).

### C. Isu Keamanan Browser

**Challenge:**  
Chrome modern mendeteksi interaksi Selenium sebagai potensi "Data Breach" saat login, memunculkan popup hitam yang mengganggu test.

**Decision:**  
Mengimplementasikan mode **Incognito** dan menonaktifkan fitur keamanan spesifik (`PasswordLeakDetection`) melalui ChromeOptions di `conftest.py` untuk memastikan kestabilan test.

---

## 📝 Assumptions

- **Network Stability**: Diasumsikan koneksi internet stabil. Namun, framework sudah dilengkapi dengan Explicit Waits untuk menangani network latency yang wajar.

- **Environment**: Website Demoblaze dianggap sebagai environment "Staging". Data yang dibuat (User baru) dianggap data sampah (dummy) yang aman untuk dibuat terus-menerus.

- **Browser**: Pengujian difokuskan pada **Google Chrome** (sesuai standar pasar terbesar), namun struktur kode memungkinkan ekstensi mudah ke Firefox/Edge.

---

## 🤝 Contributing

Contributions, issues, and feature requests are welcome! Feel free to check the [issues page](https://github.com/andhikasp/demoblazeseleniumpython/issues).

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👤 Author

**Andhika Surya Pradana**

- GitHub: [@andhikasp](https://github.com/andhikasp)
- Repository: [demoblazeseleniumpython](https://github.com/andhikasp/demoblazeseleniumpython)

---

## 🙏 Acknowledgments

- [Selenium](https://www.selenium.dev/) - Web automation framework
- [Pytest](https://docs.pytest.org/) - Testing framework
- [Demoblaze](https://www.demoblaze.com/) - Test application
- [WebDriver Manager](https://github.com/SergeyPirogov/webdriver_manager) - Driver management

---

<div align="center">
  <sub>Built with ❤️ for QA Automation</sub>
</div>
