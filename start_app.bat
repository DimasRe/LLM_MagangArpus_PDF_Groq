@echo off
echo Memulai Chatbot Dinas Arpus Jateng...
echo.

REM Pastikan MySQL berjalan dengan baik
echo Memeriksa koneksi MySQL...
python -c "from db_utils import check_mysql_connection; print('MySQL OK' if check_mysql_connection() else 'MySQL Error')"

REM Jika ada masalah dengan MySQL, coba bersihkan koneksi
echo Membersihkan koneksi MySQL yang menggantung...
python -c "from db_utils import cleanup_mysql_connections; cleanup_mysql_connections()"

echo.
echo Memulai aplikasi...
python app.py

echo.
echo Aplikasi berhenti. Membersihkan koneksi...
python -c "from db_utils import cleanup_mysql_connections; cleanup_mysql_connections()"

echo.
echo Selesai!
pause