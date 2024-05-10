import sqlite3

con = sqlite3.connect("../Database/NoiseRecords.db")

cur = con.cursor()

cur.execute("insert into noise_records values (julianday('now'), ?);",[8])
con.commit();

res = cur.execute("SELECT * FROM noise_records")

print(res.fetchall())