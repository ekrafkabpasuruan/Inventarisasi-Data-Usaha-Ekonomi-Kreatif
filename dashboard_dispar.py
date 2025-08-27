import streamlit as st
import pandas as pd
import altair as alt
import requests
import io
import re
import streamlit.components.v1 as components
import json

# --- KONFIGURASI HALAMAN ---
st.set_page_config(
    page_title="DISPAR KAB. PASURUAN",
    layout="wide",
    page_icon="https://i.pinimg.com/736x/34/e4/ba/34e4baa62df5cfe22ccb43f43567978d.jpg"
)

# --- STYLING CSS KUSTOM ---
st.markdown("""
    <style>
    .stApp {
        background-color: #f0fdf4;
    }
    .main {
        background-color: #f9fff9;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    }

    /* Judul */
    h1, h2, h3, h4 {
        color: #00695c;
        font-family: 'Segoe UI', sans-serif;
        font-weight: 600;
    }

    /* Subheader dan Keterangan */
    .st-emotion-cache-10qnfpr {
        color: #004d40;
        font-weight: 500;
    }
    .st-emotion-cache-nahz7x {
        color: #333333;
        font-style: italic;
    }

    /* Label Selectbox, FileUploader, dan TextInput */
    .stSelectbox label, .stFileUploader label, .stTextInput label {
        font-weight: 600;
        color: #004d40;
    }

    /* Teks Checkbox */
    .stCheckbox > div {
        font-weight: 400;
        color: #004d40;
    }

    /* Padding kontainer blok */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    /* Styling metrik */
    [data-testid="stMetric"] {
        background-color: #e0f2f1;
        border-radius: 8px;
        padding: 1rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        text-align: center;
    }
    [data-testid="stMetric"] > div > div:nth-child(1) {
        font-size: 1.1em;
        color: #004d40;
        font-weight: 600;
    }
    [data-testid="stMetric"] > div > div:nth-child(3) {
        font-size: 2.5em;
        color: #00695c;
        font-weight: 700;
    }

    /* Styling expander */
    .streamlit-expanderHeader {
        background-color: #b2dfdb;
        color: #004d40;
        font-weight: 600;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        margin-bottom: 0.5rem;
    }
    .streamlit-expanderContent {
        background-color: #e0f2f1;
        border-bottom-left-radius: 5px;
        border-bottom-right-radius: 5px;
        padding: 1rem;
    }

    /* Styling dataframe */
    .stDataFrame {
        border: 1px solid #b2dfdb;
        border-radius: 5px;
        overflow: hidden;
    }

    .st-emotion-cache-1c7y2kd p {
        background-color: #e8f5e9;
        color: #2e7d32;
        border-left: 5px solid #66bb6a;
        padding: 10px;
        border-radius: 5px;
    }
    .st-emotion-cache-1ldn2y5 p {
        background-color: #fffde7;
        color: #ffb300;
        border-left: 5px solid #ffd54f;
        padding: 10px;
        border-radius: 5px;
    }
    .st-emotion-cache-12fmj2r p {
        background-color: #ffebee;
        color: #d32f2f;
        border-left: 5px solid #ef5350;
        padding: 10px;
        border-radius: 5px;
    }
    
    /* Tambahkan CSS responsif untuk gambar */
    .logo-container {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
    }
    .logo-container img {
        max-width: 150px; /* Batasi lebar maksimum logo */
        height: auto;
    }
    
    /* Media query untuk layar kecil */
    @media (max-width: 768px) {
        .logo-container img {
            max-width: 100px;
        }
    }

    /* Tambahkan CSS responsif untuk video */
    .video-container {
        position: relative;
        width: 100%;
        padding-bottom: 56.25%; /* Rasio aspek 16:9 */
        height: 0;
        overflow: hidden;
        margin: auto; /* Pusatkan video */
    }
    .video-container iframe {
        position: absolute;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
    }
    
    /* Keterangan di footer agar responsif */
    .st-emotion-cache-17lsv9n {
        text-align: center !important;
    }
    
    /* Styling khusus untuk bagian pendaftaran */
    .registration-section {
        background-color: #e8f5e9;
        padding: 2rem;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        border: 1px solid #c8e6c9;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        font-weight: bold;
    }
    .form-title {
        text-align: center;
        margin-bottom: 1.5rem;
    }
    </style>
""", unsafe_allow_html=True)

# --- BAGIAN HEADER ---
col1, col2 = st.columns([0.2, 0.8])
with col1:
    st.markdown("""
        <div class="logo-container">
            <img src="https://i.pinimg.com/736x/34/e4/ba/34e4baa62df5cfe22ccb43f43567978d.jpg" alt="Logo DISPAR KAB. PASURUAN">
        </div>
    """, unsafe_allow_html=True)
with col2:
    st.title("DINAS PARIWISATA KAB. PASURUAN")
    st.subheader("Inventarisasi Data Usaha Ekonomi Kreatif")
    st.caption("✨ Visualisasi & Pemetaan Usaha Masyarakat di Kabupaten Pasuruan")

st.markdown("---") 

file_ids = {
    '1kUQIxE6-beZulQLv-ZwzbujIdhjxtT_B': 'KULINER',
    '1FQAo6shJhvTCMCfK57W-xi4yqcudcgNz': 'MUSIK',
    '1oP6IwzDosaP4qofPpDGiUpgBumcHcofY': 'PENERBITAN',
    '18CbhWLf1tyUfNoLBTHLqdan1uNJi1aBw': 'PENGEMBANG PERMAINAN',
    '1cB9xFsrg_9bgHo4YK1J_OxdjjpdyULM_': 'PERIKLANAN',
    '1szarAEXUuvA-gvd1XT8quBDjTBCHhs6W': 'SENI PERTUNJUKAN',
    '1sEWP3mBIfuzQSa8f_XqVx_FJw2u6Mal6': 'SENI RUPA',
    '1QnBGnU_vRWBQN3_zjpLmw073cqQrUdkc': 'TELEVISI & RADIO',
    '1d1slXI7e92x2uBQbS477UPW3kmhSZGmY': 'ARSITEKTUR',
    '1004nMzfSA_2u0tsHCT0vRfR2DsLRDscq': 'DESAIN INTERIOR',
    '1UIpnYknfYsay_y3_BIdM0ST4j8N2eW0V': 'DESAIN KOMUNIKASI VISUAL',
    '1bED3JEIZPF5E1kMT7YJmgJHWHazlrc1r': 'DESAIN PRODUK',
    '1F61lN4gust55u5QwfStbb7hmO7HciAM4': 'FASHION',
    '18WffL9Z4s9IQIt325K02q4Vkc-KnoIpV': 'FILM, ANIMASI, VIDEO',
    '1upaDVhBb6pI72YkrbvPLXKopAO4mUBu4': 'FOTOGRAFI',
    '1_0wyqKjvc10OvC1elQchOvBeeLXyNgl9': 'KRIYA',
    '1OfkA--rGJmyZqUf8Qhhw_EwjJDFV5oL1': 'APLIKASI',
}

# --- FUNGSI EKSTRAKSI & PEMUATAN DATA ---
def ekstrak_kecamatan(alamat):
    """Mengekstrak nama kecamatan dari string alamat."""
    if isinstance(alamat, str):
        match = re.search(r'\bKec(?:amatan)?\.?\s+([A-Za-z\s]+?)(?:,|\.|$)', alamat, re.IGNORECASE)
        if match:
            return match.group(1).strip().upper()
    return "TIDAK DIKETAHUI"

@st.cache_data(show_spinner=True)
def load_data_from_drive(file_id, subsektor):
    """Memuat file CSV dari Google Drive dan memprosesnya."""
    url = f"https://drive.google.com/uc?export=download&id={file_id}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status() # Menimbulkan HTTPError untuk respons yang buruk (4xx atau 5xx)
    except requests.exceptions.RequestException as e:
        st.error(f"Koneksi gagal saat mengunduh data untuk subsektor **{subsektor}**: {e}")
        return pd.DataFrame() # Mengembalikan DataFrame kosong jika gagal

    # Membaca CSV, melewati baris awal (asumsi metadata/header)
    df = pd.read_csv(io.StringIO(response.content.decode('utf-8')), skiprows=3)

    current_cols = df.columns.tolist()
    
    # Mendefinisikan kolom "Unnamed" yang diharapkan dan nama baru yang diinginkan
    expected_unnamed_cols = {
        'Unnamed: 0': "NAMA USAHA",
        'Unnamed: 1': "ALAMAT",
        'Unnamed: 2': "KONTAK",
        'Unnamed: 4': "TENAGA KERJA LAKI",
        'Unnamed: 5': "TENAGA KERJA PEREMPUAN",
        'Unnamed: 6': "TENAGA KERJA TOTAL",
        'Unnamed: 15': "SUBSEKTOR",
        'Unnamed: 16': "JENIS USAHA"
    }

    rename_mapping = {}
    for original, new in expected_unnamed_cols.items():
        if original in current_cols:
            rename_mapping[original] = new
    
    df.rename(columns=rename_mapping, inplace=True)

    # Memastikan kolom yang diperlukan ada sebelum memilih
    required_cols = ["NAMA USAHA", "ALAMAT", "SUBSEKTOR", "JENIS USAHA"]
    if 'TENAGA KERJA TOTAL' in df.columns:
        required_cols.append('TENAGA KERJA TOTAL')

    # Memfilter kolom untuk hanya menyertakan yang ada dan diperlukan
    df = df[[col for col in required_cols if col in df.columns]].copy()
    
    df['SUBSEKTOR'] = subsektor 

    # Mengekstrak kecamatan dari 'ALAMAT'
    if 'ALAMAT' in df.columns:
        df['KECAMATAN'] = df['ALAMAT'].apply(ekstrak_kecamatan)
    else:
        df['KECAMATAN'] = 'TIDAK DIKETAHUI'

    return df

# --- MEMUAT SEMUA DATA ---
df_list = []
with st.spinner("Memuat data usaha ekonomi kreatif..."):
    for file_id, subsektor in file_ids.items():
        df = load_data_from_drive(file_id, subsektor)
        if not df.empty:
            df_list.append(df)

if not df_list:
    st.error("❌ Gagal memuat data utama. Mohon periksa kembali koneksi internet atau File ID Google Drive Anda.")
    st.stop()

df_all = pd.concat(df_list, ignore_index=True)

# --- PEMBERSIHAN DATA ---
# Menghapus baris di mana 'NAMA USAHA' atau 'ALAMAT' adalah nilai placeholder atau null
if 'NAMA USAHA' in df_all.columns and 'ALAMAT' in df_all.columns:
    rows_to_remove = (
        (df_all['NAMA USAHA'].astype(str).str.upper().isin(['NAMA USAHA', 'NONE', 'NAN', ''])) |
        (df_all['ALAMAT'].astype(str).str.upper().isin(['ALAMAT', 'NONE', 'NAN', ''])) |
        (df_all['NAMA USAHA'].isnull()) |
        (df_all['ALAMAT'].isnull())
    )
    df_all = df_all[~rows_to_remove].copy()
    df_all.reset_index(drop=True, inplace=True)
else:
    st.warning("Kolom 'NAMA USAHA' atau 'ALAMAT' tidak ditemukan, sehingga tidak dapat membersihkan baris placeholder.")

# --- VALIDASI AWAL ---
if df_all.empty:
    st.error("❗ Tidak ada data yang valid ditemukan setelah pembersihan. Pastikan format file benar.")
    st.stop()

if 'KECAMATAN' not in df_all.columns or df_all['KECAMATAN'].isnull().all():
    st.error("Kolom 'KECAMATAN' tidak ditemukan atau kosong setelah pemrosesan data. Pemetaan tidak dapat dilakukan.")
    st.stop()
if 'SUBSEKTOR' not in df_all.columns or df_all['SUBSEKTOR'].isnull().all():
    st.error("Kolom 'SUBSEKTOR' tidak ditemukan atau kosong setelah pemrosesan data. Filter tidak dapat digunakan.")
    st.stop()

# --- TATA LETAK FILTER DAN METRIK ---
st.header("📊 Analisis Data Usaha Kreatif")

filter_col1, filter_col2 = st.columns(2)

with filter_col1:
    all_kecamatan_options = sorted(df_all['KECAMATAN'].dropna().unique().tolist())
    selected_kecamatan = st.selectbox(
        "📍 Pilih Kecamatan",
        options=['Semua Kecamatan'] + all_kecamatan_options,
        help="Pilih kecamatan untuk memfilter data dan grafik."
    )

with filter_col2:
    all_subsektor_options = sorted(df_all['SUBSEKTOR'].unique().tolist())
    selected_subsektor = st.selectbox(
        "🎨 Pilih Subsektor",
        options=['(Semua Subsektor)'] + all_subsektor_options,
        help="Pilih subsektor untuk memfilter data dan grafik."
    )

# --- FILTER DATA BERDASARKAN PILIHAN ---
filtered_df = df_all.copy()

if selected_kecamatan != 'Semua Kecamatan':
    filtered_df = filtered_df[filtered_df['KECAMATAN'] == selected_kecamatan]

if selected_subsektor != '(Semua Subsektor)':
    filtered_df = filtered_df[filtered_df['SUBSEKTOR'] == selected_subsektor]

st.markdown("---")

# --- MENAMPILKAN METRIK ---
if filtered_df.empty:
    st.warning("⚠️ Tidak ada data yang cocok dengan pilihan filter Anda. Coba pilih filter lain.")
else:
    st.subheader("Ringkasan Data Terfilter")
    # Menggunakan 3 kolom untuk menampilkan metrik
    metric_col1, metric_col2, metric_col3 = st.columns(3)
    
    with metric_col1:
        total_usaha_filtered = len(filtered_df)
        st.metric("Total Usaha Terdata", f"{total_usaha_filtered:,}")
    
    with metric_col2:
        total_tenaga_kerja_filtered = 0
        if 'TENAGA KERJA TOTAL' in filtered_df.columns:
            total_tenaga_kerja_filtered = pd.to_numeric(filtered_df["TENAGA KERJA TOTAL"], errors="coerce").fillna(0).sum()
        else:
            st.info("ℹ️ Kolom 'TENAGA KERJA TOTAL' tidak tersedia untuk perhitungan tenaga kerja.")
        st.metric("Total Tenaga Kerja", f"{int(total_tenaga_kerja_filtered):,} orang")
    
    # Tambahkan metrik untuk subsektor aktif
    with metric_col3:
        st.metric("Subsektor Aktif", selected_subsektor)


    st.markdown("---")

    # --- MENAMPILKAN DATA TERFILTER ---
    with st.expander(f"📋 **Lihat Detail Data Usaha Ekonomi Kreatif**"):
        st.dataframe(
            filtered_df[['NAMA USAHA', 'ALAMAT', 'KECAMATAN', 'SUBSEKTOR', 'JENIS USAHA', 'TENAGA KERJA TOTAL']].reset_index(drop=True),
            use_container_width=True,
            height=300
        )

    st.markdown("---")

    # --- JENIS USAHA PALING DOMINAN ---
    st.subheader("🏆 Jenis Usaha Paling Dominan")
    if 'JENIS USAHA' in filtered_df.columns and not filtered_df['JENIS USAHA'].empty:
        dominan_df = (
            filtered_df.groupby("JENIS USAHA")
            .size()
            .reset_index(name="JUMLAH")
            .sort_values(by="JUMLAH", ascending=False)
        )

        if not dominan_df.empty:
            jenis_terbanyak = dominan_df.iloc[0]
            st.success(
                f"Jenis usaha paling dominan di **{selected_kecamatan if selected_kecamatan != 'Semua Kecamatan' else 'Kabupaten Pasuruan'}** "
                f"(Subsektor: {selected_subsektor if selected_subsektor != '(Semua Subsektor)' else 'Semua'}) adalah "
                f"**{jenis_terbanyak['JENIS USAHA']}** dengan jumlah **{jenis_terbanyak['JUMLAH']} usaha**."
            )
            
            with st.expander("📊 Grafik Distribusi Jenis Usaha"):
                bars = alt.Chart(dominan_df.head(10)).mark_bar().encode(
                    x=alt.X('JUMLAH:Q', title='Jumlah Usaha'),
                    y=alt.Y('JENIS USAHA:N', sort='-x', title='Jenis Usaha'),
                    tooltip=['JENIS USAHA', 'JUMLAH'],
                    color=alt.value("#26a69a")
                )
                text = bars.mark_text(
                    align='right',
                    baseline='middle',
                    dx=-1
                ).encode(
                    text=alt.Text('JUMLAH:Q'),
                    color=alt.value('white')
                )
                chart_jenis_usaha = (bars + text).properties(
                    title=f"Top 10 Jenis Usaha di {selected_kecamatan} ({selected_subsektor})"
                ).interactive()
                st.altair_chart(chart_jenis_usaha, use_container_width=True)

        else:
            st.info("ℹ️ Kolom 'JENIS USAHA' tidak ditemukan atau kosong. Fitur ini tidak dapat ditampilkan.")
    
    st.markdown("---")

    # --- GRAFIK DISTRIBUSI ---
    st.subheader("📈 Distribusi Usaha Berdasarkan Wilayah dan Sektor")

    chart_col1, chart_col2 = st.columns(2)

    with chart_col1:
        if selected_subsektor == '(Semua Subsektor)' and not filtered_df.empty:
            st.markdown(f"#### Jumlah Usaha per Subsektor di {selected_kecamatan}")
            subsektor_counts = filtered_df['SUBSEKTOR'].value_counts().reset_index()
            subsektor_counts.columns = ['Subsektor', 'Jumlah Usaha']
            
            total_usaha_subsektor = subsektor_counts['Jumlah Usaha'].sum()
            subsektor_counts['Persentase'] = (subsektor_counts['Jumlah Usaha'] / total_usaha_subsektor)
            
            subsektor_counts['Subsektor & Persen'] = subsektor_counts.apply(
                lambda row: f"{row['Subsektor']} ({row['Persentase']:.1%})", axis=1
            )

            pie_subsektor = alt.Chart(subsektor_counts).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Jumlah Usaha:Q", stack=True),
                color=alt.Color(
                    "Subsektor & Persen:N",
                    title="Subsektor",
                    legend=alt.Legend(orient="bottom", columns=2, labelColor="black")
                ),
                order=alt.Order("Persentase", sort="ascending"),
                tooltip=[
                    alt.Tooltip("Subsektor", title="Subsektor"),
                    alt.Tooltip("Jumlah Usaha", title="Jumlah Usaha"),
                    alt.Tooltip("Persentase", format=".1%", title="Persentase")
                ]
            ).properties(
                title=f"Distribusi Usaha Berdasarkan Subsektor di {selected_kecamatan}"
            ).interactive()
            
            st.altair_chart(pie_subsektor, use_container_width=True)
            
        elif selected_subsektor != '(Semua Subsektor)':
            st.info(f"Untuk melihat grafik 'Jumlah Usaha per Subsektor', pilih '**(Semua Subsektor)**' di filter subsektor.")


    with chart_col2:
        if selected_kecamatan == 'Semua Kecamatan' and not filtered_df.empty:
            st.markdown(f"#### Jumlah Usaha per Kecamatan untuk Subsektor {selected_subsektor}")
            kecamatan_counts = filtered_df['KECAMATAN'].value_counts().reset_index()
            kecamatan_counts.columns = ['Kecamatan', 'Jumlah Usaha']
            
            total_usaha_kecamatan = kecamatan_counts['Jumlah Usaha'].sum()
            kecamatan_counts['Persentase'] = (kecamatan_counts['Jumlah Usaha'] / total_usaha_kecamatan)

            kecamatan_counts['Kecamatan & Persen'] = kecamatan_counts.apply(
                lambda row: f"{row['Kecamatan']} ({row['Persentase']:.1%})", axis=1
            )

            pie_kecamatan = alt.Chart(kecamatan_counts).mark_arc(outerRadius=120).encode(
                theta=alt.Theta("Jumlah Usaha:Q", stack=True),
                color=alt.Color(
                    "Kecamatan & Persen:N",
                    title="Kecamatan",
                    legend=alt.Legend(orient="bottom", columns=2, titleLimit=300, symbolLimit=50, labelColor="black")
                ),
                order=alt.Order("Persentase", sort="ascending"),
                tooltip=[
                    alt.Tooltip("Kecamatan", title="Kecamatan"),
                    alt.Tooltip("Jumlah Usaha", title="Jumlah Usaha"),
                    alt.Tooltip("Persentase", format=".1%", title="Persentase")
                ]
            ).properties(
                title=f"Distribusi Usaha Berdasarkan Kecamatan untuk Subsektor {selected_subsektor}"
            ).interactive()
            
            st.altair_chart(pie_kecamatan, use_container_width=True)
            
        elif selected_kecamatan != 'Semua Kecamatan':
            st.info(f"Untuk melihat grafik 'Jumlah Usaha per Kecamatan', pilih '**Semua Kecamatan**' di filter kecamatan.")


# --- BAGIAN VIDEO INTERAKTIF (GOOGLE DRIVE) ---
st.markdown("---")
st.subheader("📽️ Galeri Profil Ekonomi Kreatif")

# Daftar video Google Drive yang dikelompokkan berdasarkan subsektor
video_list = {
    "Pilih Subsektor...": None,
    "MONEV": {
        "Monev 29-juli-2025": "https://drive.google.com/file/d/1o_LHmFlx5uhAHp3iII7FJ5xH-T4rbrDQ/preview",
        "Monev 13-Agustus-2025": "https://drive.google.com/file/d/1pIxeDrdSXhVJKkuYKX3J7XdlcPCPQ_rI/preview",
    },
    "APLIKASI": {
    },
    "ARSITEKTUR": {
        "Arda KaryaWijaya" : "https://drive.google.com/file/d/1yQ9xXU1xcUext8Jh7zFC9LEVKN0KSxOm/preview"
    },
    "DESAIN INTERIOR": {
    },
    "DESAIN KOMUNIKASI VISUAL": {
    },
    "DESAIN PRODUK": {
    },
    "FASHION": {
        "Faiza Bordir Bangil" : "https://drive.google.com/file/d/1-eS_PSwkxeVQkLClTafgZRVGG-Iqzodj/preview"
    },
    "FILM, ANIMASI, VIDEO": {
    },
    "FOTOGRAFI": {
    },
    "KRIYA": {
    },
    "KULINER": {
        "Bakpia Mami Pusat" : "https://drive.google.com/file/d/1Fi5zSclj1MWL9sEMLYHF2bSZBTtZzwJ5/preview"
    },
    "MUSIK": {
    },
    "PENERBITAN": {
    },
    "PENGEMBANG PERMAINAN": {
    },
    "PERIKLANAN": {
    },
    "SENI PERTUNJUKAN": {
    },
    "SENI RUPA": {
        "Dian Art Studio" : "https://drive.google.com/file/d/18II-HJVdLf5m-uId7WJm3HNMTTfkYCCP/preview"
    },
    "TELEVISI & RADIO": {
    },
}

# Menampilkan selectbox video
selected_subsektor_video = st.selectbox(
    "📺 Pilih Subsektor:",
    options=list(video_list.keys())
)

# --- LOGIKA KOREKSI ---
# Cek apakah pengguna telah memilih subsektor selain opsi default
if selected_subsektor_video and selected_subsektor_video != "Pilih Subsektor...":
    # Cek apakah subsektor yang dipilih memiliki daftar video
    if video_list[selected_subsektor_video]:
        video_options = list(video_list[selected_subsektor_video].keys())
        selected_video_title = st.selectbox(
            f"Pilih profile untuk subsektor {selected_subsektor_video}:",
            options=video_options
        )

        # Mengambil URL dari video yang dipilih
        selected_url = video_list[selected_subsektor_video][selected_video_title]
        
        st.markdown(f"#### {selected_video_title}")
        # Menggunakan st.components.v1.html dengan kontainer responsif
        components.html(f"""
            <div class="video-container">
                <iframe src="{selected_url}" frameborder="0" allowfullscreen></iframe>
            </div>
        """, height=185)
        st.caption(f"Ini adalah profil tentang {selected_video_title}.")
    else:
        # Tampilkan pesan jika subsektor tidak memiliki video
        st.info(f"Tidak ada profile yang tersedia untuk subsektor **{selected_subsektor_video}**.")

else:
    # Tampilkan pesan default saat belum ada subsektor yang dipilih
    st.info("Silakan pilih subsektor untuk melihat daftar profile yang tersedia.")

st.markdown("---")

# --- BAGIAN REGISTRASI INTERAKTIF BARU ---
st.markdown("""
    <div class="registration-section">
        <div class="form-title">
            <h3>Punya Usaha Kreatif di Kabupaten Pasuruan?</h3>
            <p>Ayo daftarkan usaha Anda dan bergabunglah dengan ekosistem ekonomi kreatif kami!</p>
        </div>
    </div>
""", unsafe_allow_html=True)

# Inisialisasi session state jika belum ada
if 'show_form' not in st.session_state:
    st.session_state['show_form'] = False

# Tombol untuk menampilkan/menyembunyikan formulir
if st.button('Daftar Usaha Ekonomi Kreatif Sekarang!', use_container_width=True):
    st.session_state['show_form'] = not st.session_state['show_form']

if st.session_state['show_form']:
    st.markdown("---")
    st.subheader("📝 Formulir Pendataan")

    # URL API Google Apps Script
    # GANTI URL INI DENGAN URL WEB APP GOOGLE APPS SCRIPT ANDA YANG SUDAH DI-DEPLOY
    form_url = "https://script.google.com/macros/s/AKfycbz7EburtlhxORmFc4fqCNW-oTyjhs1mf48FL5uXLTV0YSh8ZzZ9QTWyg62Me86TRmQ7/exec"

    with st.form(key='registration_form'):
        st.markdown("**Informasi Dasar Usaha**")
        col_form1, col_form2 = st.columns(2)
        with col_form1:
            nama_usaha = st.text_input("Nama Usaha", key="nama_usaha", placeholder="Contoh: Sanggar Batik Pasuruan")
            alamat = st.text_input("Alamat Lengkap", help="Sertakan nama kecamatan dan kabupaten/kota", key="alamat", placeholder="Contoh: Jl. Diponegoro No. 12, Kec. Prigen, Kab. Pasuruan")
        with col_form2:
            kontak = st.text_input("Nomor Kontak / WA", help="Contoh: 081234567890", key="kontak", placeholder="08XX-XXXX-XXXX")
            jenis_usaha = st.text_input("Jenis Usaha", help="Contoh: Kerajinan Anyaman, Jasa Desain Grafis", key="jenis_usaha", placeholder="Kerajinan Tangan, Jasa Desain, dsb.")

        st.markdown("---")
        st.markdown("**Detail Kategori & Legalitas**")
        col_form3, col_form4, col_form5 = st.columns(3)
        with col_form3:
            # Dropdown untuk Subsektor
            subsektor_list = sorted(list(file_ids.values()))
            subsektor = st.selectbox(
                "Subsektor",
                options=["-- Pilih Subsektor --"] + subsektor_list,
                key="subsektor"
            )
        with col_form4:
            tenaga_kerja_total = st.number_input("Total Tenaga Kerja", min_value=0, key="tenaga_kerja", help="Jumlah total karyawan (termasuk pemilik).")
        with col_form5:
            # Kolom untuk NIB dan HAKI
            nib = st.text_input("Nomor Induk Berusaha (NIB)", key="nib", placeholder="Contoh: 1234567890")
            sertifikat_haki = st.selectbox(
                "Sertifikat HAKI",
                options=["-- Pilih Opsi --", "Punya", "Tidak Punya"],
                key="sertifikat_haki"
            )
        
        st.markdown("---")
        submit_button = st.form_submit_button(label='🚀 Kirim Data ', use_container_width=True)

        if submit_button:
            # Cek validasi sederhana
            if not nama_usaha or not alamat or subsektor == "-- Pilih Subsektor --":
                st.error("⚠️ Harap lengkapi semua data dengan benar. Pastikan Nama Usaha, Alamat, dan Subsektor terisi.")
            else:
                data = {
                    'nama_usaha': str(nama_usaha),
                    'alamat': str(alamat),
                    'kontak': str(kontak),
                    'jenis_usaha': str(jenis_usaha),
                    'subsektor': str(subsektor),
                    'tenaga_kerja_total': str(tenaga_kerja_total),
                    'nib': str(nib),
                    'sertifikat_haki': str(sertifikat_haki)
                }
                try:
                    response = requests.post(form_url, data=data, timeout=10)
                    if response.status_code == 200:
                        st.success("✅ Pendaftaran berhasil! Data Anda telah terkirim.")
                        # Sembunyikan formulir setelah pengiriman berhasil
                        st.session_state['show_form'] = False
                        # Menghapus inputan formulir
                        for key in st.session_state:
                            if key in ['nama_usaha', 'alamat', 'kontak', 'jenis_usaha', 'subsektor', 'tenaga_kerja', 'nib', 'sertifikat_haki']:
                                del st.session_state[key]
                        st.rerun() # Menggunakan st.rerun() yang sudah dikoreksi
                    else:
                        st.error("❌ Pendaftaran gagal. Coba lagi atau periksa konfigurasi API Anda.")
                except requests.exceptions.RequestException as e:
                    st.error(f"Terjadi kesalahan koneksi: {e}")

st.markdown("---")
st.markdown("Aplikasi ini dikembangkan oleh Dinas Pariwisata Kabupaten Pasuruan untuk mempromosikan dan memetakan Usaha Ekonomi Kreatif di wilayah Kabupaten Pasuruan.")









