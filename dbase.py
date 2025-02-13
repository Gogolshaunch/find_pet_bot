import sqlite3

DATABASE_NAME = 'mydatabase.db'

conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS owner (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        name TEXT,
        phonenumber TEXT,
        tg_user TEXT,
        city TEXT,
        type_pet TEXT,
        name_pet TEXT,
        sex_pet INTEGER,
        breed_pet TEXT,
        describe TEXT,
        photo TEXT)""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS finder (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        name TEXT,
        phonenumber TEXT,
        tg_user TEXT,
        city TEXT,
        type_pet TEXT,
        name_pet TEXT,
        sex_pet INTEGER,
        breed_pet TEXT,
        describe TEXT,
        photo TEXT)""")
conn.commit()

def new_human(person, chat_id):
    table_name = 'finder' if person.status == 1 else 'owner'
    cursor.execute(f"""
        INSERT INTO {table_name} (chat_id, name, phonenumber, tg_user, city, type_pet, name_pet, sex_pet, breed_pet, describe, photo)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (chat_id, person.name, person.phone_number, person.tg_user, person.city, person.type_pet, person.name_pet, person.sex_pet, person.breed_pet, person.describe, person.photo))
    conn.commit()

def choice_human(table_name, person_city, type_pet):
    cursor.execute(f"""
        SELECT * FROM {table_name} WHERE city = ? OR type_pet = ?
    """, (person_city, type_pet))
    result = cursor.fetchall()
    return result

def choice_human_owner(person_city, type_pet):
    return choice_human('owner', person_city, type_pet)

def choice_human_finder(person_city, type_pet):
    return choice_human('finder', person_city, type_pet)

def count_person(status):
    table_name = 'finder' if status == 1 else 'owner'
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    result = cursor.fetchone()[0]
    return result

def del_person(person, chat):
    table_name = 'finder' if person.status == 1 else 'owner'
    cursor.execute(f"DELETE FROM {table_name} WHERE chat_id = ?", (chat,))
    conn.commit()
