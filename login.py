import sqlite3
import time
from passlib.hash import bcrypt
import hashlib


def login():
    while True:
        username = input("Please input your email")
        password = input("Please input your password")
        with sqlite3.connect("rmp.db") as db:
            cursor = db.cursor()
        find_user = ("SELECT * FROM users WHERE email = ? AND passwd = ?")
        cursor.execute(find_user, [(username), (password)])
        results = cursor.fetchall()

        if results:
            for i in results:
                print("Welcome " + i[2])
            break
        else:
            print("Email or password not recognized")
            again = input("Do you want to try again y/n: ")
            if again.lower() == "n":
                print("Goodbye")
                time.sleep(1)
                break


login()
