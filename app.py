import streamlit as st
import pandas as pd
import itertools
import time
from datetime import datetime

# ==========================================
# 1. KONFIGURASI & TEMA DASHBOARD
# ==========================================
st.set_page_config(
    page_title="Library Intelligence",
    page_icon="🧠",
    layout="wide"
)

# Custom CSS untuk UI "Enterprise"
st.markdown("""
<style>
    .stApp { background-color: #0b0f19 !important; color: #e2e8f0 !important; }
    
    /* Efek Kartu Glassmorphism */
    .premium-card {
        background: rgba(23, 32, 48, 0.8);
        border: 1px solid rgba(59, 130, 246, 0.2);
        padding: 25px;
        border-radius: 18px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
        margin-bottom: 25px;
    }

    .main-title {
        background: linear-gradient(135deg, #60a5fa, #c084fc);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 800; font-size: 42px;
        letter-spacing: -1px;
    }

    /* Indikator Logika */
    .indicator {
        height: 12px; width: 12px; border-radius: 50%;
        display: inline-block; margin-right: 8px;
    }
    .status-on { background-color: #10b981; box-shadow: 0 0 10px #10b981; }
    .status-off { background-color: #ef4444; box-shadow: 0 0 10px #ef4444; }

    /* Hasil Banner */
    .result-box {
        padding: 25px; border-radius: 15px; text-align: center;
        font-size: 1.3rem; font-weight: 700; border: 2px solid;
    }
    .success-res { background: rgba(16, 185, 129, 0.1); color: #34d399; border-color: #059669; }
    .danger-res { background: rgba(239, 68, 68, 0.1); color: #f87171; border-color: #dc2626; }
</style>
""", unsafe_allow_html=True)

# Inisialisasi Riwayat (Session State)
if 'history' not in st.session_state:
    st.session_state.history = []

# ==========================================
# 2. SIDEBAR (PANEL KONTROL PETUGAS)
# ==========================================
with st.sidebar:
    st.markdown("<h2 class='main-title'>DASHBOARD</h2>", unsafe_allow_html=True)
    st.write("Sistem Keputusan Sirkulasi")
    st.divider()
    
    with st.container():
        st.markdown("### 📝 Input Parameter")
        nama = st.text_input("Nama Peminjam", "Rizky Ramadhan")
        buku = st.text_input("Judul Koleksi", "Logika Informatika")
        
        st.markdown("---")
        # Variabel Proposisi
        A = st.toggle("A: Keanggotaan Aktif", value=True)
        B = st.toggle("B: Ketersediaan Buku", value=True)
        C = st.toggle("C: Bebas Denda", value=True)
        D = st.toggle("D: Dispensasi Khusus", value=False)
        R = st.toggle("R: Kategori Referensi", value=False)

# ==========================================
# 3. LOGIC ENGINE (ARITMETIKA PROPOSISI)
# ==========================================
# Ekspresi Formal: (A ∧ B) ∧ (C ∨ D) ∧ ¬R
is_authorized = (A and B) and (C or D)
final_decision = is_authorized and not R

# ==========================================
# 4. MAIN INTERFACE
# ==========================================
st.markdown("<h1 class='main-title'>Sistem Keputusan Sirkulasi Perpustakaan</h1>", unsafe_allow_html=True)

# Baris Metrik Real-time
c1, c2, c3, c4 = st.columns(4)
c1.metric("Status Anggota", "AKTIF" if A else "NON-AKTIF")
c2.metric("Kelayakan Fisik", "TERSEDIA" if B else "KOSONG")
c3.metric("Status Finansial", "CLEAR" if C else "DENDA")
c4.metric("Kategori Buku", "UMUM" if not R else "REFERENSI")

col_main, col_side = st.columns([1.8, 1])

with col_main:
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("🔮 Engine Validasi Proposisional")
    
    # Visualisasi Gerbang Aktif
    cols = st.columns(5)
    labels = ["A", "B", "C", "D", "R"]
    states = [A, B, C, D, R]
    for i, col in enumerate(cols):
        status_class = "status-on" if states[i] else "status-off"
        col.markdown(f"<div class='indicator {status_class}'></div> *{labels[i]}*", unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    
    if st.button("JALANKAN ANALISIS SISTEM", use_container_width=True):
        st.toast("Mengevaluasi variabel...", icon="🧠")
        time.sleep(0.5)
        
        # Simpan ke riwayat
        status_txt = "DISETUJUI" if final_decision else "DITOLAK"
        st.session_state.history.append({
            "Waktu": datetime.now().strftime("%H:%M:%S"),
            "Peminjam": nama,
            "Buku": buku,
            "Keputusan": status_txt
        })

        if final_decision:
            st.markdown(f"<div class='result-box success-res'>✅ KEPUTUSAN: PEMINJAMAN DISETUJUI<br><small>Kriteria logika terpenuhi untuk {nama}</small></div>", unsafe_allow_html=True)
            st.balloons()
        else:
            st.markdown(f"<div class='result-box danger-res'>❌ KEPUTUSAN: PEMINJAMAN DITOLAK<br><small>Pelanggaran pada variabel proposisi terdeteksi.</small></div>", unsafe_allow_html=True)
            
            # Diagnostic Logic
            if R: st.warning("*Alasan:* Buku kategori 'Referensi' (R) memicu gerbang NOT.")
            elif not (A and B): st.error("*Alasan:* Kegagalan syarat mutlak pada gerbang AND (A atau B bernilai False).")
            else: st.info("*Alasan:* Masalah administrasi denda (C) tanpa dispensasi (D).")
    
    st.markdown("</div>", unsafe_allow_html=True)

    # Tabel Riwayat (Audit Trail)
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("📜 Log Aktivitas Sesi")
    if st.session_state.history:
        st.table(pd.DataFrame(st.session_state.history).tail(5))
    else:
        st.caption("Belum ada aktivitas validasi.")
    st.markdown("</div>", unsafe_allow_html=True)

with col_side:
    # Logic Map
    st.markdown("<div class='premium-card'>", unsafe_allow_html=True)
    st.subheader("📐 Arsitektur Logika")
    st.latex(r"F = ((A \land B) \land (C \lor D)) \land \neg R")
    
    
    
    st.markdown("""
    *Matriks Operasi:*
    1.  *Tahap I*: Konjungsi Mutlak $(A \land B)$.
    2.  *Tahap II*: Disjungsi Inklusif $(C \lor D)$.
    3.  *Tahap III*: Negasi Filter $(\dots \land \neg R)$.
    """)
    st.markdown("</div>", unsafe_allow_html=True)

    # Truth Table Explorer
    with st.expander("🔍 Explorer Tabel Kebenaran"):
        st.caption("Sampel 8 kombinasi dasar:")
        data = []
        for a, b, c in itertools.product([1, 0], repeat=3):
            res = "✓" if (a and b and c) else "✗"
            data.append([a, b, c, res])
        st.dataframe(pd.DataFrame(data, columns=["A", "B", "C", "F"]), use_container_width=True)

# Footer
st.markdown("<p style='text-align:center; color:#4b5563; font-size:12px;'>Library Intelligence System | Tugas Besar Logika Informatika 2026</p>", unsafe_allow_html=True)