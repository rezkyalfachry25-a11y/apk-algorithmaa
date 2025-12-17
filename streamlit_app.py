import streamlit as st
import pandas as pd
from manager import ManagerData
from models import Mahasiswa
from auth import UserManager

st.set_page_config(
    page_title="SIM Akademik",
    layout="wide"
)

# ===== SESSION =====
if "login" not in st.session_state:
    st.session_state.login = False

auth = UserManager()
mgr = ManagerData()

# ===== LOGIN =====
if not st.session_state.login:
    st.title("🔐 Login SIM Akademik")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.login(user, pw):
            st.session_state.login = True
            st.experimental_rerun()
        else:
            st.error("Username atau password salah")

    st.stop()

# ===== HEADER =====
st.title("📘 SIM Akademik (Streamlit Version)")
st.caption("Migrasi dari Tkinter → Web App")

# ===== FORM INPUT =====
with st.form("form_mhs"):
    st.subheader("➕ Input Mahasiswa")

    col1, col2 = st.columns(2)

    nim = col1.text_input("NIM")
    nama = col1.text_input("Nama")
    jurusan = col2.text_input("Jurusan")
    angkatan = col2.number_input("Angkatan", 2000, 2100, 2023)
    semester = col2.number_input("Semester", 1, 14, 1)
    ipk = col1.number_input("IPK", 0.0, 4.0, 3.0)
    telepon = col2.text_input("Telepon")
    email = col2.text_input("Email")

    submit = st.form_submit_button("Tambah Data")

    if submit:
        try:
            m = Mahasiswa(
                nim, nama, jurusan,
                angkatan, semester,
                ipk, telepon, email
            )
            mgr.add(m)
            st.success("Data berhasil ditambahkan")
        except Exception as e:
            st.error(str(e))

# ===== DATAFRAME =====
st.subheader("📊 Data Mahasiswa")

df = pd.DataFrame([m.to_dict() for m in mgr.data])

st.dataframe(df, use_container_width=True)

# ===== FILTER =====
st.subheader("🔍 Filter & Search")

colf1, colf2, colf3 = st.columns(3)
field = colf1.selectbox("Field", ["nama", "jurusan", "semester"])
keyword = colf2.text_input("Keyword")

if colf3.button("Cari"):
    result = mgr.search(keyword, field)
    df = pd.DataFrame([m.to_dict() for m in result])
    st.dataframe(df, use_container_width=True)

# ===== SORT =====
st.subheader("↕ Sorting")

cols = st.columns(3)
if cols[0].button("Sort Nama A-Z"):
    mgr.sort_by_name()
    st.experimental_rerun()

if cols[1].button("Sort IPK"):
    mgr.sort_by_ipk()
    st.experimental_rerun()

# ===== DELETE =====
st.subheader("🗑 Hapus Data")
nim_del = st.text_input("Masukkan NIM yang akan dihapus")

if st.button("Hapus"):
    mgr.delete(nim_del)
    st.success("Data dihapus")
    st.experimental_rerun()

# ===== CHART =====
st.subheader("📈 Visualisasi IPK")
if not df.empty:
    st.bar_chart(df["ipk"])

# ===== LOGOUT =====
if st.button("Logout"):
    st.session_state.login = False
    st.experimental_rerun()
