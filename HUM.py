# -*- coding: utf-8 -*-
import streamlit as st
import math

st.set_page_config(page_title="Hızlı KG Hesaplama", layout="centered")

st.title("⚙️ Hızlı Malzeme KG Hesaplama Modülü")

# ----------------------------
# MALZEME YOĞUNLUKLARI
# ----------------------------
YOĞUNLUK = {
    "Kestamit": 1.36,
    "Çelik": 7.85,
    "Bakır": 8.96,
    "Alüminyum": 2.70
}

# ----------------------------
# 1) MALZEME SEÇİMİ
# ----------------------------
st.subheader("1️⃣ Malzeme Seç")
malzeme = st.selectbox("Malzeme:", list(YOĞUNLUK.keys()))
rho = YOĞUNLUK[malzeme]   # Yoğunluk

# ----------------------------
# 2) PROFİL TÜRÜ
# ----------------------------
st.subheader("2️⃣ Profil Türü Seç")
profil = st.radio("Profil Türü:", ["Levha", "Yuvarlak", "Boru"])

st.write("---")

# ----------------------------
# 3) BOYUT GİRİŞİ & HESAPLAMA
# ----------------------------
st.subheader("3️⃣ Boyutları Gir")

adet = st.number_input("Adet:", min_value=1, value=1)

kg = None

# ------------------ LEVHA ---------------------------------
if profil == "Levha":
    kal = st.number_input("Kalınlık (mm)", min_value=0.0, step=0.1)
    en = st.number_input("En (mm)", min_value=0.0, step=0.1)
    boy = st.number_input("Boy (mm)", min_value=0.0, step=0.1)

    if kal > 0 and en > 0 and boy > 0:
        hacim = (kal * en * boy) / 1e9  # m³
        kg = rho * hacim * adet

# ------------------ YUVARLAK -------------------------------
elif profil == "Yuvarlak":
    cap = st.number_input("Çap (mm)", min_value=0.0, step=0.1)
    boy = st.number_input("Boy (mm)", min_value=0.0, step=0.1)

    if cap > 0 and boy > 0:
        hacim = (math.pi * (cap ** 2) / 4) * boy / 1e9
        kg = rho * hacim * adet

# ------------------ BORU -----------------------------------
elif profil == "Boru":
    dis_cap = st.number_input("Dış Çap (mm)", min_value=0.0, step=0.1)
    ic_cap = st.number_input("İç Çap (mm)", min_value=0.0, step=0.1)
    boy = st.number_input("Boy (mm)", min_value=0.0, step=0.1)

    if dis_cap > 0 and boy > 0 and ic_cap >= 0:
        hacim = (math.pi * (dis_cap**2 - ic_cap**2) / 4) * boy / 1e9
        kg = rho * hacim * adet

# ----------------------------
# 4) SONUÇ
# ----------------------------
st.write("---")
st.subheader("4️⃣ Hesaplanan Ağırlık")

if kg is not None:
    st.success(f"**Toplam: {kg:.3f} kg**")
else:
    st.info("Lütfen gerekli ölçüleri girin.")
