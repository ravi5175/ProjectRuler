# -*- coding: utf-8 -*-
"""
Created on Sat Nov 30 15:50:07 2019

@author: Kapil Bansal
"""

import sqlite3
conn=sqlite3.connect('MainDatabase.sqlite')
#DROP TABLE Recruiters
#Checking if tables exist or not
def table_maker():
    cur=conn.cursor()
    cur.executescript('''
    
    CREATE TABLE IF NOT EXISTS Users (
        User_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Name TEXT NOT NULL,
        Phone INTEGER(10) UNIQUE NOT NULL,
        Email TEXT,
        Address TEXT(50),
        Marks_10 DECIMAL(2,2) NOT NULL,
        Marks_12 DECIMAL(2,2),
        DOB TEXT NOT NULL,
        Gender TEXT NOT NULL,
        Category TEXT,
        Password TEXT
    );
    CREATE TABLE IF NOT EXISTS Recruiters (
        Recruiter_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        SPOC_phone INTEGER(10) NOT NULL,
        Company_Name TEXT NOT NULL UNIQUE,
        Company_mail TEXT NOT NULL UNIQUE,
        Company_Address TEXT NOT NULL,
        Password TEXT
    );
    CREATE TABLE IF NOT EXISTS Jobs (
        Job_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        Job_name TEXT NOT_NULL,
        Skill_required TEXT NOT NULL,
        Job_Description TEXT,
        Expected_salary TEXT,
        State_Name TEXT NOT NULL,
        Location TEXT NOT NULL,
        Company_Name TEXT NOT NULL,
        link TEXT NOT NULL,
        Recruiter_id INTEGER,
        sector TEXT,
        last_date TEXT,
        applied INTEGER,
        FOREIGN KEY (Recruiter_id)
        REFERENCES Recruiters (Recruiter_id)
    );
    CREATE TABLE IF NOT EXISTS Applications (
        Application_id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        User_id INTEGER,
        Recruiter_id INTEGER,
        Job_id INTEGER,
        ratings DECIMAL,
        status INTEGER,
        FOREIGN KEY (User_id)
        REFERENCES Users (User_id),
        FOREIGN KEY (Recruiter_id)
        REFERENCES Recruiters (Recruiter_id),
        FOREIGN KEY (Job_id)
        REFERENCES Jobs (Job_id)
    );
    ''')
    conn.commit()
    conn.close()
def make_user(name,phone,mail,address,marks_10,marks_12,gender,dob,password,category):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''
                    INSERT OR IGNORE INTO Users(Name,Phone,Email,Address,Marks_10,Marks_12,Gender,DOB,Password,Category)
                    VALUES(?,?,?,?,?,?,?,?,?,?)''',(name,phone,mail,address,marks_10,marks_12,gender,dob,password,category))
        conn.commit()
def make_recruiter(name,phone,mail,address,password):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''
                    INSERT OR IGNORE INTO Recruiters(Company_name,SPOC_phone,Company_mail,Company_Address,Password)
                    VALUES(?,?,?,?,?)''',(name,phone,mail,address,password))
        conn.commit()
def user_check(name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Name,Password FROM Users WHERE Name=?''',(name,))
        row=cur.fetchone()
        return row

def spoc_check(name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Company_Name,Password FROM Recruiters WHERE Company_Name=?''',(name,))
        row=cur.fetchone()
        return row

def user_info(name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT User_id,Name,Phone,Email,Address,Marks_10,Marks_12,DOB,Gender,Category FROM Users WHERE Name=?''',(name,))
        row=cur.fetchone()
        return row

def spoc_info(name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Recruiter_id,Company_Name,SPOC_phone,Company_mail,Company_Address FROM Recruiters WHERE Company_Name=?''',(name,))
        row=cur.fetchone()
        return row

def add_job(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Recruiter_id FROM Recruiters WHERE Company_Name=?''',(Company_Name,))
        Recruiter_id=cur.fetchone()[0]
        link='NULL'
        cur.execute('''INSERT INTO Jobs(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,Recruiter_id,link) VALUES(?,?,?,?,?,?,?,?,?)''',(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,Recruiter_id,link))
        conn.commit()            
        return 1
def add_scrap_job(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,link,last_date):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''INSERT INTO Jobs(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,link,last_date) VALUES(?,?,?,?,?,?,?,?,?)''',(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,link,last_date))
        conn.commit()            
        return 1
def fetch_job_name(Company_Name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Recruiter_id FROM Recruiters WHERE Company_Name=?''',(Company_Name,))
        Recruiter_id=cur.fetchone()[0]
        cur.execute('''SELECT Job_name FROM Jobs WHERE Recruiter_id=?''',(Recruiter_id,))
        row=cur.fetchall()
        return row
def fetch_job(Job_name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name FROM Jobs WHERE Job_name=?''',(Job_name,))
        row=cur.fetchall()
        return row
def check_job_availability(Post,Company_Name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_name,Skill_required,Company_Name FROM Jobs Where Job_name=? AND Company_Name=?''',(Post,Company_Name))
        row=cur.fetchone()
        if row!=None:
            return 1
        else:
            return 0
def fetch_scrap():
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_name,State_Name,link FROM Jobs WHERE link!='NULL' ''')
        row=cur.fetchall()
        return row

def update_job(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_id FROM Jobs WHERE Job_name=? AND Company_Name=?''',(Job_name,Company_Name,))
        Job_id=cur.fetchone()[0]
        cur.execute('''UPDATE Jobs SET Job_name=?,Skill_required=?,Job_Description=?,Expected_salary=?,state_Name=?,Location=?,Company_Name=? WHERE Job_id=?''',(Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name,Job_id))
        conn.commit()     
def free_jobs():
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT * FROM Jobs WHERE Recruiter_id IS NOT NULL''')
        row=cur.fetchall()
        return row
    
def job_apply(User_id,Job_id):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Recruiter_id FROM Jobs WHERE Job_Id=?''',(Job_id,))
        Recruiter_id=cur.fetchone()[0]
        cur.execute('''INSERT INTO Applications(User_id,Recruiter_id,Job_id) VALUES(?,?,?)''',(User_id,Recruiter_id,Job_id))
        conn.commit
        return Recruiter_id
def fetch_job_id(Job_name):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_name,Skill_required,Job_Description,Expected_salary,state_Name,Location,Company_Name FROM Jobs WHERE Job_id=?''',(Job_name,))
        row=cur.fetchall()
        return row[0]
def fetch_recommend(State_Name,sector):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_name,Skill_required,Job_Description,Expected_salary,State_Name,Location,Company_Name,sector,last_date,minimum_qualification FROM Jobs WHERE State_Name=? AND sector=?''',(State_Name,sector))
        row=cur.fetchall()
        return row
def recruiter_job(id):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT User_id,Recruiter_id from Applications WHERE Job_id=?''',(id,))
        rows=cur.fetchall()
        if len(rows)!=0:
            for row in range(len(rows)):
                user_id=rows[row][0]
                cur.execute('''SELECT Name,Phone,Email,Address,Marks_10,Marks_12,DOB,Gender,Category FROM Users WHERE User_id=?''',(user_id,))
                rows[row]=rows[row]+cur.fetchone()
        return rows
def user_job(id):
    with sqlite3.connect("MainDatabase.sqlite") as conn:
        cur=conn.cursor()
        cur.execute('''SELECT Job_id,Recruiter_id from Applications WHERE User_id=?''',(id,))
        rows=cur.fetchall()
        if len(rows)!=0:
            for row in range(len(rows)):
                job_id=rows[row][0]
                cur.execute('''SELECT Job_name,Skill_required,Job_Description,Expected_salary,State_Name,Location,Company_Name,sector,last_date,minimum_qualification FROM Jobs WHERE Job_id=?''',(job_id,))
                rows[row]=rows[row]+cur.fetchone()
            return rows
        else:
            return None
table_maker()