import streamlit as st
from db import *
import pandas as pd

st.set_page_config(page_title="Hospital Management System", layout="wide")
st.title("🏥 Hospital Management System")

menu = [
    "Home",
    "Add Patient", "View Patients", "Delete Patient",
    "Add Doctor", "View Doctors", "Delete Doctor",
    "Add Appointment", "View Appointments", "Delete Appointment"
]
choice = st.sidebar.selectbox("Navigation", menu)

# -------------------- HOME --------------------
if choice == "Home":
    st.subheader("Welcome to Hospital Management System")
    st.markdown("Use the sidebar to navigate different features.")

# -------------------- ADD PATIENT --------------------
elif choice == "Add Patient":
    st.subheader("Add New Patient")
    name = st.text_input("Name")
    age = st.number_input("Age", min_value=0)
    gender = st.selectbox("Gender", ["Male", "Female", "Other"])
    diagnosis = st.text_input("Diagnosis")
    admitted_on = st.date_input("Admitted On")

    if st.button("Add Patient"):
        add_patient(name, age, gender, diagnosis, admitted_on)
        st.success("✅ Patient added successfully!")

# -------------------- VIEW PATIENTS --------------------
elif choice == "View Patients":
    st.subheader("All Patients")
    patients = view_patients()
    df = pd.DataFrame(patients, columns=["ID", "Name", "Age", "Gender", "Diagnosis", "Admitted On"])
    st.dataframe(df)

# -------------------- DELETE PATIENT --------------------
elif choice == "Delete Patient":
    st.subheader("Delete Patient Record")
    patients = view_patients()
    if not patients:
        st.warning("No patients found.")
    else:
        patient_map = {f"{p[0]} - {p[1]}": p[0] for p in patients}
        selected_patient = st.selectbox("Select Patient to Delete", list(patient_map.keys()))
        if st.button("Delete Patient"):
            delete_patient(patient_map[selected_patient])
            st.success("🗑️ Patient deleted successfully!")

# -------------------- ADD DOCTOR --------------------
elif choice == "Add Doctor":
    st.subheader("Add New Doctor")
    name = st.text_input("Doctor Name")
    specialty = st.text_input("Specialty")
    phone = st.text_input("Phone Number")
    if st.button("Add Doctor"):
        add_doctor(name, specialty, phone)
        st.success("✅ Doctor added successfully!")

# -------------------- VIEW DOCTORS --------------------
elif choice == "View Doctors":
    st.subheader("All Doctors")
    doctors = view_doctors()
    df = pd.DataFrame(doctors, columns=["ID", "Name", "Specialty", "Phone"])
    st.dataframe(df)

# -------------------- DELETE DOCTOR --------------------
elif choice == "Delete Doctor":
    st.subheader("Delete Doctor Record")
    doctors = view_doctors()
    if not doctors:
        st.warning("No doctors found.")
    else:
        doctor_map = {f"{d[0]} - {d[1]}": d[0] for d in doctors}
        selected_doctor = st.selectbox("Select Doctor to Delete", list(doctor_map.keys()))
        if st.button("Delete Doctor"):
            delete_doctor(doctor_map[selected_doctor])
            st.success("🗑️ Doctor deleted successfully!")

# -------------------- ADD APPOINTMENT --------------------
elif choice == "Add Appointment":
    st.subheader("Book an Appointment")
    patients = view_patients()
    doctors = view_doctors()

    if not patients or not doctors:
        st.warning("You must have at least one patient and doctor added first.")
    else:
        patient_map = {f"{p[0]} - {p[1]}": p[0] for p in patients}
        doctor_map = {f"{d[0]} - {d[1]}": d[0] for d in doctors}

        selected_patient = st.selectbox("Select Patient", list(patient_map.keys()))
        selected_doctor = st.selectbox("Select Doctor", list(doctor_map.keys()))
        appointment_date = st.date_input("Appointment Date")
        reason = st.text_area("Reason")

        if st.button("Add Appointment"):
            appointments(patient_map[selected_patient], doctor_map[selected_doctor], appointment_date, reason)
            st.success("✅ Appointment booked successfully!")

# -------------------- VIEW APPOINTMENTS --------------------
elif choice == "View Appointments":
    st.subheader("All Appointments")
    df = view_appointments()
    st.dataframe(df)

# -------------------- DELETE APPOINTMENT --------------------
elif choice == "Delete Appointment":
    st.subheader("Delete Appointment Record")
    df = view_appointments()
    if df.empty:
        st.warning("No appointments found.")
    else:
        appointment_map = {f"{row.Appointment_ID} - {row.Patient_Name} with {row.Doctor_Name}": row.Appointment_ID for _, row in df.iterrows()}
        selected_appointment = st.selectbox("Select Appointment to Delete", list(appointment_map.keys()))
        if st.button("Delete Appointment"):
            delete_appointment(appointment_map[selected_appointment])
            st.success("🗑️ Appointment deleted successfully!")
