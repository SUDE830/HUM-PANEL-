import streamlit as st
import math

# ---------------------------------------------------
# SAYFA AYARLARI
# ---------------------------------------------------
st.set_page_config(
    page_title="Hızlı Malzeme KG Hesaplama",
    page_icon="⚙️",
    layout="centered"
)

# ---------------------------------------------------
# ÖZEL CSS TASARIMI + LOGO BÖLÜMÜ
# ---------------------------------------------------
st.markdown("""
<style>
/* GENEL */
body {
    font-family: 'Segoe UI', sans-serif;
}

/* HEADER KUTUSU */
.header-box {
    background: linear-gradient(90deg, #0d2538, #143957);
    padding: 25px;
    text-align: center;
    border-radius: 14px;
    color: white;
    margin-bottom: 35px;
    box-shadow: 0 0 22px rgba(0,0,0,0.40);
}

/* LOGO */
.logo-img {
    width: 180px;
    margin-bottom: 10px;
}

/* KART TASARIMI */
.card {
    background: rgba(255,255,255,0.05);
    padding: 22px;
    border-radius: 12px;
    margin-bottom: 20px;
    border: 1px solid rgba(255,255,255,0.10);
    box-shadow: 0 0 12px rgba(0,0,0,0.25);
}

/* FOOTER */
.footer {
    text-align:center;
    padding: 10px;
    margin-top: 30px;
    opacity: 0.5;
    font-size: 13px;
}
</style>
""", unsafe_allow_html=True)


# ---------------------------------------------------
# YOĞUNLUKLAR (g/cm3)
# ---------------------------------------------------
YOĞUNLUK = {
    "Kestamit": 1.37,
    "Çelik": 7.85,
    "Bakır": 8.96,
    "Alüminyum": 2.70,
}

# ---------------------------------------------------
# FORMÜLLER (ASLA DEĞİŞTİRİLMEDİ!)
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
# HEADER + LOGO
# ---------------------------------------------------
st.markdown("<div class='header-box'>", unsafe_allow_html=True)

st.image("hum_logo.png", use_column_width=False, output_format="PNG", caption="", width=180)

st.markdown(
    "<h1 style='margin-top:5px;'>Hızlı Malzeme KG Hesaplama Modülü</h1>",
    unsafe_allow_html=True
)

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# 1) MALZEME SEÇ
# ---------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("1️⃣ Malzeme Seç")

malzeme = st.selectbox("Malzeme:", list(YOĞUNLUK.keys()))
yog = YOĞUNLUK[malzeme]

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# 2) PROFİL TÜRÜ
# ---------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("2️⃣ Profil Türü Seç")

profil = st.radio("Profil Türü:", ["Levha", "Yuvarlak", "Boru"])
st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# 3) ÖLÇÜLER
# ---------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("3️⃣ Boyutları Gir")

adet = st.number_input("Adet", min_value=1, value=1)

if profil == "Levha":
    en = st.number_input("En (mm)", min_value=0.0, value=50.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=50.0)
    kal = st.number_input("Kalınlık (mm)", min_value=0.0, value=50.0)

elif profil == "Yuvarlak":
    cap = st.number_input("Çap (mm)", min_value=0.0, value=30.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=1000.0)

elif profil == "Boru":
    dis_cap = st.number_input("Dış Çap (mm)", min_value=0.0, value=40.0)
    ic_cap = st.number_input("İç Çap (mm)", min_value=0.0, value=30.0)
    boy = st.number_input("Boy (mm)", min_value=0.0, value=1000.0)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------------------------------
# 4) SONUÇ
# ---------------------------------------------------
st.markdown("<div class='card'>", unsafe_allow_html=True)
st.subheader("4️⃣ Hesaplanan Ağırlık")

kg = None

if profil == "Levha":
    kg = hesap_levha(adet, en, boy, kal, yog)

elif profil == "Yuvarlak":
    kg = hesap_mil(adet, cap, boy, yog)

elif profil == "Boru" and dis_cap > ic_cap:
    kg = hesap_boru(adet, dis_cap, ic_cap, boy, yog)

if kg:
    st.success(f"**Toplam Ağırlık: {kg:.3f} kg**")
else:
    st.info("Lütfen tüm ölçüleri girin.")

st.markdown("</div>", unsafe_allow_html=True)


# ---------------------------------------------------
# FOOTER
# ---------------------------------------------------
st.markdown("<div class='footer'>HUM Mühendislik • Otomatik KG Hesaplama Modülü</div>", unsafe_allow_html=True)

