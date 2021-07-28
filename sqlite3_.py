import sqlite3

# sqlite3是一个微型的数据库，主要用于浏览器，手机/平板n， 智能设备的应用
# 支持标准的sql语句，不过没有特定的数据类型，
# 可以根据开发语法的特性或类型，来限定字段的类型
conn = sqlite3.connect('users.sqlite3')  # 自动创建文件

cursor = conn.cursor()
cursor.execute('''
    CREATE TABLE user(id Integer PARAMETER KEY ,name, age, phone)
''')

cursor.execute('''
INSERT INTO user (name, age, phone)
values('disen', 20, '13267886101')
''')

cursor.execute('''
INSERT INTO user(id,name,age,phone)
values ('jack', 18, '15559887456')
''')

cursor.execute('SELECT * from user')
for row in cursor.fetchall():
    print(row)

conn.commit()  # 提交事务
