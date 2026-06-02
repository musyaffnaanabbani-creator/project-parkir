import streamlit as st
from datetime import datetime
import pandas as pd

# =====================================================
# LOGIN ADMIN
# =====================================================

ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "123"

# =====================================================
# LINKED LIST NODE
# =====================================================

class KendaraanNode:
    def __init__(self, tiket, plat, jenis, waktu_masuk):
        self.tiket = tiket
        self.plat = plat
        self.jenis = jenis
        self.waktu_masuk = waktu_masuk
        self.next = None

# =====================================================
# LINKED LIST PARKIR
# =====================================================

class LinkedListParkir:
    def __init__(self):
        self.head = None

    def tambah(self, node):
        if self.head is None:
            self.head = node
            return

        current = self.head

        while current.next:
            current = current.next

        current.next = node

    def tampilkan(self):
        data = []

        current = self.head

        while current:
            data.append({
                "Tiket": current.tiket,
                "Plat": current.plat,
                "Jenis": current.jenis,
                "Waktu Masuk": current.waktu_masuk
            })

            current = current.next

        return data

    def cari(self, plat):
        current = self.head

        while current:
            if current.plat.lower() == plat.lower():
                return current

            current = current.next

        return None

    def hapus(self, plat):
        current = self.head

        prev = None

        while current:

            if current.plat.lower() == plat.lower():

                if prev:
                    prev.next = current.next
                else:
                    self.head = current.next

                return current

            prev = current
            current = current.next

        return None

# =====================================================
# SESSION STATE
# =====================================================

if "login" not in st.session_state:
    st.session_state.login = False

if "parkir" not in st.session_state:
    st.session_state.parkir = LinkedListParkir()

if "riwayat" not in st.session_state:
    st.session_state.riwayat = []

if "pendapatan" not in st.session_state:
    st.session_state.pendapatan = 0

if "nomor_tiket" not in st.session_state:
    st.session_state.nomor_tiket = 1000

# =====================================================
# LOGIN PAGE
# =====================================================

if not st.session_state.login:

    st.title("🅿️ SISTEM PARKIR MALL")

    st.subheader("Login Admin")

    username = st.text_input("Username")

    password = st.text_input("Password", type="password")

    if st.button("Login"):

        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            st.session_state.login = True
            st.success("Login Berhasil")
            st.rerun()

        else:
            st.error("Username atau Password Salah")

# =====================================================
# DASHBOARD
# =====================================================

else:

    st.title("🏢 SISTEM PARKIR MALL")

    menu = st.sidebar.radio(
        "Menu",
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

    # =================================================
    # DASHBOARD
    # =================================================

    if menu == "Dashboard":

        total_parkir = len(st.session_state.parkir.tampilkan())

        total_transaksi = len(st.session_state.riwayat)

        col1, col2, col3 = st.columns(3)

        col1.metric("Kendaraan Parkir", total_parkir)

        col2.metric("Transaksi", total_transaksi)

        col3.metric(
            "Pendapatan",
            f"Rp {st.session_state.pendapatan:,}"
        )

        st.info("Selamat Datang di Dashboard Sistem Parkir Mall")

    # =================================================
    # KENDARAAN MASUK
    # =================================================

    elif menu == "Kendaraan Masuk":

        st.subheader("🚗 Kendaraan Masuk")

        plat = st.text_input("Plat Nomor")

        jenis = st.selectbox(
            "Jenis Kendaraan",
            ["Motor", "Mobil"]
        )

        if st.button("Cetak Tiket"):

            tiket = f"TKT-{st.session_state.nomor_tiket}"

            st.session_state.nomor_tiket += 1

            waktu = datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            )

            node = KendaraanNode(
                tiket,
                plat,
                jenis,
                waktu
            )

            st.session_state.parkir.tambah(node)

            st.success("Kendaraan Berhasil Masuk")

            st.write("### TIKET PARKIR")

            st.write(f"Nomor Tiket : {tiket}")
            st.write(f"Plat Nomor : {plat}")
            st.write(f"Jenis : {jenis}")
            st.write(f"Waktu Masuk : {waktu}")

    # =================================================
    # KENDARAAN KELUAR
    # =================================================

    elif menu == "Kendaraan Keluar":

        st.subheader("🚘 Kendaraan Keluar")

        plat = st.text_input("Masukkan Plat Nomor")

        metode = st.selectbox(
            "Metode Pembayaran",
            [
                "Cash",
                "QRIS",
                "Debit",
                "Kredit",
                "E-Wallet"
            ]
        )

        if st.button("Proses Keluar"):

            data = st.session_state.parkir.cari(plat)

            if data:

                masuk = datetime.strptime(
                    data.waktu_masuk,
                    "%d-%m-%Y %H:%M:%S"
                )

                keluar = datetime.now()

                durasi = (
                    keluar - masuk
                ).total_seconds() / 3600

                if data.jenis == "Motor":
                    tarif = 3000
                else:
                    tarif = 5000

                biaya = max(1, int(durasi)) * tarif

                st.write("### Detail Pembayaran")

                st.write("Plat :", data.plat)
                st.write("Jenis :", data.jenis)
                st.write("Metode :", metode)
                st.write("Total :", f"Rp {biaya:,}")

                st.session_state.pendapatan += biaya

                st.session_state.riwayat.append({
                    "Plat": data.plat,
                    "Jenis": data.jenis,
                    "Masuk": data.waktu_masuk,
                    "Keluar": keluar.strftime(
                        "%d-%m-%Y %H:%M:%S"
                    ),
                    "Metode": metode,
                    "Biaya": biaya
                })

                st.session_state.parkir.hapus(plat)

                st.success(
                    "Kendaraan Keluar Berhasil"
                )

            else:
                st.error(
                    "Kendaraan Tidak Ditemukan"
                )

    # =================================================
    # DAFTAR PARKIR
    # =================================================

    elif menu == "Daftar Parkir":

        st.subheader("📋 Daftar Kendaraan Parkir")

        data = st.session_state.parkir.tampilkan()

        if data:
            st.dataframe(pd.DataFrame(data))
        else:
            st.warning(
                "Belum Ada Kendaraan Parkir"
            )

    # =================================================
    # CARI KENDARAAN
    # =================================================

    elif menu == "Cari Kendaraan":

        st.subheader("🔍 Cari Kendaraan")

        plat = st.text_input("Masukkan Plat")

        if st.button("Cari"):

            data = st.session_state.parkir.cari(plat)

            if data:

                st.success("Ditemukan")

                st.write("Tiket :", data.tiket)
                st.write("Plat :", data.plat)
                st.write("Jenis :", data.jenis)
                st.write(
                    "Masuk :",
                    data.waktu_masuk
                )

            else:
                st.error(
                    "Kendaraan Tidak Ada"
                )

    # =================================================
    # SORTING PLAT
    # =================================================

    elif menu == "Sorting Plat":

        st.subheader("🔤 Sorting Plat Nomor")

        data = st.session_state.parkir.tampilkan()

        if data:

            data_sort = sorted(
                data,
                key=lambda x: x["Plat"]
            )

            st.dataframe(
                pd.DataFrame(data_sort)
            )

        else:
            st.warning(
                "Data Parkir Kosong"
            )

    # =================================================
    # RIWAYAT TRANSAKSI
    # =================================================

    elif menu == "Riwayat Transaksi":

        st.subheader("📜 Riwayat Transaksi")

        if st.session_state.riwayat:

            st.dataframe(
                pd.DataFrame(
                    st.session_state.riwayat
                )
            )

        else:
            st.warning(
                "Belum Ada Transaksi"
            )

    # =================================================
    # PENDAPATAN
    # =================================================

    elif menu == "Pendapatan":

        st.subheader("💰 Pendapatan Parkir")

        st.metric(
            "Total Pendapatan",
            f"Rp {st.session_state.pendapatan:,}"
        )