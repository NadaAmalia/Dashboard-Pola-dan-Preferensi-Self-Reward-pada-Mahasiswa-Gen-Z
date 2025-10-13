import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# SETUP DASHBOARD
# =========================
st.title("🎁 Pola dan Preferensi Self-Reward Pada Mahasiswa Gen Z")
st.write("Analisis sederhana terhadap data pola reward mahasiswa berdasarkan survei.")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data_prep_final.csv")
    return df

df = load_data()

# =========================
# DATA PREVIEW
# =========================
with st.expander("🔍 Lihat Data (5 Baris Pertama)"):
    st.dataframe(df.head())

# =========================
# RINGKASAN STATISTIK
# =========================
col1, col2, col3, col4 = st.columns(4)

col1.metric("Jumlah Responden", len(df))
col2.metric("Median Budget Reward", f"{df['Budget_Reward'].median():,.0f} Rupiah")
col3.metric("Rata-rata Frekuensi Reward", f"{df['Freq_Reward'].mean():.2f}")
col4.metric("Rata-rata Skala Penting", f"{df['Skala_Penting'].mean():.2f}")

# =========================
# DISTRIBUSI NUMERIK
# =========================
st.header("📊 Distribusi Numerik")

num_cols = ["Freq_Reward", "Freq_InginReward", "Budget_Reward", "Durasi_Reward", "Skala_Penting"]
for col in num_cols:
    fig, ax = plt.subplots()
    ax.hist(df[col], bins=20, color='skyblue', edgecolor='black')
    ax.set_title(f"Distribusi {col}")
    ax.set_xlabel(col)
    ax.set_ylabel("Jumlah Responden")
    st.pyplot(fig)

# Boxplot khusus Budget (karena outlier)
st.subheader("📦 Boxplot Budget Reward")
fig, ax = plt.subplots()
ax.boxplot(df["Budget_Reward"], vert=False)
ax.set_xlabel("Budget_Reward")
st.pyplot(fig)

# =========================
# DISTRIBUSI KATEGORI
# =========================
st.header("📊 Distribusi Pilihan Reward, Trigger, dan Efek")

# Fungsi bantu untuk agregasi kolom biner
def top_counts(prefix, top_n=10):
    cols = [c for c in df.columns if c.startswith(prefix)]
    counts = df[cols].sum().sort_values(ascending=False).head(top_n)
    return counts

# Bentuk Reward - Top 10
st.subheader("Top 10 Bentuk Reward")
bentuk_counts = top_counts("Bentuk_Reward")
fig, ax = plt.subplots()
bentuk_counts.plot(kind='barh', ax=ax, color='teal')
ax.invert_yaxis()
ax.set_xlabel("Jumlah Responden")
st.pyplot(fig)

# Trigger Reward - Top 10
st.subheader("Top Trigger Reward")
trigger_counts = top_counts("Trigger_Reward")
fig, ax = plt.subplots()
trigger_counts.plot(kind='barh', ax=ax, color='orange')
ax.invert_yaxis()
ax.set_xlabel("Jumlah Responden")
st.pyplot(fig)

# Efek Reward - Top 10
st.subheader("Top Efek Reward")
efek_counts = top_counts("Efek_Reward")
fig, ax = plt.subplots()
efek_counts.plot(kind='barh', ax=ax, color='purple')
ax.invert_yaxis()
ax.set_xlabel("Jumlah Responden")
st.pyplot(fig)

# =========================
# PERBANDINGAN BUDGET PER TIPE REWARD
# =========================
st.header("💰 Perbandingan Budget per Tipe Reward")

tipe_cols = [
    "Bentuk_Reward_membeli benda yang diinginkan",
    "Bentuk_Reward_traveling",
    "Bentuk_Reward_membeli makanan atau minuman favorit"
]

# Buat boxplot untuk masing-masing tipe
for col in tipe_cols:
    if col in df.columns:
        st.subheader(f"Budget Reward untuk: {col}")
        data_box = [
            df.loc[df[col] == 1, "Budget_Reward"],
            df.loc[df[col] == 0, "Budget_Reward"]
        ]
        fig, ax = plt.subplots()
        ax.boxplot(data_box, labels=["Pilih", "Tidak Pilih"])
        ax.set_ylabel("Budget_Reward")
        st.pyplot(fig)

# =========================
# KORELASI NUMERIK
# =========================
st.header("📈 Korelasi Numerik Sederhana")

corr_cols = ["Freq_Reward", "Freq_InginReward", "Budget_Reward", "Durasi_Reward", "Skala_Penting"]
corr_matrix = df[corr_cols].corr()

st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'))

# Scatter plot Freq_Reward vs Freq_InginReward
st.subheader("Scatter: Freq_Reward vs Freq_InginReward")
fig, ax = plt.subplots()
ax.scatter(df["Freq_Reward"], df["Freq_InginReward"], alpha=0.6)
ax.set_xlabel("Freq_Reward")
ax.set_ylabel("Freq_InginReward")
ax.set_title("Hubungan antara Frekuensi Reward dan Keinginan Reward")
st.pyplot(fig)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("📌 Dashboard ini menampilkan distribusi dan korelasi sederhana dari pola reward mahasiswa. Semua data bersifat anonim.")

