import streamlit as st
import pandas as pd
from datetime import datetime
import os

st.set_page_config(page_title="Cloud Attendance System", layout="centered")
st.title("🌐 Online Attendance Portal")

DB_FILE = "attendance_data.csv"

# Create file if not exists
if not os.path.exists(DB_FILE):
    df = pd.DataFrame(columns=["Name", "Date", "Check-In", "Check-Out"])
    df.to_csv(DB_FILE, index=False)

st.sidebar.header("Admin Panel")

if st.sidebar.button("Clear All Records"):
    df = pd.DataFrame(columns=["Name", "Date", "Check-In", "Check-Out"])
    df.to_csv(DB_FILE, index=False)
    st.sidebar.success("All records cleared!")

tab1, tab2 = st.tabs(["Mark Attendance", "View & Download Report"])

# ---------------- CHECK IN / OUT ---------------- #
with tab1:
    st.subheader("Employee Check-In / Check-Out")

    name = st.text_input("Enter Full Name")

    col1, col2 = st.columns(2)

    if col1.button("Check In"):
        if name:
            now = datetime.now()
            df = pd.read_csv(DB_FILE)

            new_entry = {
                "Name": name,
                "Date": now.strftime("%Y-%m-%d"),
                "Check-In": now.strftime("%H:%M:%S"),
                "Check-Out": ""
            }

            df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
            df.to_csv(DB_FILE, index=False)

            st.success(f"{name} checked in successfully!")
        else:
            st.error("Please enter name")

    if col2.button("Check Out"):
        if name:
            df = pd.read_csv(DB_FILE)
            today = datetime.now().strftime("%Y-%m-%d")

            mask = (df["Name"] == name) & (df["Date"] == today) & (df["Check-Out"] == "")
            if mask.any():
                df.loc[mask, "Check-Out"] = datetime.now().strftime("%H:%M:%S")
                df.to_csv(DB_FILE, index=False)
                st.success(f"{name} checked out successfully!")
            else:
                st.warning("No active check-in found.")
        else:
            st.error("Please enter name")

# ---------------- REPORT SECTION ---------------- #
with tab2:
    st.subheader("Attendance Report")

    df = pd.read_csv(DB_FILE)
    st.dataframe(df, use_container_width=True)

    if not df.empty:
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "Download Full Report",
            data=csv,
            file_name="attendance_report.csv",
            mime="text/csv"
        )
