import sqlite3

conn = sqlite3.connect('example.db')

conn.execute('''
create table if not exists records(
    id INTEGER primary key,
    name TEXT not null,
    age INTEGER not null)''')

def create_record (name, age):
    with conn:
        conn.execute("insert into records (name, age) values (?, ?)", (name, age))

def get_all_records():
    with conn:
        cursor = conn.execute("select * from records")
        return cursor.fetchall()

def get_record_by_id(rec_id):
    with conn:
        cursor = conn.execute("select * from records where id = ?", (rec_id,))
        return cursor.fetchone()

def delete_record (id):
    with conn:
        conn.execute("delete from records where id = ?", (id,))

def update_record (name, age, id):
    with conn:
        conn.execute("update records set name=?, age=? where id=?", (name, age, id))

create_record("Virat Kohli", 35)
create_record("Messi", 37)
print (get_all_records())
print (get_record_by_id(1))
print (delete_record(2))
print (delete_record(3))
print (get_all_records())
print (update_record("Papa", 70, 1))
print (get_all_records())
conn.close()
