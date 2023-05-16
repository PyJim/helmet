from helper import db_execute, db_query
import sqlite3
from flask import render_template, redirect


def signup_empty(name, username, email, password, confirm_password):
    first = name == ''
    user = username == ''
    email = email == ''
    pwd = password == ''
    confirm_pwd = confirm_password == ''

    return first or user or email or pwd or confirm_pwd

def signin_empty(username, password):
    username = username == ''
    pwd = password == ''

    return username or pwd


class PasswordCheck:
    def __init__(self, password1, password2):
        self.password1 = password1
        self.password2 = password2

    def mismatch(self):
        return self.password1 != self.password2

    def not_strong(self):
        return len(self.password1) < 6


class EmailCheck:
    def __init__(self, email):
        self.email = email

    def invalid(self):
        return "@" not in self.email


def check_author(username, email):
    query1 = f"""SELECT * FROM AUTHORS WHERE Username=?;"""
    query2 = f"""SELECT * FROM AUTHORS WHERE Email=?;"""

    username_check = db_query(query1, [username])
    email_check = db_query(query2, [email])
    return [username_check, email_check]


def create_author(name, username, email, password):
    query = """INSERT INTO AUTHORS (Name, Username, Email, Pwd) VALUES (?, ?, ?, ?);"""
    return db_execute(query, [name, username, email, password])

def create_author_reports(username):
    connection = sqlite3.connect('database.db')
    query = f"""CREATE TABLE IF NOT EXISTS {username}(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Title TEXT NOT NULL,
        Loc TEXT NOT NULL,
        Des TEXT NOT NULL,
        Img TEXT,
        Vid TEXT)"""
    connection.execute(query)
    connection.commit()
    connection.close()

def find_author(username):
    query = 'SELECT * FROM AUTHORS WHERE Username=?;'
    return db_query(query, [username])

def get_all_reports():
    query = f"""SELECT * FROM REPORT;"""
    result = db_query(query)
    return result

def get_author_reports(username):
    query = f"""SELECT * FROM {username};"""
    result = db_query(query)
    return result

def create_report(username, title, location, description, image, video):
    connection = sqlite3.connect('database.db')
    query = f"""INSERT INTO {username} (Title, Loc, Des, Img, Vid) VALUES (?, ?, ?, ?, ?);"""
    connection.execute(query, [title, location, description, image, video])
    connection.commit()
    connection.close()


def add_report(username, title, location, description, image, video):
    connection = sqlite3.connect('database.db')
    query = """INSERT INTO REPORT (Title, Loc, Des, Img, Vid, Author) VALUES (?, ?, ?, ?, ?, ?);"""
    connection.execute(query, [title, location, description, image, video, username])
    connection.commit()
    connection.close()
