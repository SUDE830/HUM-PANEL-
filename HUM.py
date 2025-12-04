import streamlit as st
import math

# ---------------------------------------------------
# SAYFA AYARI
# ---------------------------------------------------
st.set_page_config(
    page_title="KG Hesaplama Modülü",
    page_icon="⚙️",
    layout="wide"
)

# ---------------------------------------------------
# SİDEBAR TASARIMI + LOGO
# ---------------------------------------------------
st.sidebar.image("hum_logo.png", use_column_width=True)
st.sidebar.markdown("### 🔧 Malzeme Seç")

malzeme = st.sidebar.radio(
    "Malzeme:",
    ["Kestamit", "Çelik", "Bakır", "Alüminyum"]
)

# Yoğunluklar (g/cm3)
YOĞUNLUK = {
    "Kestamit": 1.37,
    "Çelik": 7.85,
    "Bakır": 8.96,
    "Alüminyum": 2.70
}

yog = YOĞUNLUK[malzeme]

st.sidebar.markdown("---")
st.sidebar.markdown("### 📐 Profil Türü Seç")

profil = st.sidebar.radio(
    "Profil Türü:",
    ["Levha", "Yuvarlak", "Boru"]
)

st.sidebar.markdown("---")
st.sidebar.info("Bu panel seçtiğiniz malzemeye göre otomatik hesaplama yapar.")

# ---------------------------------------------------
# FORMÜLLER
# ---------------------------------------------------
def hesap_levha(adet, en, boy, kal, yog):
    hacim_cm3 = (en * boy * kal) / 1000
    return adet * yog * hacim_cm3 / 1000

def hesap_mil(adet, cap, boy, yog):
    r = (cap / 10) / 2
    L = boy / 10
    hacim_cm3 = math.pi * r * r * L
    return adet * yog * hacim_cm3 / 1000

def hesap_boru(adet, dis_cap, ic_cap, boy, yog):
    R = (dis_cap / 10) / 2
    r = (ic_cap / 10) / 2
    L = boy / 10
    hacim_cm3 = math.pi * (R*R - r*r) * L
    return adet * yog * hacim_cm3 / 1000

# ---------------------------------------------------
# ANA BAŞLIK
# ---------------------------------------------------
st.markdown(
    """
    <div style='text-align:center; padding:15px; 
    background:#0e2339; color:white; border-radius:12px;
    margin-bottom:25px;'>
        <h1>Hızlı Malzeme KG Hesaplama Modülü</h1>
        <h4>Seçilen Malzeme: """ + malzeme + """</h4>
    </div>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------
# PROFİL TÜRÜNE GÖRE ANA EKRAN
# ---------------------------------------------------
st.markdown(f"## 📌 {profil} için ölçüleri girin:")

adet = st.number_input("Adet", min_value=1, value=1)

# ---- LEVHA ----
if profil == "Levha":
    en = st.number_input("En (mm)", min_value=0.0)
    boy = st.number_input("Boy (mm)", min_value=0.0)
    kal = st.number_input("Kalınlık (mm)", min_value=0.0)

# ---- YUVARLAK (MİL) ----
elif profil == "Yuvarlak":
    cap = st.number_input("Çap (mm)", min_value=0.0)
    boy = st.number_input("Boy (mm)", min_value=0.0)

# ---- BORU ----
elif profil == "Boru":
    dis_cap = st.number_input("Dış Çap (mm)", min_value=0.0)
    ic_cap = st.number_input("İç Çap (mm)", min_value=0.0)
    boy = st.number_input("Boy (mm)", min_value=0.0)

# ---------------------------------------------------
# SONUÇ
# ---------------------------------------------------
st.markdown("## 📦 Hesaplanan Ağırlık:")

try:
    if profil == "Levha":
        kg = hesap_levha(adet, en, boy, kal, yog)

    elif profil == "Yuvarlak":
        kg = hesap_mil(adet, cap, boy, yog)

    elif profil == "Boru":
        if ic_cap >= dis_cap:
            st.error("İç çap dış çaptan büyük olamaz!")
            kg = None
        else:
            kg = hesap_boru(adet, dis_cap, ic_cap, boy, yog)

    if kg:
        st.success(f"### 💠 Toplam Ağırlık: **{kg:.3f} kg**")

    else:
        st.info("Lütfen tüm değerleri girin.")

except:
    st.warning("Eksik veya hatalı ölçü girdiniz.")
