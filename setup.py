#!/usr/bin/env python3
"""
Database setup script for Chatbot Dinas Arpus Jateng
This script creates the necessary database tables and initial setup
"""

import os
from pathlib import Path

# --- Setup DB engine (SQLAlchemy) ---
# Note: Ini adalah bagian dari backend utama (app.py)
# Namun, jika Anda ingin menggunakan setup.py untuk inisialisasi DB (misalnya migrasi),
# Anda akan perlu mengimpor Base dan engine dari app.py atau file model terpisah.
# Untuk saat ini, kita mengasumsikan inisialisasi DB dilakukan oleh app.py itu sendiri.

def create_directories():
    """Create necessary directories."""
    print("📁 Membuat direktori...")

    directories = ['uploads']

    for dir_name in directories:
        Path(dir_name).mkdir(exist_ok=True)
        print(f"✅ Direktori berhasil dibuat: {dir_name}")

def check_env_file():
    """Check if .env file exists and has required variables."""
    print("🔧 Memeriksa konfigurasi lingkungan...")

    if not os.path.exists('.env'):
        print("⚠️  PERINGATAN: File .env tidak ditemukan!")
        print("   Harap buat file .env dengan variabel berikut:")
        print("   - GROQ_API_KEY=kunci-api-groq-anda")
        print("   - DATABASE_URL=mysql+pymysql://user:password@host:3306/database_name")
        print("   Dapatkan kunci API GROQ Anda di: https://console.groq.com/")
        return False

    # Check if required variables are present
    with open('.env', 'r') as f:
        env_content = f.read()

    # Kita hanya akan memeriksa GROQ_API_KEY di setup.py
    # DATABASE_URL akan diperiksa oleh app.py itu sendiri saat startup.
    required_vars = ['GROQ_API_KEY']
    missing_vars = []

    for var in required_vars:
        # Periksa jika variabel tidak ada atau masih placeholder
        if var not in env_content or f'{var}=kunci-api-groq-anda' in env_content or f'{var}=' in env_content:
            missing_vars.append(var)

    if missing_vars:
        print(f"⚠️  PERINGATAN: Variabel lingkungan yang hilang atau tidak terkonfigurasi: {', '.join(missing_vars)}")
        return False

    print("✅ Konfigurasi lingkungan terlihat bagus (untuk GROQ_API_KEY).")
    return True

def install_dependencies():
    """Display dependency installation instructions."""
    print("📦 Dependensi yang diperlukan (lihat requirements.txt):")
    print("   Pastikan semua terinstal dengan: pip install -r requirements.txt")

def create_requirements_file():
    """Create requirements.txt file with all necessary dependencies."""
    requirements = """fastapi==0.104.1
uvicorn[standard]==0.24.0
python-multipart==0.0.6
pydantic[email]==2.5.0
python-docx==1.1.0
PyPDF2==3.0.1
requests==2.31.0
python-dotenv==1.0.0
pymysql
sqlalchemy
"""

    with open('requirements.txt', 'w') as f:
        f.write(requirements.strip())

    print("✅ Berhasil membuat requirements.txt.")

def main():
    """Main setup function to configure the Chatbot Dinas Arpus Jateng."""
    print("🚀 Chatbot Dinas Arpus Jateng - Setup (Tanpa Login Pengguna)")
    print("=" * 50)

    create_requirements_file()
    print()

    install_dependencies()
    print()

    create_directories()
    print()

    # Catatan: Inisialisasi tabel database sekarang ditangani oleh app.py
    # melalui SQLAlchemy saat aplikasi pertama kali dijalankan.
    # Tidak perlu memanggil create_database() di sini lagi.

    env_ok = check_env_file()
    print()

    print("=" * 50)
    if env_ok:
        print("✅ Setup berhasil diselesaikan!")
        print("🚀 Anda sekarang dapat menjalankan backend dengan: uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
    else:
        print("⚠️  Setup selesai dengan peringatan.")
        print("📝 Harap konfigurasikan file .env Anda sebelum menjalankan aplikasi.")

    print("\n📖 Langkah selanjutnya:")
    print("1. Konfigurasikan file .env Anda dengan GROQ_API_KEY dan DATABASE_URL (MySQL).")
    print("   Contoh DATABASE_URL: mysql+pymysql://root:@localhost:3306/chatbot_arpus")
    print("2. Instal dependensi: pip install -r requirements.txt.")
    print("3. Jalankan backend: uvicorn app:app --host 0.0.0.0 --port 8000 --reload")
    print("4. Buka browser di perangkat ini: http://localhost:8000")
    print("   Atau buka dari perangkat lain di jaringan yang sama (jika `script.js` telah diubah): http://10.44.10.140:8000")
    print("   Untuk demo akses admin: http://10.44.10.140:8000/?is_admin_query=true")


if __name__ == "__main__":
    main()