import streamlit as st

st.title("Aplikasi Pendukung Keputusan: Jual Gabah vs Olah Beras")
st.write("Sesuaikan parameter di bawah ini sesuai dengan kondisi riil di daerah Anda.")

# --- 1. INPUT DATA UTAMA & Kondisi Panen ---
st.header("1. Data Panen & Kondisi Cuaca")
berat_gabah_ton = st.number_input("Jumlah Gabah (Ton)", value=1.0, min_value=0.1, step=0.1)
berat_gabah_kg = berat_gabah_ton * 1000
berat_gabah_kuintal = berat_gabah_kg / 100

harga_gabah_dasar = st.number_input("Harga Dasar Gabah Kering Panen (Rp/kg)", value=7200, step=100)

st.subheader("Pengaruh Kadar Air Berdasarkan Cuaca/Waktu")
st.write("Tentukan sendiri penyesuaian harga (bisa bernilai minus jika basah, atau plus jika kering)")
penyesuaian_kadar_air = st.number_input("Penyesuaian Harga karena Kadar Air (Rp/kg)", value=-300, step=50, help="Contoh: Masukkan angka negatif jika gabah basah karena hujan/pagi hari.")
harga_gabah_final = harga_gabah_dasar + penyesuaian_kadar_air
st.info(f"Harga Gabah Final Setelah Penyesuaian: **Rp {harga_gabah_final:,} /kg**")


# --- 2. INPUT BIAYA & PENGOLAHAN ---
st.header("2. Biaya & Parameter Pengolahan")

# Biaya Penjemuran dengan aturan pembulatan kelebihan kuintal
tarif_jemur_per_kuintal = st.number_input("Biaya Penjemuran per Kuintal (Rp)", value=10000, step=1000)
# Menggunakan pembulatan ke atas untuk sisa kuintal
import math
total_biaya_jemur = math.ceil(berat_gabah_kuintal) * tarif_jemur_per_kuintal
st.caption(f"Total biaya penjemuran untuk {berat_gabah_kuintal} kuintal: Rp {total_biaya_jemur:,}")

# Rendemen & Hasil Sampingan
persentase_beras = st.slider("Estimasi Rendemen Beras (%)", min_value=40, max_value=75, value=60)
berat_beras_kg = berat_gabah_kg * (persentase_beras / 100)

persentase_dedak = st.slider("Estimasi Hasil Dedak (%)", min_value=5, max_value=25, value=15)
estimasi_dedak_kg = berat_gabah_kg * (persentase_dedak / 100)


# --- 3. ONGKOS GILING & HARGA JUAL PRODUK OLAHAN ---
st.header("3. Ongkos Giling & Harga Pasar")

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

harga_beras = st.number_input("Harga Jual Beras Bersih di Pasar (Rp/kg)", value=14500, step=100)
harga_dedak = st.number_input("Harga Jual Dedak (Rp/kg)", value=3500, step=100)


# --- 4. TOMBOL PERHITUNGAN & KEPUTUSAN ---
st.header("4. Hasil Analisis Keuntungan")
if st.button("Hitung dan Bandingkan Keuntungan"):
    # Opsi A: Jual Gabah
    pendapatan_jual_gabah = berat_gabah_kg * harga_gabah_final
    
    # Opsi B: Olah Beras
    pendapatan_beras = beras_bersih * harga_beras
    pendapatan_dedak = estimasi_dedak_kg * harga_dedak
    total_pengeluaran_olah = total_biaya_jemur + biaya_transport_pribadi
    total_pendapatan_olah = pendapatan_beras + pendapatan_dedak - total_pengeluaran_olah
    
    selisih = total_pendapatan_olah - pendapatan_jual_gabah
    
    # Tampilkan Rincian
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
