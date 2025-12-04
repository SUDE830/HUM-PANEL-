import streamlit as st

st.set_page_config(
    page_title="Hızlı Malzeme KG Hesaplama",
    page_icon="⚙️",
    layout="centered"
)

# ===========================
# YOĞUNLUKLAR (g/cm3)
# ===========================
YOĞUNLUK = {
    "Kestamit": 1.37,
    "Çelik": 7.85,
    "Bakır": 8.96,
    "Alüminyum": 2.70,
}

# ===========================
# HESAP FONKSİYONLARI
# ===========================

def hesap_levha(adet, en, boy, kal, yog):
    """
    LEVHA HACİM FORMÜLÜ:
    V (cm3) = (en * boy * kal) / 1000
    Ağırlık (kg) = adet * yog * V / 1000
    """
    hacim_cm3 = (en * boy * kal) / 1000
    kg = adet * yog * hacim_cm3 / 1000
    return kg


def hesap_mil(adet, cap, boy, yog):
    """
    YUVARLAK (MİL) HACİM FORMÜLÜ:
    V = π * (d/2)^2 * L
    mm → cm dönüşümü: mm/10
    """
    import math
    r = (cap / 10) / 2
    L = boy / 10
    hacim_cm3 = math.pi * r * r * L
    kg = adet * yog * hacim_cm3 / 1000
    return kg


def hesap_boru(adet, dis_cap, ic_cap, boy, yog):
    """
    BORU HACİM FORMÜLÜ:
    V = π * (R² - r²) * L
    mm → cm dönüşümü
    """
    import math
    R = (dis_cap / 10) / 2
    r = (ic_cap / 10) / 2
    L = boy / 10
    hacim_cm3 = math.pi * (R*R - r*r) * L
    kg = adet * yog * hacim_cm3 / 1000
    return kg


# ===========================
# UI TASARIMI
# ===========================

st.markdown("<h1 style='text-align:center;'>⚙️ Hızlı Malzeme KG Hesaplama Modülü</h1>", unsafe_allow_html=True)
st.write("")

# -------- 1-) Malzeme Seç --------
st.subheader("1️⃣ Malzeme Seç")

malzeme = st.selectbox("Malzeme:", list(YOĞUNLUK.keys()))
yog = YOĞUNLUK[malzeme]

# -------- 2-) Profil Türü Seç --------
st.subheader("2️⃣ Profil Türü Seç")

profil = st.radio("Profil Türü:", ["Levha", "Yuvarlak", "Boru"])

# -------- 3-) Boyutlar --------
st.subheader("3️⃣ Boyutları Gir")

adet = st.number_input("Adet", min_value=1, value=1)

# LEVHA ----------------------------------------------------------
if profil == "Levha":
    en = st.number_input("En (mm)", min_value=0.0, value=50.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=50.0)
    kal = st.number_input("Kalınlık (mm)", min_value=0.0, value=50.0)

    if en > 0 and boy > 0 and kal > 0:
        kg = hesap_levha(adet, en, boy, kal, yog)
        st.subheader("4️⃣ Hesaplanan Ağırlık")
        st.success(f"Toplam Ağırlık: **{kg:.3f} kg**")

# MIL -------------------------------------------------------------
elif profil == "Yuvarlak":
    cap = st.number_input("Çap (mm)", min_value=0.0, value=30.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=1000.0)

    if cap > 0 and boy > 0:
        kg = hesap_mil(adet, cap, boy, yog)
        st.subheader("4️⃣ Hesaplanan Ağırlık")
        st.success(f"Toplam Ağırlık: **{kg:.3f} kg**")

# BORU ------------------------------------------------------------
elif profil == "Boru":
    dis_cap = st.number_input("Dış Çap (mm)", min_value=0.0, value=40.0)
    ic_cap = st.number_input("İç Çap (mm)", min_value=0.0, value=30.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=1000.0)

    if dis_cap > 0 and ic_cap >= 0 and boy > 0 and dis_cap > ic_cap:
        kg = hesap_boru(adet, dis_cap, ic_cap, boy, yog)
        st.subheader("4️⃣ Hesaplanan Ağırlık")
        st.success(f"Toplam Ağırlık: **{kg:.3f} kg**")

