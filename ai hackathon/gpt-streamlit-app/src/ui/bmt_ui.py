import streamlit as st
import pandas as pd
from pathlib import Path


DATA_DIR = Path.cwd()
DONOR_FILE = DATA_DIR / "donors.csv"
PATIENT_FILE = DATA_DIR / "patients.csv"


def load_csv(path, columns):
    if path.exists():
        try:
            return pd.read_csv(path)
        except Exception:
            # If file exists but is empty or corrupted, return empty frame with columns
            return pd.DataFrame(columns=columns)
    else:
        return pd.DataFrame(columns=columns)


def append_row(path: Path, row: dict, columns):
    df = load_csv(path, columns)
    new_df = pd.DataFrame([row])
    # append to CSV, write header only if file doesn't exist
    new_df.to_csv(path, mode="a", header=not path.exists(), index=False, encoding="utf-8")


def donor_tab():
    st.header("Donor Information")
    with st.form(key="donor_form"):
        name = st.text_input("Name")
        age = st.number_input("Age", min_value=0, max_value=120, value=30)
        city = st.text_input("City")
        hla = st.text_input("HLA (e.g. A*01:01;B*08:01)")
        submitted = st.form_submit_button("Save Donor")

    if submitted:
        if not name:
            st.error("Name is required")
        else:
            row = {"Name": name, "Age": age, "City": city, "HLA": hla}
            append_row(DONOR_FILE, row, ["Name", "Age", "City", "HLA"])
            st.success(f"Saved donor: {name}")

    st.markdown("---")
    st.subheader("Existing donors")
    donors = load_csv(DONOR_FILE, ["Name", "Age", "City", "HLA"])
    if donors.empty:
        st.info("No donors yet. Add one above.")
    else:
        st.dataframe(donors)


def patient_tab():
    st.header("Patient Information")
    with st.form(key="patient_form"):
        name = st.text_input("Name", key="pname")
        age = st.number_input("Age", min_value=0, max_value=120, value=40, key="page")
        city = st.text_input("City", key="pcity")
        hla = st.text_input("HLA (e.g. A*01:01;B*08:01)", key="phla")
        submitted = st.form_submit_button("Save Patient")

    if submitted:
        if not name:
            st.error("Name is required")
        else:
            row = {"Name": name, "Age": age, "City": city, "HLA": hla}
            append_row(PATIENT_FILE, row, ["Name", "Age", "City", "HLA"])
            st.success(f"Saved patient: {name}")

    st.markdown("---")
    st.subheader("Patient list and HLA search")
    patients = load_csv(PATIENT_FILE, ["Name", "Age", "City", "HLA"])

    col1, col2 = st.columns([3, 1])
    with col1:
        st.dataframe(patients)
    with col2:
        query = st.text_input("Find HLA (substring)")
        if query:
            # case-insensitive contains search in HLA column
            matches = patients[patients["HLA"].astype(str).str.contains(query, case=False, na=False)]
            st.metric("Matches", len(matches))
            st.dataframe(matches)


def main():
    st.set_page_config(page_title="Bone Marrow Transmission UI", layout="centered")
    st.title("Bone Marrow Transmission — Donor/Patient")
    tabs = st.tabs(["Donor", "Patient"])
    with tabs[0]:
        donor_tab()
    with tabs[1]:
        patient_tab()


if __name__ == "__main__":
    main()
