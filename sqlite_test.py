import sqlite3

conn = sqlite3.connect('contacts_manager.db')
cursor = conn.cursor()

##uname = input('Enter user name to check')
##query = "SELECT * FROM users where uname={}".format(uname)
##
##cursor.execute(query)
##
##values = cursor.fetchone()
##
###print(values)
##
##

uname = input('Enter user name to insert')
print(uname,type(uname))
cursor.execute('''insert into users(uname)
                  values(:uname)''', {'uname':uname})
conn.commit()

print('now printing all users')
x = input('enter username to get userid')
query = """SELECT uid FROM users
        where uname = "bala"
        """

cursor.execute(query)
values = cursor.fetchall()


print(values)
print(type(values))
if values == []:
    print(':)')

cursor.close()
conn.close()
