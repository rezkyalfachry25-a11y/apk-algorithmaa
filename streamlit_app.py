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

mgr = ManagerData()
auth = UserManager()

# ===== LOGIN =====
if not st.session_state.login:
    st.title("🔐 Login SIM Akademik")

    user = st.text_input("Username")
    pw = st.text_input("Password", type="password")

    if st.button("Login"):
        if auth.login(user, pw):
            st.session_state.login = True
            st.rerun()
        else:
            st.error("Username atau Password salah")

    st.stop()

# ===== HEADER =====
st.title("📘 Sistem Informasi Manajemen Akademik")
st.caption("Versi Web (Streamlit) – Migrasi dari Tkinter")

# ===== FORM INPUT =====
with st.form("form_input"):
    st.subheader("➕ Input Data Mahasiswa")

    col1, col2 = st.columns(2)

    nim = col1.text_input("NIM")
    nama = col1.text_input("Nama")
    jurusan = col2.text_input("Jurusan")
    angkatan = col2.number_input("Angkatan", 2000, 2100, 2023)
    semester = col2.number_input("Semester", 1, 14, 1)
    ipk = col1.number_input("IPK", 0.0, 4.0, 3.0)
    telepon = col2.text_input("Telepon")
    email = col2.text_input("Email")

    if st.form_submit_button("Tambah Data"):
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

# ===== TABEL DATA =====
st.subheader("📊 Data Mahasiswa")
df = pd.DataFrame([m.to_dict() for m in mgr.data])
st.dataframe(df, use_container_width=True)

# ===== SEARCH =====
st.subheader("🔍 Pencarian Data")
colA, colB, colC = st.columns(3)
keyword = colA.text_input("Keyword")
field = colB.selectbox("Cari berdasarkan", ["nim", "nama", "jurusan"])

if colC.button("Cari"):
    hasil = mgr.search(keyword, field)
    df = pd.DataFrame([m.to_dict() for m in hasil])
    st.dataframe(df, use_container_width=True)

# ===== SORTING =====
st.subheader("↕ Sorting Data")
c1, c2 = st.columns(2)

if c1.button("Sort Nama A-Z"):
    mgr.sort_nama()
    st.rerun()

if c2.button("Sort IPK"):
    mgr.sort_ipk()
    st.rerun()

# ===== DELETE =====
st.subheader("🗑 Hapus Data")
nim_del = st.text_input("Masukkan NIM")

if st.button("Hapus"):
    mgr.delete(nim_del)
    st.success("Data berhasil dihapus")
    st.rerun()

# ===== CHART =====
st.subheader("📈 Grafik IPK Mahasiswa")
if not df.empty:
    st.bar_chart(df["ipk"])

# ===== LOGOUT =====
if st.button("Logout"):
    st.session_state.login = False
    st.rerun()

