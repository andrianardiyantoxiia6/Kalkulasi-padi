import streamlit as st
import math

# --- PENGATURAN HALAMAN ---
st.set_page_config(page_title="Sistem DSS Analisis Gabah & Beras", page_icon="🌾", layout="centered")

# --- JUDUL APLIKASI ---
st.title("🌾 Decision Support System (DSS) Agribisnis Padi")
st.write("Platform Analisis Terpadu untuk Petani & Pengelola Pabrik Gabah (RMU).")

# Inisialisasi state untuk menyimpan pilihan mode
if 'pilihan_aktif' not in st.session_state:
    st.session_state.pilihan_aktif = None

# --- SIDEBAR & MENU UTAMA ---
with st.sidebar:
    st.header("📖 Glosarium Sistem")
    
    with st.expander("1. Parameter Fisik & Cuaca"):
        st.write("Menentukan tingkat kadar air, potensi susut bobot, dan persentase rendemen beras serta dedak secara otomatis.")
    
    with st.expander("2. Derajat Sosoh"):
        st.write("Tingkat kebersihan beras dari kulit ari yang memengaruhi harga jual pasar.")
        
    with st.expander("3. Kalkulasi Bisnis Pabrik"):
        st.write("Memperhitungkan margin kotor, biaya operasional jemur/giling, biaya transport logistik, hingga keuntungan bersih pabrik.")
        
    st.caption("💡 Instrumen Utama Tugas Akhir & HAKI.")

# TAMPILAN AWAL: TOMBOL PILIH MODE
if st.session_state.pilihan_aktif is None:
    st.markdown("### Silakan pilih peran atau mode penggunaan aplikasi:")
    
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("👨‍🌾 Masuk ke Mode Petani", use_container_width=True):
            st.session_state.pilihan_aktif = "petani"
            st.rerun()
    with col_b:
        if st.button("🏭 Masuk ke Mode Pabrik", use_container_width=True):
            st.session_state.pilihan_aktif = "pabrik"
            st.rerun()

else:
    # Tombol untuk kembali ke menu utama pemilihan mode
    if st.button("⬅️ Kembali ke Pilihan Mode"):
        st.session_state.pilihan_aktif = None
        st.rerun()
    
    st.markdown("---")

    # ==========================================
    # KONDISI 1: MODE PETANI
    # ==========================================
    if st.session_state.pilihan_aktif == "petani":
        st.subheader("👨‍🌾 Analisis Keputusan Petani: Jual Gabah vs Olah Beras")
        
        berat_gabah_kg = st.number_input("Jumlah Gabah Petani (Kilogram / kg)", value=1000.0, min_value=10.0, step=50.0)
        harga_gabah_dasar = st.number_input("Harga Dasar Gabah Kering Panen (Rp/kg)", value=7200, step=100)

        st.markdown("---")
        st.write("### 🌦️ Kondisi Lapangan Saat Panen")
        pilihan_waktu = st.selectbox("Waktu Pemanenan:", ["Siang / Sore Hari (Waktu Optimal)", "Pagi Hari (Masih Berembun / Lembab)"])
        pilihan_cuaca = st.selectbox("Kondisi Cuaca:", ["Terik Matahari (Kering Optimal)", "Mendung / Gerimis (Agak Basah)", "Hujan Deras / Habis Hujan (Sangat Basah)"])
        pilihan_kondisi_padi = st.selectbox("Kondisi Fisik Bulir Padi:", ["Siap Panen Optimal (Kuning Merata & Bernas)", "Campur Bulir Hijau (Akibat Pruning / Pangkas)", "Belum Cukup Umur / Banyak Gabah Hampa"])

        penyesuaian_kadar_air = 0
        if "Pagi Hari" in pilihan_waktu: penyesuaian_kadar_air -= 100
        if "Mendung / Gerimis" in pilihan_cuaca: penyesuaian_kadar_air -= 200
        elif "Hujan Deras" in pilihan_cuaca: penyesuaian_kadar_air -= 400
        if "Campur Bulir Hijau" in pilihan_kondisi_padi: penyesuaian_kadar_air -= 300
        elif "Belum Cukup Umur" in pilihan_kondisi_padi: penyesuaian_kadar_air -= 600

        harga_gabah_final = harga_gabah_dasar + penyesuaian_kadar_air
        st.info(f"🔍 **Deteksi Otomatis Penyesuaian Harga:** Rp {penyesuaian_kadar_air:,} /kg | **Harga Gabah Final:** Rp {harga_gabah_final:,} /kg")

        st.markdown("---")
        st.write("### ⚙️ Pengolahan & Penggilingan")
        tarif_jemur_per_kg = st.number_input("Biaya Penjemuran (Rp/kg)", value=100, step=10)
        total_biaya_jemur = berat_gabah_kg * tarif_jemur_per_kg

        if "Siap Panen Optimal" in pilihan_kondisi_padi:
            persentase_beras, persentase_dedak = 65, 14
        elif "Campur Bulir Hijau" in pilihan_kondisi_padi:
            persentase_beras, persentase_dedak = 57, 18
        else:
            persentase_beras, persentase_dedak = 50, 20

        st.success(f"🌾 **Rendemen Otomatis:** Beras **{persentase_beras}%** | Dedak **{persentase_dedak}%**")
        berat_beras_kg = berat_gabah_kg * (persentase_beras / 100)
        estimasi_dedak_kg = berat_gabah_kg * (persentase_dedak / 100)

        pilihan_sosoh = st.selectbox("Derajat Sosoh Beras Hasil Giling:", ["Sosoh Sedang (Standar Pasar Lokal)", "Kurang Sosoh (Banyak Kulit Ari)", "Sosoh Sempurna / Putih Bersih (Premium)"])
        if "Kurang Sosoh" in pilihan_sosoh: pengaruh_harga_beras = -500
        elif "Sosoh Sedang" in pilihan_sosoh: pengaruh_harga_beras = 0
        else: pengaruh_harga_beras = 1000

        harga_beras_dasar = st.number_input("Harga Dasar Jual Beras Bersih (Rp/kg)", value=14500, step=100)
        harga_beras_final = harga_beras_dasar + pengaruh_harga_beras
        harga_dedak = st.number_input("Harga Jual Dedak (Rp/kg)", value=3500, step=100)

        tipe_ambil = st.radio("Metode Pengambilan Hasil Giling:", ["Pihak Pabrik yang Ambil (Tambah 1% ongkos)", "Diambil Sendiri (Ongkos standar 10% + Transport)"])
        persentase_ongkos = 0.11 if "Pihak Pabrik" in tipe_ambil else 0.10
        ongkos_giling = berat_beras_kg * persentase_ongkos
        beras_bersih_final = berat_beras_kg - ongkos_giling

        biaya_transport = st.number_input("Biaya Transportasi Pribadi (Rp)", value=50000, step=10000) if "Diambil Sendiri" in tipe_ambil else 0

        st.markdown("---")
        if st.button("Hitung Analisis Keuntungan Petani"):
            pendapatan_jual_gabah = berat_gabah_kg * harga_gabah_final
            pendapatan_beras = beras_bersih_final * harga_beras_final
            pendapatan_dedak = estimasi_dedak_kg * harga_dedak
            total_pengeluaran_olah = total_biaya_jemur + biaya_transport
            total_pendapatan_olah = pendapatan_beras + pendapatan_dedak - total_pengeluaran_olah
            selisih = total_pendapatan_olah - pendapatan_jual_gabah

            c1, c2 = st.columns(2)
            with c1: st.metric("Opsi Jual Gabah", f"Rp {pendapatan_jual_gabah:,.0f}")
            with c2: st.metric("Opsi Olah Beras", f"Rp {total_pendapatan_olah:,.0f}")

            st.markdown("---")
            if selisih > 0:
                st.success(f"**Rekomendasi:** Lebih menguntungkan **DIOLAH MENJADI BERAS** (Selisih profit: +Rp {selisih:,.0f}).")
            else:
                st.warning(f"**Rekomendasi:** Lebih menguntungkan **DIJUAL GABAH LANGSUNG** (Selisih rugi jika diolah: Rp {abs(selisih):,.0f}).")

            with st.expander("📋 Rincian Kalkulasi Transparan Petani", expanded=True):
                st.write(f"• **Gabah:** {berat_gabah_kg:,.0f} kg × Rp {harga_gabah_final:,} = Rp {pendapatan_jual_gabah:,.0f}")
                st.write(f"• **Beras Bersih:** {beras_bersih_final:,.1f} kg × Rp {harga_beras_final:,} = Rp {pendapatan_beras:,.0f}")
                st.write(f"• **Dedak:** {estimasi_dedak_kg:,.1f} kg × Rp {harga_dedak:,} = Rp {pendapatan_dedak:,.0f}")
                st.write(f"• **Total Biaya Pengolahan:** Rp {total_pengeluaran_olah:,}")

    # ==========================================
    # KONDISI 2: MODE PABRIK / PENGGILINGAN (RMU)
    # ==========================================
    elif st.session_state.pilihan_aktif == "pabrik":
        st.subheader("🏭 Mode Analisis Bisnis Pabrik Gabah / Rice Milling Unit (RMU)")
        
        berat_beli_ton = st.number_input("Pembelian Gabah Basah / Kering dari Petani (Ton)", value=10.0, min_value=0.5, step=0.5)
        berat_beli_kg = berat_beli_ton * 1000
        harga_beli_per_kg = st.number_input("Harga Beli Gabah dari Petani (Rp/kg)", value=6800, step=100)
        
        st.markdown("---")
        st.write("### 🚚 Logistik & Pengangkutan Gabah")
        diantar_agen = st.radio("Apakah gabah diantar oleh agen?", ["Iya", "Tidak"])
        
        biaya_transport_total = 0
        rincian_transport_teks = "Diantar agen (Tanpa biaya tambahan transport)"

        if diantar_agen == "Tidak":
            sewa_mobil = st.radio("Apakah anda sewa mobil?", ["Iya", "Tidak"])
            if sewa_mobil == "Iya":
                harga_sewa_mobil = st.number_input("Harga Sewa Mobil (Rp)", value=300000, step=50000)
                bayar_sopir = st.number_input("Bayar Sopir (Rp)", value=150000, step=25000)
                upah_kuli = st.number_input("Upah Kuli / Bongkar Muat (Rp)", value=100000, step=25000)
                persen_resiko = st.number_input("Persentase Tambahan Biaya Penanggulangan Risiko Perjalanan (%)", value=5.0, min_value=0.0, step=1.0)
                
                subtotal_logistik = harga_sewa_mobil + bayar_sopir + upah_kuli
                biaya_resiko = subtotal_logistik * (persen_resiko / 100)
                biaya_transport_total = subtotal_logistik + biaya_resiko
                
                rincian_transport_teks = f"Sewa Mobil: Rp {harga_sewa_mobil:,.0f} + Sopir: Rp {bayar_sopir:,.0f} + Kuli: Rp {upah_kuli:,.0f} + Risiko ({persen_resiko}%): Rp {biaya_resiko:,.0f}"
            else:
                upah_kuli_saja = st.number_input("Upah Kuli / Bongkar Muat (Rp)", value=100000, step=25000)
                biaya_transport_total = upah_kuli_saja
                rincian_transport_teks = f"Kendaraan Milik Sendiri, Upah Kuli: Rp {upah_kuli_saja:,.0f}"

        st.markdown("---")
        st.write("### ⚙️ Parameter Operasional Pabrik")
        kualitas_masuk = st.selectbox("Kualitas Rata-rata Gabah Masuk:", ["Standar Bagus", "Agak Basah / Banyak Kadar Air", "Banyak Bulir Hijau / Hampa"])
        
        if "Standar Bagus" in kualitas_masuk:
            rendemen_beras_pabrik, rendemen_dedak_pabrik = 64, 15
        elif "Agak Basah" in kualitas_masuk:
            rendemen_beras_pabrik, rendemen_dedak_pabrik = 60, 17
        else:
            rendemen_beras_pabrik, rendemen_dedak_pabrik = 53, 20

        st.info(f"📊 **Standar Pabrik Terdeteksi:** Rendemen Beras **{rendemen_beras_pabrik}%** | Dedak **{rendemen_dedak_pabrik}%**")

        biaya_jemur_pabrik = st.number_input("Biaya Pengeringan / Jemur Total (Rp)", value=500000, step=50000)
        biaya_giling_mesin = st.number_input("Biaya Operasional Mesin Giling & Listrik (Rp)", value=400000, step=50000)
        biaya_pekerja_upah = st.number_input("Total Upah Tenaga Kerja Borongan Pengolahan (Rp)", value=600000, step=50000)
        
        st.markdown("---")
        st.write("### 💰 Proyeksi Harga Jual Hasil Produksi Pabrik")
        harga_jual_beras_pabrik = st.number_input("Target Harga Jual Beras Grosir ke Pasar (Rp/kg)", value=13800, step=100)
        harga_jual_dedak_pabrik = st.number_input("Harga Jual Dedak / Menir Pabrik (Rp/kg)", value=3200, step=100)

        st.markdown("---")
        if st.button("Hitung Analisis Profitabilitas Pabrik"):
            modal_beli_gabah = berat_beli_kg * harga_beli_per_kg
            total_berat_beras_hasil = berat_beli_kg * (rendemen_beras_pabrik / 100)
            total_berat_dedak_hasil = berat_beli_kg * (rendemen_dedak_pabrik / 100)
            
            omzet_beras = total_berat_beras_hasil * harga_jual_beras_pabrik
            omzet_dedak = total_berat_dedak_hasil * harga_jual_dedak_pabrik
            total_omzet = omzet_beras + omzet_dedak
            
            total_biaya_operasional = biaya_jemur_pabrik + biaya_giling_mesin + biaya_pekerja_upah + biaya_transport_total
            total_modal_keseluruhan = modal_beli_gabah + total_biaya_operasional
            
            laba_bersih_pabrik = total_omzet - total_modal_keseluruhan
            margin_keuntungan = (laba_bersih_pabrik / total_modal_keseluruhan) * 100 if total_modal_keseluruhan > 0 else 0

            c1, c2, c3 = st.columns(3)
            with c1: st.metric("Total Modal Pabrik", f"Rp {total_modal_keseluruhan:,.0f}")
            with c2: st.metric("Total Omzet Penjualan", f"Rp {total_omzet:,.0f}")
            with c3: st.metric("Laba Bersih Pabrik", f"Rp {laba_bersih_pabrik:,.0f}")

            st.markdown("---")
            if laba_bersih_pabrik > 0:
                st.success(f"**Status Bisnis RMU:** **PROFITABLE / UNTUNG**. Margin keuntungan bersih mencapai **{margin_keuntungan:.2f}%** dari total modal.")
            else:
                st.error(f"**Status Bisnis RMU:** **MERUGI**. Operasional pabrik mengalami defisit sebesar Rp {abs(laba_bersih_pabrik):,.0f}.")

            with st.expander("📋 Laporan Keuangan & Kalkulasi Detail Pabrik", expanded=True):
                st.write(f"• **Pembelian Bahan Baku ({berat_beli_ton} Ton):** Rp {modal_beli_gabah:,.0f}")
                st.write(f"• **Biaya Logistik & Transportasi:** Rp {biaya_transport_total:,.0f} *({rincian_transport_teks})*")
                st.write(f"• **Akumulasi Biaya Operasional Lainnya (Jemur + Mesin + Upah Giling):** Rp {biaya_jemur_pabrik + biaya_giling_mesin + biaya_pekerja_upah:,.0f}")
                st.write(f"• **Produksi Beras ({rendemen_beras_pabrik}%):** {total_berat_beras_hasil:,.1f} kg × Rp {harga_jual_beras_pabrik:,} = Rp {omzet_beras:,.0f}")
                st.write(f"• **Produksi Dedak ({rendemen_dedak_pabrik}%):** {total_berat_dedak_hasil:,.1f} kg × Rp {harga_jual_dedak_pabrik:,} = Rp {omzet_dedak:,.0f}")
                st.markdown(f"**Formula Laba Bersih:** Total Omzet Penjualan - (Modal Pembelian + Total Biaya Operasional & Transport) = **Rp {laba_bersih_pabrik:,.0f}**")
