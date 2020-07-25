import sqlite3 as sql

conn = sql.connect('banco.db')
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE emails(
    id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
    email TEXT NOT NULL);
''')
cursor.execute('''
INSERT INTO emails(email)
VALUES ('israel.santos13@fatec.sp.gov.br'),
       ('wesley.dias3@fatec.sp.gov.br'),
       ('denis.lima6@fatec.sp.gov.br'),
       ('natalia.biscaro@fatec.sp.gov.br');
''')
conn.commit()
conn.close()
