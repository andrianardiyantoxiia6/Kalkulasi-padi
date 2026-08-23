import streamlit as st
import math

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Kalkulator Tani: Jual vs Olah", page_icon="🌾", layout="centered")

# --- JUDUL APLIKASI ---
st.title("🌾 Kalkulator Keputusan Petani")
st.write("Aplikasi Analisis Keuntungan Berbasis Kondisi Fisik Panen: Jual Gabah vs Olah Menjadi Beras.")

# --- BUKU PANDUAN / GLOSARIUM DI SIDEBAR ---
with st.sidebar:
    st.header("📖 Glosarium & Panduan Tani")
    st.write("Panduan parameter fisik dan teknis pengolahan gabah.")
    
    with st.expander("1. Waktu Pemanenan"):
        st.write("**Istilah:** Waktu spesifik saat proses panen dilakukan.")
        st.info("• **Pagi Hari:** Embun/lembab tinggi (Potongan ringan -Rp100).\n• **Siang / Sore Hari:** Optimal dan kering angin (Normal).")
    
    with st.expander("2. Kondisi Fisik Padi (Kematangan & Warna)"):
        st.write("**Istilah:** Tingkat kemasakan bulir padi saat dipanen.")
        st.info("• **Siap Panen Seragam:** Kualitas prima, rendemen tinggi.\n• **Campur Bulir Hijau (Pruning/Belum Cukup Umur):** Banyak gabah hampa/hijau, rendemen susut dan potongan harga lebih tinggi.")

    with st.expander("3. Biaya Penjemuran"):
        st.write("**Istilah:** Biaya pengeringan per kuintal (pembulatan ke atas).")
    
    with st.expander("4. Derajat Sosoh (Kualitas Beras)"):
        st.write("**Istilah:** Tingkat keputihan dan kebersihan beras dari kulit ari.")
        st.info("• **Kurang Sosoh:** -Rp500/kg\n• **Sosoh Sedang:** Normal\n• **Sosoh Sempurna / Premium:** +Rp1.000/kg")
        
    st.divider()
    st.caption("💡 Instrumen Cerdas Pendukung Tugas Akhir & HAKI.")

# --- 1. DATA UTAMA GABAH ---
st.header("1. Data Jumlah & Harga Dasar Gabah")
berat_gabah_ton = st.number_input("Jumlah Gabah (Ton)", value=1.0, min_value=0.1, step=0.1)
berat_gabah_kg = berat_gabah_ton * 1000
berat_gabah_kuintal = berat_gabah_kg / 100

harga_gabah_dasar = st.number_input("Harga Dasar Gabah Kering Panen (Rp/kg)", value=7200, step=100)


# --- 2. WAKTU, CUACA & KONDISI FISIK PADI (OTOMATIS) ---
st.header("2. Waktu, Cuaca & Kondisi Fisik Padi Saat Panen")

pilihan_waktu = st.selectbox(
    "Kapan waktu pemanenan dilakukan?",
    [
        "Siang / Sore Hari (Waktu Optimal)",
        "Pagi Hari (Masih Berembun / Lembab)"
    ]
)

pilihan_cuaca = st.selectbox(
    "Bagaimana kondisi cuaca saat panen?",
    [
        "Terik Matahari (Kering Optimal)",
        "Mendung / Gerimis (Agak Basah)",
        "Hujan Deras / Habis Hujan (Sangat Basah)"
    ]
)

pilihan_kondisi_padi = st.selectbox(
    "Bagaimana kondisi fisik & kematangan bulir padi di lapangan?",
    [
        "Siap Panen Optimal (Kuning Merata & Bernas)",
        "Campur Bulir Hijau (Akibat Pruning / Pangkas Daun)",
        "Belum Cukup Umur / Banyak Gabah Hampa & Hijau"
    ]
)

# Logika Otomatis: Akumulasi Potongan Harga Gabah dari Waktu, Cuaca, & Kondisi Padi
penyesuaian_kadar_air = 0

if "Pagi Hari" in pilihan_waktu:
    penyesuaian_kadar_air -= 100

if "Mendung / Gerimis" in pilihan_cuaca:
    penyesuaian_kadar_air -= 200
elif "Hujan Deras" in pilihan_cuaca:
    penyesuaian_kadar_air -= 400

if "Campur Bulir Hijau" in pilihan_kondisi_padi:
    penyesuaian_kadar_air -= 300
elif "Belum Cukup Umur" in pilihan_kondisi_padi:
    penyesuaian_kadar_air -= 600

harga_gabah_final = harga_gabah_dasar + penyesuaian_kadar_air
st.info(f"🔍 **Deteksi Otomatis:** Total penyesuaian harga gabah sebesar **Rp {penyesuaian_kadar_air:,} /kg**.\n Harga Gabah Final: **Rp {harga_gabah_final:,} /kg**")


# --- 3. BIAYA & PENENTUAN RENDEMEN OTOMATIS ---
st.header("3. Biaya Penjemuran & Estimasi Rendemen")

tarif_jemur_per_kuintal = st.number_input("Biaya Penjemuran per Kuintal (Rp)", value=10000, step=1000)
total_biaya_jemur = math.ceil(berat_gabah_kuintal) * tarif_jemur_per_kuintal
st.caption(f"Total biaya penjemuran untuk {berat_gabah_kuintal} kuintal: Rp {total_biaya_jemur:,}")

# PENENTUAN RENDEMEN BERAS & DEDAK OTOMATIS BERDASARKAN KONDISI PADI
if "Siap Panen Optimal" in pilihan_kondisi_padi:
    persentase_beras = 65
    persentase_dedak = 14
elif "Campur Bulir Hijau" in pilihan_kondisi_padi:
    persentase_beras = 57
    persentase_dedak = 18 # Banyak bulir hijau hancur jadi menir/dedak halus
else: # Belum cukup umur
    persentase_beras = 50
    persentase_dedak = 20

st.success(f"🌾 **Rendemen Otomatis Terdeteksi:**\n- Estimasi Menjadi Beras: **{persentase_beras}%**\n- Estimasi Menjadi Dedak: **{persentase_dedak}%**")

berat_beras_kg = berat_gabah_kg * (persentase_beras / 100)
estimasi_dedak_kg = berat_gabah_kg * (persentase_dedak / 100)


# --- 4. DERAJAT SOSOH & KUALITAS PASAR BERAS ---
st.header("4. Derajat Sosoh & Kualitas Pasar Beras")

pilihan_sosoh = st.selectbox(
    "Bagaimana derajat sosoh (kondisi fisik hasil gilingan beras)?",
    [
        "Sosoh Sedang (Cukup bersih, standar pasaran lokal)",
        "Kurang Sosoh (Masih banyak kulit ari / merah kecoklatan)",
        "Sosoh Sempurna / Putih Bersih (Kualitas Premium)"
    ]
)

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
beras_bersih = berat_beras_kg - ongkos_giling_beras

biaya_transport_pribadi = 0
if "Diambil Sendiri" in tipe_ambil:
    biaya_transport_pribadi = st.number_input("Biaya Transportasi Pribadi (Rp)", value=50000, step=10000)


# --- 5. TOMBOL PERHITUNGAN & KEPUTUSAN ---
st.header("5. Hasil Analisis Keuntungan")
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
