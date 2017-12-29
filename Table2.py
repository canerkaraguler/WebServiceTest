import mysql.connector as conn
import json


db = conn.connect(host="54.202.76.117", user="cnrkrglr", password="caner2000")
cursor = db.cursor()


class Table2:
    def __init__(self):
        pass

    # data transfer objeleri yaratilacak

    def CreateDatabaseRelatedToJson(self, database_name, table_name, request_data):

        cursor.execute("""CREATE DATABASE IF NOT EXISTS """ + database_name)
        db.commit()

        cursor.execute("""USE """ + database_name)
        db.commit()

        lst = list()
        itemList = list(request_data.items())
        print(str(len(itemList)))
        for listCount in range(len(itemList)):
            lst.append(itemList[listCount][0])

        createsqltable = """CREATE TABLE IF NOT EXISTS """ + table_name + " ( record_id int NOT NULL AUTO_INCREMENT," + " VARCHAR(250),".join(
            lst) + " VARCHAR(250), PRIMARY KEY (record_id))"
        print(createsqltable)
        cursor.execute(createsqltable)
        db.commit()

    def AddItemToDatabase(self, database_name, table_name, request_data):

        cursor.execute("""USE """ + database_name)
        db.commit()

        lstValue = list()
        lstKey = list()
        itemList = list(request_data.items())

        for listCount in range(len(itemList)):
            lstValue.append("'" + str(itemList[listCount][1]))
            lstKey.append(str(itemList[listCount][0]))

        queryString = """INSERT INTO """ + table_name + " (" + ",".join(lstKey) + ")"" VALUES (" + "',".join(
            lstValue) + "'" + ")"
        print(queryString)
        cursor.execute(queryString)
        db.commit()

    def GetPassword(self, username):

        cursor.execute("""USE userDB""")
        db.commit()
        cursor.execute("SELECT password FROM userTable WHERE username=" + "\'" + username + "\'")
        row = cursor.fetchone()
        db.commit()
        return row

    def CheckUserExistance(self, username):

        cursor.execute("""USE userDB""")
        db.commit()
        cursor.execute("SELECT username FROM userTable WHERE username=" + "\'" + username + "\'")
        row = cursor.fetchone()
        db.commit()
        return row

    def Login(self, username, password):

        cursor.execute("""USE userDB""")
        db.commit()
        cursor.execute("SELECT username FROM userTable WHERE username=" + "\'" + username + "\'")
        row = cursor.fetchone()
        db.commit()
        if row is not None:
            passwordObtainedFromDB = self.GetPassword(username)[0]

            if passwordObtainedFromDB == password:
                return True
            else:
                return False
        else:
            return False

    def CheckAdminExistance(self, username):

        cursor.execute("""USE userDB""")
        db.commit()
        cursor.execute(
            "SELECT username FROM userTable WHERE username=" + "\'" + username + "\'" + "AND admin=" + "\'1\'")
        row = cursor.fetchone()
        db.commit()

        return row

    def CreateNewUser(self, user):
        print("creating user")
        cursor.execute("""USE userDB""")
        db.commit()

        queryString = """INSERT INTO userTable (username,password,userId,admin) VALUES (""" + "\'" + user.username + "\'" + "," + "\'" + user.password + "\'" + "," + "\'" + str(
            user.userId) + "\'" + "," + "\'" + str(user.admin) + "\'" + ")"

        cursor.execute(queryString)
        db.commit()

    def GetAllInfo(self, database_name, table_name):

        cursor.execute("""USE """ + database_name)
        db.commit()
        queryString = """SELECT * FROM """ + table_name
        cursor.execute(queryString)
        response = cursor.fetchall()
        db.commit()

        queryString2 = """SELECT column_name FROM information_schema.columns WHERE table_name=\'""" + table_name + "\'"
        cursor.execute(queryString2)
        responseColumns = cursor.fetchall()
        db.commit()

        index2 = 0
        datatmp = {}

        data = {}
        for item in response:
            index = 0
            for column in responseColumns:
                datatmp[str(column[0])] = str(item[index])

                index = index + 1

            data[str(index2)] = str(json.loads(json.dumps(datatmp)))

            index2 = index2 + 1

        return json.loads(json.dumps(data))


