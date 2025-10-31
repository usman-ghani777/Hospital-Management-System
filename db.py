import pymysql
from config import *
import pandas as pd

# -------------------- DATABASE CONNECTION --------------------
def connect():
    return pymysql.connect(
        host=MYSQL_HOST,
        user=MYSQ_USER,
        password=MYSQL_PASSWORD,
        database=MYSQL_DATABASE
    )

# -------------------- PATIENTS --------------------
def add_patient(name, age, gender, diagnosis, admitted_on):
    mydb = connect()
    cur = mydb.cursor()
    sql = 'INSERT INTO patients (name, age, gender, diagnosis, admitted_on) VALUES (%s,%s,%s,%s,%s)'
    cur.execute(sql, (name, age, gender, diagnosis, admitted_on))
    mydb.commit()
    mydb.close()

def view_patients():
    mydb = connect()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM patients")
    data = cur.fetchall()
    mydb.close()
    return data

def delete_patient(patient_id):
    mydb = connect()
    cur = mydb.cursor()
    # First delete all appointments linked to this patient
    cur.execute("DELETE FROM appointments WHERE patient_id = %s", (patient_id,))
    cur.execute("DELETE FROM patients WHERE id = %s", (patient_id,))
    mydb.commit()
    mydb.close()

# -------------------- DOCTORS --------------------
def add_doctor(name, specialty, phone):
    mydb = connect()
    cur = mydb.cursor()
    sql = 'INSERT INTO doctors (name, specialty, phone) VALUES (%s, %s, %s)'
    cur.execute(sql, (name, specialty, phone))
    mydb.commit()
    mydb.close()

def view_doctors():
    mydb = connect()
    cur = mydb.cursor()
    cur.execute("SELECT * FROM doctors")
    data = cur.fetchall()
    mydb.close()
    return data

def delete_doctor(doctor_id):
    mydb = connect()
    cur = mydb.cursor()
    # First delete all appointments linked to this doctor
    cur.execute("DELETE FROM appointments WHERE doctor_id = %s", (doctor_id,))
    cur.execute("DELETE FROM doctors WHERE id = %s", (doctor_id,))
    mydb.commit()
    mydb.close()

# -------------------- APPOINTMENTS --------------------
def appointments(patient_id, doctor_id, appointment_date, reason):
    mydb = connect()
    cur = mydb.cursor()
    sql = 'INSERT INTO appointments (patient_id, doctor_id, appointment_date, reason) VALUES (%s,%s,%s,%s)'
    cur.execute(sql, (patient_id, doctor_id, appointment_date, reason))
    mydb.commit()
    mydb.close()

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

def delete_appointment(appointment_id):
    mydb = connect()
    cur = mydb.cursor()
    cur.execute("DELETE FROM appointments WHERE id = %s", (appointment_id,))
    mydb.commit()
    mydb.close()
