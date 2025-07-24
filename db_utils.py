"""
Utilitas untuk mengelola koneksi database dengan lebih baik.
"""
import time
import pymysql
from sqlalchemy import create_engine, event
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.pool import QueuePool

def setup_database_engine(database_url, pool_size=10, max_overflow=20, pool_timeout=30):
    """
    Membuat dan mengkonfigurasi engine database dengan penanganan koneksi yang lebih baik.
    
    Args:
        database_url: URL koneksi database
        pool_size: Jumlah maksimum koneksi dalam pool
        max_overflow: Jumlah maksimum koneksi yang bisa dibuat melebihi pool_size
        pool_timeout: Timeout untuk mendapatkan koneksi dari pool (detik)
        
    Returns:
        SQLAlchemy engine yang sudah dikonfigurasi
    """
    engine = create_engine(
        database_url,
        poolclass=QueuePool,
        pool_size=pool_size,
        max_overflow=max_overflow,
        pool_timeout=pool_timeout,
        pool_recycle=3600,  # Recycle koneksi setiap 1 jam
        pool_pre_ping=True  # Verifikasi koneksi sebelum digunakan
    )
    
    # Event listener untuk menangani koneksi yang dibuat
    @event.listens_for(engine, "connect")
    def connect(dbapi_connection, connection_record):
        print("Database connection established")
        
    # Event listener untuk menangani koneksi yang ditutup
    @event.listens_for(engine, "close")
    def close(dbapi_connection, connection_record):
        print("Database connection closed")
    
    # Event listener untuk menangani koneksi yang gagal
    @event.listens_for(engine, "checkout")
    def checkout(dbapi_connection, connection_record, connection_proxy):
        try:
            # Verifikasi bahwa koneksi masih hidup
            cursor = dbapi_connection.cursor()
            cursor.execute("SELECT 1")
            cursor.close()
        except pymysql.err.OperationalError as e:
            # Jika koneksi mati, coba buat koneksi baru
            if e.args[0] in (2006, 2013, 2055):  # MySQL server has gone away, Lost connection, etc.
                print("Connection was invalid. Creating new connection...")
                connection_record.connection = None
                raise SQLAlchemyError("Connection was invalid")
    
    return engine

def check_mysql_connection(host='localhost', user='k_arpus', password='12345', port=3307, database='data_arpus'):
    """
    Memeriksa koneksi MySQL dan menampilkan daftar proses yang berjalan.
    Berguna untuk debugging koneksi yang menggantung.
    """
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database,
            connect_timeout=5
        )
        
        with conn.cursor() as cursor:
            cursor.execute("SHOW PROCESSLIST")
            processes = cursor.fetchall()
            
            print(f"Total koneksi aktif: {len(processes)}")
            print("Daftar proses:")
            for process in processes:
                print(f"ID: {process[0]}, User: {process[1]}, Host: {process[2]}, DB: {process[3]}, Command: {process[4]}, Time: {process[5]}, State: {process[6]}")
                
        conn.close()
        return True
    except Exception as e:
        print(f"Error saat memeriksa koneksi MySQL: {e}")
        return False

def cleanup_mysql_connections(host='localhost', user='k_arpus', password='12345', port=3307, database='data_arpus'):
    """
    Membersihkan koneksi MySQL yang menggantung (sleep lebih dari 100 detik).
    """
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            database=database,
            connect_timeout=5
        )
        
        with conn.cursor() as cursor:
            # Cari koneksi yang sleep lebih dari 100 detik
            cursor.execute("SHOW PROCESSLIST")
            processes = cursor.fetchall()
            
            killed_count = 0
            for process in processes:
                process_id = process[0]
                command = process[4]
                time_sec = process[5]
                
                # Jika koneksi dalam status Sleep dan sudah lebih dari 100 detik
                if command == "Sleep" and time_sec > 100:
                    try:
                        cursor.execute(f"KILL {process_id}")
                        killed_count += 1
                        print(f"Killed connection ID: {process_id} (Sleep for {time_sec} seconds)")
                    except Exception as e:
                        print(f"Failed to kill connection {process_id}: {e}")
            
            print(f"Total koneksi yang dibersihkan: {killed_count}")
                
        conn.close()
        return killed_count
    except Exception as e:
        print(f"Error saat membersihkan koneksi MySQL: {e}")
        return 0