import psycopg2

try:
    # Твої дані з .env: пароль 567234, база application_db
    conn = psycopg2.connect(
        dbname="application_db",
        user="postgres",
        password="567234",
        host="localhost",
        port="5432"
    )
    conn.autocommit = True
    cur = conn.cursor()

    # Видаляємо таблицю, яка блокує Alembic
    cur.execute("DROP TABLE IF EXISTS alembic_version CASCADE;")
    
    print("✅ Success! Таблиця alembic_version видалена.")
    
    cur.close()
    conn.close()
except Exception as e:
    print(f"❌ Error: {e}")