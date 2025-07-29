import streamlit as st
import pandas as pd
from db import *

st.title("Hospital Management System")

menu = ['View Patients', 'Add Patient', 'View Doctors', 'Add Doctor', 'Add Appointment','View Appointments']
choice = st.sidebar.selectbox("Menu", menu)

# ---------------------------------------
# Add Patient
# ---------------------------------------
if choice == 'Add Patient':
    st.subheader('Add New Patient')

    name = st.text_input("Patient Name")
    age = st.number_input("Age", step=1)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diagnosis = st.text_area("Diagnosis")
    admitted_on = st.date_input("Admitted On")

    if st.button("Add Patient"):
        add_patient(name, age, gender, diagnosis, admitted_on)
        st.success(f"Patient '{name}' added successfully!")

# ---------------------------------------
# View Patients
# ---------------------------------------
elif choice == 'View Patients':
    st.subheader('Patient List')
    patients = view_patients()

    if patients:
        st.table(patients)
    else:
        st.info(' No patients found.')

# ---------------------------------------
# Add Doctor
# ---------------------------------------
elif choice == 'Add Doctor':
    st.subheader('Add New Doctor')

    name = st.text_input("Doctor Name")
    specialty = st.text_input("Specialty")
    phone = st.text_input("Phone Number")

    if st.button("Add Doctor"):
        if name and specialty and phone:
            add_doctor(name, specialty, phone)
            st.success(f"Doctor '{name}' added successfully!")
        else:
            st.warning("Please fill in all fields before adding a doctor.")


# ---------------------------------------
# View Doctors
# ---------------------------------------
elif choice == 'View Doctors':
    st.subheader('Doctor Records')
    doctors = view_doctors()

    if doctors:
        st.table(doctors)
    else:
        st.info('No doctors found.')

# ---------------------------------------
# Add Appointment
# ---------------------------------------
elif choice == "Add Appointment":
    st.subheader("Schedule Appointment")

    patients = view_patients()
    doctors = view_doctors()

    if patients and doctors:
        patient_dict = {f"{p[1]} (ID: {p[0]})": p[0] for p in patients}
        doctor_dict = {f"{d[1]} (ID: {d[0]})": d[0] for d in doctors}

        selected_patient = st.selectbox("Select Patient", list(patient_dict.keys()))
        selected_doctor = st.selectbox("Select Doctor", list(doctor_dict.keys()))
        appointment_date = st.date_input("Appointment Date")
        reason = st.text_area("Reason for Appointment")

        if st.button("Book Appointment"):
            appointments(
                patient_id=patient_dict[selected_patient],
                doctor_id=doctor_dict[selected_doctor],
                appointment_date=appointment_date,
                reason=reason
            )
            st.success("Appointment booked successfully.")
    else:
        st.warning(" Please add both patients and doctors before scheduling an appointment.")


elif choice == "View Appointments":
    st.subheader(" Appointment Records")

    df = view_appointments()
    if not df.empty:
        st.dataframe(df)
    else:
        st.info(" No appointments found.")
