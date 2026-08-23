import streamlit as st
import math

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Kalkulator Tani: Jual vs Olah", page_icon="🌾", layout="centered")

# --- JUDUL APLIKASI ---
st.title("🌾 Kalkulator Keputusan Petani")
st.write("Aplikasi Analisis Keuntungan: Menjual Gabah Langsung vs Diolah Menjadi Beras.")

# --- BUKU PANDUAN / GLOSARIUM DI SIDEBAR ---
with st.sidebar:
    st.header("📖 Glosarium & Panduan Tani")
    st.write("Panduan istilah teknis dan simulasi visual untuk membantu pengisian data.")
    
    with st.expander("1. Kadar Air & Cuaca Panen"):
        st.write("**Istilah:** Pengaruh cuaca saat panen terhadap kadar air gabah.")
        st.write("🌦️ **Simulasi Kondisi:**")
        st.info("• **Pagi / Hujan:** Gabah basah, berat lebih berat tapi dipotong harga -Rp300/kg.\n• **Siang / Terik:** Gabah kering optimal, harga normal tanpa potongan.")
    
    with st.expander("2. Biaya Penjemuran"):
        st.write("**Istilah:** Biaya pengeringan gabah (dihitung per kuintal dengan pembulatan ke atas).")
        st.write("☀️ **Simulasi Kasus:**")
        st.info("Jika Anda punya 1,2 ton (12 kuintal) gabah, total kuantitas dikalikan tarif jemur (misal: 12 x Rp10.000 = Rp120.000).")
    
    with st.expander("3. Derajat Sosoh (Kualitas Beras)"):
        st.write("**Istilah:** Tingkat keputihan dan kebersihan beras dari kulit ari setelah digiling.")
        st.write("🌾 **Simulasi Visual Fisik:**")
        st.info("• **Kurang Sosoh:** Masih ada kulit ari (-Rp500/kg).\n• **Sosoh Sedang:** Standar pasaran lokal (Normal).\n• **Sosoh Premium:** Putih bersih mengkilap (+Rp1.000/kg).")
    
    with st.expander("4. Ongkos Giling & Logistik"):
        st.write("**Istilah:** Biaya jasa pabrik (sistem bagi hasil beras).")
        st.write("🚚 **Simulasi Opsi:**")
        st.info("• **Pihak Pabrik Jemput:** Pabrik ambil ke rumah, ongkos naik 1%.\n• **Diambil Sendiri:** Ongkos standar 10% tapi keluar biaya transport pribadi.")
        
    st.divider()
    st.caption("💡 Glosarium ini dirancang untuk memudahkan pemahaman petani dan dokumen pelengkap HAKI/Skripsi.")

# --- 1. INPUT DATA UTAMA & CUACA (OTOMATIS) ---
st.header("1. Data Panen & Kondisi Cuaca")
berat_gabah_ton = st.number_input("Jumlah Gabah (Ton)", value=1.0, min_value=0.1, step=0.1)
berat_gabah_kg = berat_gabah_ton * 1000
berat_gabah_kuintal = berat_gabah_kg / 100

harga_gabah_dasar = st.number_input("Harga Dasar Gabah Kering Panen (Rp/kg)", value=7200, step=100)

# PILIHAN CUACA OTOMATIS
pilihan_cuaca = st.selectbox(
    "Bagaimana kondisi cuaca atau waktu saat memanen?",
    [
        "Siang / Terik Matahari (Kering Optimal - Tanpa Potongan)",
        "Pagi Hari / Lembab (Sedikit Basah - Potongan Ringan)",
        "Musim Hujan / Habis Hujan (Sangat Basah - Potongan Tinggi)"
    ]
)

# Logika otomatis penyesuaian harga berdasarkan cuaca
if "Siang / Terik" in pilihan_cuaca:
    penyesuaian_kadar_air = 0
elif "Pagi Hari" in pilihan_cuaca:
    penyesuaian_kadar_air = -200
else:
    penyesuaian_kadar_air = -400

harga_gabah_final = harga_gabah_dasar + penyesuaian_kadar_air
st.info(f"🔍 **Deteksi Otomatis:** Penyesuaian kadar air sebesar **Rp {penyesuaian_kadar_air:,} /kg**.\n Harga Gabah Final: **Rp {harga_gabah_final:,} /kg**")


# --- 2. INPUT BIAYA & PENGOLAHAN ---
st.header("2. Biaya & Parameter Pengolahan")

tarif_jemur_per_kuintal = st.number_input("Biaya Penjemuran per Kuintal (Rp)", value=10000, step=1000)
total_biaya_jemur = math.ceil(berat_gabah_kuintal) * tarif_jemur_per_kuintal
st.caption(f"Total biaya penjemuran untuk {berat_gabah_kuintal} kuintal: Rp {total_biaya_jemur:,}")

persentase_beras = st.slider("Estimasi Rendemen Beras (%)", min_value=40, max_value=75, value=60)
berat_beras_kg = berat_gabah_kg * (persentase_beras / 100)

persentase_dedak = st.slider("Estimasi Hasil Dedak (%)", min_value=5, max_value=25, value=15)
estimasi_dedak_kg = berat_gabah_kg * (persentase_dedak / 100)


# --- 3. DERAJAT SOSOH & HARGA PASAR (OTOMATIS) ---
st.header("3. Kualitas Giling & Harga Pasar")

pilihan_sosoh = st.selectbox(
    "Bagaimana kondisi fisik hasil gilingan beras (Derajat Sosoh)?",
    [
        "Sosoh Sedang (Cukup bersih, standar pasaran lokal)",
        "Kurang Sosoh (Masih banyak kulit ari / merah kecoklatan)",
        "Sosoh Sempurna / Putih Bersih (Kualitas Premium)"
    ]
)

# Logika otomatis penyesuaian harga beras berdasarkan derajat sosoh
if "Kurang Sosoh" in pilihan_sosoh:
    pengaruh_harga_beras = -500
elif "Sosoh Sedang" in pilihan_sosoh:
    pengaruh_harga_beras = 0
else:
    pengaruh_harga_beras = 1000

harga_beras_dasar = st.number_input("Harga Dasar Jual Beras Bersih di Pasar (Rp/kg)", value=14500, step=100)
harga_beras_final = harga_beras_dasar + pengaruh_harga_beras
st.info(f"🔍 **Deteksi Otomatis:** Penyesuaian kualitas sosoh sebesar **Rp {pengaruh_harga_beras:+,} /kg**.\n Estimasi Harga Beras Final: **Rp {harga_beras_final:,} /kg**")

harga_dedak = st.number_input("Harga Jual Dedak (Rp/kg)", value=3500, step=100)

tipe_ambil = st.radio("Metode Pengambilan Hasil Giling:", [
    "Pihak Pabrik yang Ambil (Tambah 1% ongkos)", 
    "Diambil Sendiri (Ongkos standar 10% + Biaya Transport Pribadi)"
])

persentase_ongkos = 0.11 if "Pihak Pabrik" in tipe_ambil else 0.10
ongkos_giling_beras = berat_beras_kg * persentase_ongkos
beras_bersih = beras_berat_kg = berat_beras_kg - ongkos_giling_beras

biaya_transport_pribadi = 0
if "Diambil Sendiri" in tipe_ambil:
    biaya_transport_pribadi = st.number_input("Biaya Transportasi Pribadi (Rp)", value=50000, step=10000)


# --- 4. TOMBOL PERHITUNGAN & KEPUTUSAN ---
st.header("4. Hasil Analisis Keuntungan")
if st.button("Hitung dan Bandingkan Keuntungan"):
    pendapatan_jual_gabah = berat_gabah_kg * harga_gabah_final
    
    pendapatan_beras = beras_bersih * harga_beras_final
    pendapatan_dedak = estimasi_dedak_kg * harga_dedak
    total_pengeluaran_olah = total_biaya_jemur + biaya_transport_pribadi
    total_pendapatan_olah = pendapatan_beras + pendapatan_dedak - total_pengeluaran_olah
    
    selisih = total_pendapatan_olah - pendapatan_jual_gabah
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Opsi Jual Gabah", f"Rp {pendapatan_jual_gabah:,.0f}")
    with col2:
        st.metric("Opsi Olah Jadi Beras", f"Rp {total_pendapatan_olah:,.0f}")
    
    st.divider()
    
    if selisih > 0:
        st.success(f"**Rekomendasi:** Lebih menguntungkan **DIOLAH MENJADI BERAS**.\n\nPotensi tambahan keuntungannya adalah sekitar **Rp {selisih:,.0f}**.")
    else:
        st.warning(f"**Rekomendasi:** Lebih menguntungkan **DIJUAL GABAH LANGSUNG**.\n\nJika diolah, Anda berisiko rugi/selisih lebih rendah sekitar **Rp {abs(selisih):,.0f}**.")
