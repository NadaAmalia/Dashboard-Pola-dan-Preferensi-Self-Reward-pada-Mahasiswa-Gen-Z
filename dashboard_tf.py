import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# =========================
# SETUP DASHBOARD
# =========================
st.set_page_config(page_title="🎁 Dashboard Self-Reward Pada Mahasiswa Gen Z", layout="wide")

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.image("https://img.icons8.com/color/96/000000/gift.png")
    st.title("Reward Dashboard")
    st.markdown("### 📊 Navigasi")
    st.button("Ringkasan")
    st.button("Kategori")
    st.button("Perbandingan")
    st.button("Korelasi")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data_prep_final.csv")
    return df

df = load_data()

# Hapus kolom privasi jika ada
df = df.drop(columns=[c for c in df.columns if "Nama" in c or "Whatsapp" in c], errors="ignore")

# =========================
# HEADER
# =========================
st.markdown(
    """
    <div style="background-color:#1E3A8A;padding:15px;border-radius:10px;margin-bottom:20px">
        <h1 style="color:white;text-align:center;">🎁 DASHBOARD POLA SELF-REWARD PADA MAHASISWA GEN Z</h1>
    </div>
    """,
    unsafe_allow_html=True
)

# =========================
# KARTU RINGKASAN (TOP SECTION)
# =========================
total_responden = len(df)
median_budget = df['Budget_Reward'].median()
mean_freq = df['Freq_Reward'].mean()

# Rata-rata skala penting dalam persen
mean_penting = df['Skala_Penting'].mean()
persentase_penting = (mean_penting / 5) * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("📋 Jumlah Responden", f"{total_responden}")
col2.metric("💰 Median Budget Reward", f"Rp{median_budget:,.0f}")
col3.metric("📅 Rata-rata Frekuensi Reward", f"{mean_freq:.2f}")
col4.metric("⭐ Rata-rata Skala Penting", f"{persentase_penting:.2f}%")

# =========================
# BOX PLOT (Budget Reward)
# =========================
st.markdown("## 📦 Boxplot Budget Reward")
fig, ax = plt.subplots()
ax.boxplot(df["Budget_Reward"], vert=False)
ax.set_title("Boxplot Budget Reward")
ax.set_xlabel("Budget_Reward")
st.pyplot(fig)

# =========================
# KATEGORI POPULER (Bar Chart Horizontal)
# =========================
st.markdown("## 🏆 Top 10 Bentuk, Trigger, dan Efek Reward")

def top_counts(prefix, top_n=10):
    cols = [c for c in df.columns if c.startswith(prefix)]
    counts = df[cols].sum().sort_values(ascending=False).head(top_n)
    return counts

colE, colF, colG = st.columns(3)

with colE:
    bentuk_counts = top_counts("Bentuk_Reward")
    fig, ax = plt.subplots()
    bentuk_counts.plot(kind='barh', ax=ax, color="#3B82F6")
    ax.set_title("Top 10 Bentuk Reward")
    ax.invert_yaxis()
    st.pyplot(fig)

with colF:
    trigger_counts = top_counts("Trigger_Reward")
    fig, ax = plt.subplots()
    trigger_counts.plot(kind='barh', ax=ax, color="#F59E0B")
    ax.set_title("Top Trigger Reward")
    ax.invert_yaxis()
    st.pyplot(fig)

with colG:
    efek_counts = top_counts("Efek_Reward")
    fig, ax = plt.subplots()
    efek_counts.plot(kind='barh', ax=ax, color="#8B5CF6")
    ax.set_title("Top Efek Reward")
    ax.invert_yaxis()
    st.pyplot(fig)

# =========================
# PERBANDINGAN BUDGET PER TIPE REWARD
# =========================
st.markdown("## 💰 Perbandingan Budget per Tipe Reward")

tipe_cols = [
    "Bentuk_Reward_membeli benda yang diinginkan",
    "Bentuk_Reward_traveling",
    "Bentuk_Reward_membeli makanan atau minuman favorit"
]

colH, colI, colJ = st.columns(3)
for idx, col in enumerate(tipe_cols):
    if col in df.columns:
        data_box = [
            df.loc[df[col] == 1, "Budget_Reward"],
            df.loc[df[col] == 0, "Budget_Reward"]
        ]
        fig, ax = plt.subplots()
        ax.boxplot(data_box, labels=["Pilih", "Tidak"])
        ax.set_title(col.replace("Bentuk_Reward_", ""))
        ax.set_ylabel("Budget_Reward")
        [colH, colI, colJ][idx].pyplot(fig)

# =========================
# KORELASI NUMERIK
# =========================
st.markdown("## 📈 Korelasi Numerik")
corr_cols = ["Freq_Reward", "Freq_InginReward", "Budget_Reward", "Durasi_Reward", "Skala_Penting"]
corr_matrix = df[corr_cols].corr()
st.dataframe(corr_matrix.style.background_gradient(cmap='coolwarm'))

fig, ax = plt.subplots()
ax.scatter(df["Freq_Reward"], df["Freq_InginReward"], alpha=0.6, color="#3B82F6")
ax.set_xlabel("Freq_Reward")
ax.set_ylabel("Freq_InginReward")
ax.set_title("Scatter: Freq_Reward vs Freq_InginReward")
st.pyplot(fig)

# =========================
# FOOTER
# =========================
st.markdown("---")
st.caption("📌 Dashboard interaktif pola reward mahasiswa | Dibuat dengan ❤ pakai Streamlit")
