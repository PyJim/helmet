from helper import db_execute, db_query
import sqlite3
from flask import render_template, redirect
from datetime import datetime

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
    query = f"""SELECT * FROM REPORT WHERE Author = ?;"""
    result = db_query(query, [username])
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

def edit_report(username, title, location, description, image, video, report_id):
    connection = sqlite3.connect('database.db')
    query = """UPDATE REPORT SET Title=?, Loc=?, Des=?, Img=?, Vid=?, Author=? WHERE id = ?;"""
    connection.execute(query, [title, location, description, image, video, username, report_id])
    connection.commit()
    connection.close()


def editEvent(title, date_time, desc, org, loc, image, username, event_id):
    date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    month = date_time.strftime("%b")
    date_string = f'{date_time.strftime("%d %B, %Y")} {date_time.strftime("%I:%M %p")}'

    connection = sqlite3.connect('database.db')
    query = """UPDATE EVENTS SET Title=?, Datetime=?, Desc=?, Organizer=?, Loc=?, Img=?, Month=?, Date=?, Author=? WHERE id=?;"""
    connection.execute(query, [title, date_time, desc, org, loc, image, month, date_string, username, event_id])
    connection.commit()
    connection.close()

def searchEvents(phrase, datetime):
    query = """SELECT * FROM EVENTS WHERE Title LIKE ? AND Datetime >= ?"""
    result = db_query(query, [phrase, datetime])
    return result

def getUserEvents(user, datetime):
    query = """SELECT * FROM EVENTS WHERE Author = ? AND Datetime >= ?"""
    result = db_query(query, [user, datetime])
    return result

def allEvents(date):
    query = """SELECT * FROM EVENTS WHERE Datetime >= ?"""
    result = db_query(query, [date])
    return result

def deleteEvent(event_id):
    connection = sqlite3.connect('database.db')
    query = """DELETE FROM EVENTS WHERE id = ?"""
    connection.execute(query, [event_id])
    connection.commit()
    connection.close()

def deletePost(post_id):
    connection = sqlite3.connect('database.db')
    query = """DELETE FROM REPORT WHERE id = ?"""
    connection.execute(query, [post_id])
    connection.commit()
    connection.close()


def searchPosts(phrase):
    query = """SELECT * FROM REPORT WHERE Title LIKE ?"""
    result = db_query(query, [phrase])
    return result

def searchUserPosts(phrase, username):
    query = """SELECT * FROM REPORT WHERE Title LIKE ? AND Author = ?"""
    result = db_query(query, [phrase, username])
    return result

def searchUserEvents(phrase, username, datetime):
    query = """SELECT * FROM EVENTS WHERE Title LIKE ? AND  Author = ? AND Datetime = ?"""
    result = db_query(query, [phrase, username, datetime])
    return result

def addEvent(title, date_time, desc, org, loc, image, username):
    date_time = datetime.strptime(date_time, '%Y-%m-%dT%H:%M')
    month = date_time.strftime("%b")
    date_string = f'{date_time.strftime("%d %B, %Y")} {date_time.strftime("%I:%M %p")}'

    connection = sqlite3.connect('database.db')
    query = """INSERT INTO EVENTS (Title, Datetime, Desc, Organizer, Loc, Img, Month, Date, Author) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);"""
    connection.execute(query, [title, date_time, desc, org, loc, image, month, date_string, username])
    connection.commit()
    connection.close()
    

def getPostById(id):
    connection = sqlite3.connect('database.db')
    query = """SELECT * FROM REPORT WHERE id = ?"""
    result = db_query(query, [id])
    return result