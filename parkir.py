import streamlit as st
import pandas as pd
import random
from datetime import datetime

# =====================================
# CONFIG
# =====================================
st.set_page_config(
    page_title="Sistem Parkir UAS",
    page_icon="🚗",
    layout="wide"
)

# =====================================
# NODE LINKED LIST
# =====================================
class Node:
    def __init__(self, plat, jenis):
        self.tiket = random.randint(10000, 99999)
        self.plat = plat.upper()
        self.jenis = jenis
        self.masuk = datetime.now()
        self.next = None

# =====================================
# LINKED LIST
# =====================================
class ParkirLinkedList:
    def __init__(self, kapasitas=50):
        self.head = None
        self.kapasitas = kapasitas

    def jumlah_kendaraan(self):
        count = 0
        cur = self.head

        while cur:
            count += 1
            cur = cur.next

        return count

    def cari(self, plat):
        cur = self.head

        while cur:
            if cur.plat == plat.upper():
                return cur
            cur = cur.next

        return None

    def tambah(self, plat, jenis):

        if self.jumlah_kendaraan() >= self.kapasitas:
            return False, "Parkiran penuh"

        if self.cari(plat):
            return False, "Plat sudah terdaftar"

        baru = Node(plat, jenis)

        if self.head is None:
            self.head = baru
            return True, baru

        cur = self.head

        while cur.next:
            cur = cur.next

        cur.next = baru

        return True, baru

    def tampil(self):

        data = []

        cur = self.head

        while cur:

            data.append({
                "Tiket": cur.tiket,
                "Plat": cur.plat,
                "Jenis": cur.jenis,
                "Jam Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M:%S")
            })

            cur = cur.next

        return data

    def keluar(self, plat):

        cur = self.head
        prev = None

        while cur:

            if cur.plat == plat.upper():

                keluar = datetime.now()

                jam = max(
                    1,
                    int((keluar - cur.masuk).total_seconds() // 3600) + 1
                )

                if cur.jenis == "Motor":
                    biaya = 3000 + ((jam - 1) * 2000)
                else:
                    biaya = 5000 + ((jam - 1) * 4000)

                hasil = {
                    "Tiket": cur.tiket,
                    "Plat": cur.plat,
                    "Jenis": cur.jenis,
                    "Jam Masuk": cur.masuk.strftime("%d-%m-%Y %H:%M:%S"),
                    "Jam Keluar": keluar.strftime("%d-%m-%Y %H:%M:%S"),
                    "Lama Parkir (Jam)": jam,
                    "Biaya": biaya
                }

                if prev:
                    prev.next = cur.next
                else:
                    self.head = cur.next

                return hasil

            prev = cur
            cur = cur.next

        return None

# =====================================
# BUBBLE SORT
# =====================================
def bubble_sort(data):

    n = len(data)

    for i in range(n):

        for j in range(0, n - i - 1):

            if data[j]["Plat"] > data[j + 1]["Plat"]:

                data[j], data[j + 1] = data[j + 1], data[j]

    return data

# =====================================
# SESSION
# =====================================
if "parkir" not in st.session_state:
    st.session_state.parkir = ParkirLinkedList()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "login" not in st.session_state:
    st.session_state.login = False

# =====================================
# LOGIN
# =====================================
if not st.session_state.login:

    st.title("🔐 Login Admin")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == "admin" and password == "123":

            st.session_state.login = True
            st.rerun()

        else:
            st.error("Username atau Password salah")

    st.stop()

# =====================================
# SIDEBAR
# =====================================
st.sidebar.title("Menu")

menu = st.sidebar.selectbox(
    "Pilih Menu",
    [
        "Dashboard",
        "Kendaraan Masuk",
        "Kendaraan Keluar",
        "Daftar Parkir",
        "Cari Kendaraan",
        "Sorting Plat",
        "Riwayat Transaksi",
        "Pendapatan"
    ]
)

if st.sidebar.button("Logout"):
    st.session_state.login = False
    st.rerun()

# =====================================
# DASHBOARD
# =====================================
if menu == "Dashboard":

    st.title("📊 Dashboard Parkir")

    total = st.session_state.parkir.jumlah_kendaraan()

    motor = 0
    mobil = 0

    for x in st.session_state.parkir.tampil():

        if x["Jenis"] == "Motor":
            motor += 1
        else:
            mobil += 1

    c1, c2, c3 = st.columns(3)

    c1.metric("Kendaraan Aktif", total)
    c2.metric("Motor", motor)
    c3.metric("Mobil", mobil)

    st.subheader("Kapasitas Parkir")

    kapasitas = st.session_state.parkir.kapasitas

    st.progress(total / kapasitas)

    st.write(f"{total}/{kapasitas} Slot Terisi")

# =====================================
# MASUK
# =====================================
elif menu == "Kendaraan Masuk":

    st.title("🚗 Kendaraan Masuk")

    plat = st.text_input("Plat Nomor")

    jenis = st.selectbox(
        "Jenis Kendaraan",
        ["Motor", "Mobil"]
    )

    if st.button("Simpan"):

        if plat:

            sukses, hasil = st.session_state.parkir.tambah(
                plat,
                jenis
            )

            if sukses:

                st.success("Kendaraan berhasil masuk")

                st.info(
                    f"""
                    Tiket : {hasil.tiket}
                    
                    Plat : {hasil.plat}
                    
                    Jenis : {hasil.jenis}
                    """
                )

            else:
                st.error(hasil)

# =====================================
# KELUAR
# =====================================
elif menu == "Kendaraan Keluar":

    st.title("💳 Pembayaran Parkir")

    plat = st.text_input("Masukkan Plat")

    if st.button("Proses"):

        hasil = st.session_state.parkir.keluar(plat)

        if hasil:

            st.session_state.riwayat.append(hasil)

            st.success("Pembayaran Berhasil")

            st.dataframe(
                pd.DataFrame([hasil]),
                use_container_width=True
            )

        else:
            st.error("Plat tidak ditemukan")

# =====================================
# DAFTAR
# =====================================
elif menu == "Daftar Parkir":

    st.title("🅿️ Kendaraan Sedang Parkir")

    data = st.session_state.parkir.tampil()

    if data:

        st.dataframe(
            pd.DataFrame(data),
            use_container_width=True
        )

    else:
        st.warning("Parkiran kosong")

# =====================================
# CARI
# =====================================
elif menu == "Cari Kendaraan":

    st.title("🔍 Cari Kendaraan")

    plat = st.text_input("Plat Nomor")

    if st.button("Cari"):

        hasil = st.session_state.parkir.cari(plat)

        if hasil:

            st.success("Data ditemukan")

            st.write({
                "Tiket": hasil.tiket,
                "Plat": hasil.plat,
                "Jenis": hasil.jenis,
                "Jam Masuk": hasil.masuk.strftime("%d-%m-%Y %H:%M:%S")
            })

        else:
            st.error("Data tidak ditemukan")

# =====================================
# SORTING
# =====================================
elif menu == "Sorting Plat":

    st.title("🔤 Sorting Plat")

    data = st.session_state.parkir.tampil()

    if data:

        hasil = bubble_sort(data)

        st.dataframe(
            pd.DataFrame(hasil),
            use_container_width=True
        )

    else:
        st.info("Belum ada data")

# =====================================
# RIWAYAT
# =====================================
elif menu == "Riwayat Transaksi":

    st.title("📄 Riwayat Transaksi")

    if st.session_state.riwayat:

        df = pd.DataFrame(
            st.session_state.riwayat
        )

        st.dataframe(
            df,
            use_container_width=True
        )

        csv = df.to_csv(index=False)

        st.download_button(
            "Download CSV",
            csv,
            "riwayat_parkir.csv",
            "text/csv"
        )

    else:
        st.info("Belum ada transaksi")

# =====================================
# PENDAPATAN
# =====================================
elif menu == "Pendapatan":

    st.title("💰 Pendapatan")

    total = sum(
        x["Biaya"]
        for x in st.session_state.riwayat
    )

    st.metric(
        "Total Pendapatan",
        f"Rp {total:,}"
    )

    st.metric(
        "Jumlah Transaksi",
        len(st.session_state.riwayat)
    )

    if st.session_state.riwayat:

        df = pd.DataFrame(
            st.session_state.riwayat
        )

        st.line_chart(df["Biaya"])