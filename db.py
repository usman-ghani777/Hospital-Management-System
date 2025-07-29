import pymysql
from config import *

def connect():
     return  pymysql.connect(
             host = MYSQL_HOST,
             user=MYSQ_USER,
             password= MYSQL_PASSWORD,
             database=MYSQL_DATABASE 
             )

def add_patient(name, age, gender, diagnosis, admitted_on):
     mydb = connect()
     cur = mydb.cursor()
     sql = 'INSERT INTO PATIENTS (name, age, gender, diagnosis, admitted_on) VALUES (%s,%s,%s,%s,%s)'
     set_values = (name, age, gender, diagnosis, admitted_on)
     cur.execute(sql,set_values)
     mydb.commit()
     mydb.close()


def view_patients():
    mydb = connect()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    mydb.close()
    return data


def add_doctor(name, specialty, phone):
    mydb = connect()
    cur = mydb.cursor()
    sql = 'INSERT INTO doctors (name, specialty, phone) VALUES (%s, %s, %s)'
    set_values = (name, specialty, phone)
    cur.execute(sql, set_values)
    mydb.commit()
    mydb.close()



def view_doctors():
    mydb = connect()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM DOCTORS")
    data = cur.fetchall()
    mydb.close()
    return data


def appointments(patient_id,doctor_id,appointment_date,reason):
    mydb = connect()
    cur = mydb.cursor()
    sql = 'INSERT INTO APPOINTMENTS (patient_id,doctor_id,appointment_date,reason) VALUES (%s,%s,%s,%s)'
    set_values = (patient_id,doctor_id,appointment_date,reason)
    cur.execute(sql,set_values)
    mydb.commit()
    mydb.close()


import pandas as pd

def view_appointments():
    mydb = connect()
    cur = mydb.cursor()

    query = """
        SELECT 
            a.id AS Appointment_ID,
            p.name AS Patient_Name,
            d.name AS Doctor_Name,
            a.appointment_date AS Date,
            a.reason AS Reason
        FROM appointments a
        JOIN patients p ON a.patient_id = p.id
        JOIN doctors d ON a.doctor_id = d.id
        ORDER BY a.appointment_date DESC;
    """

    cur.execute(query)
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    df = pd.DataFrame(rows, columns=columns)

    mydb.close()
    return df







    
     
    


             
