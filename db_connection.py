import psycopg2
def connect_to_db():
    try:
        connection = psycopg2.connect(
            dbname="musicappdb",
            user="postgres",  # PostgreSQL kullanıcı adınız
            password="",  # PostgreSQL şifreniz
            host="localhost",  # Eğer yerelde çalışıyorsanız
            port="5432"  # PostgreSQL varsayılan portu
        )
        print("Database connection successful!")
        return connection
    except Exception as e:
        print("Error connecting to the database:", e)
        return None


