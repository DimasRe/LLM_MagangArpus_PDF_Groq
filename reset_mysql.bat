@echo off
echo Membersihkan koneksi MySQL yang menggantung...
echo.

REM Pastikan path ke MySQL sesuai dengan instalasi XAMPP Anda
set MYSQL_PATH=C:\xampp\mysql\bin
set MYSQL_USER=k_arpus
set MYSQL_PASS=12345
set MYSQL_PORT=3307

echo Menghentikan layanan MySQL...
net stop MySQL

echo Menunggu 5 detik...
timeout /t 5 /nobreak > nul

echo Memulai layanan MySQL...
net start MySQL

echo Menunggu 5 detik untuk MySQL siap...
timeout /t 5 /nobreak > nul

echo Membersihkan koneksi yang menggantung...
"%MYSQL_PATH%\mysql" -u%MYSQL_USER% -p%MYSQL_PASS% -P%MYSQL_PORT% -e "SHOW PROCESSLIST; KILL [id_koneksi_yang_menggantung];"

echo.
echo Selesai! MySQL seharusnya sudah bersih dari koneksi yang menggantung.
echo Jika masih ada masalah, coba restart komputer Anda.
echo.
pause