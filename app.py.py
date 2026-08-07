import streamlit as st
import time
import json
import os
import requests
import random
import string
import base64

# إعدادات الصفحة
st.set_page_config(page_title="AnesSecurity - Hacker Portal", page_icon="🛡️", layout="centered")

# --- كود الـ CSS الكامل والمعدل لإظهار الدرع فقط داخل الدائرة ---
st.markdown("""
    <style>
    /* إخفاء عناصر Streamlit */
    #MainMenu, footer, header, .stDeployButton, div[data-testid="stToolbar"], div[data-testid="stDecoration"], div[data-testid="stStatusWidget"] {
        display: none !important;
    }

    .stApp { background-color: #0b0f0c; color: #00ff66; }
    
    h1, h2, h3 { color: #00ff66 !important; font-family: 'Courier New', Courier, monospace; text-align: center; text-shadow: 0 0 10px rgba(0, 255, 102, 0.4); }
    
    .cyber-logo-box { display: flex; align-items: center; justify-content: center; margin: 10px auto 20px auto; }
    
    /* تكبير الصورة وقص الأطراف لإظهار الدرع فقط داخل الدائرة المتوهجة */
    .cyber-logo-img {
        width: 190px;
        height: 190px;
        object-fit: cover;
        object-position: center;
        transform: scale(1.6);
        border-radius: 50%;
        border: 2px solid #00ff66;
        box-shadow: 0 0 20px #00ff66, inset 0 0 15px #00ff66;
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1.6); box-shadow: 0 0 15px #00ff66; }
        50% { transform: scale(1.68); box-shadow: 0 0 30px #00ff66; }
        100% { transform: scale(1.6); box-shadow: 0 0 15px #00ff66; }
    }

    .stButton>button { background-color: #000000 !important; color: #00ff66 !important; border: 2px solid #00ff66 !important; border-radius: 8px; font-weight: bold; width: 100%; transition: all 0.3s ease; }
    .stButton>button:hover { background-color: #00ff66 !important; color: #000000 !important; box-shadow: 0 0 20px #00ff66; }
    .stTextInput>div>div>input { background-color: #121814 !important; color: #00ff66 !important; border: 1px solid #00ff66 !important; }
    </style>
""", unsafe_allow_html=True)

# إدارة قاعدة البيانات
DB_FILE = "users_db.json"
def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try: return json.load(f)
            except: return {}
    return {}

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# تهيئة الجلسة
if "logged_in" not in st.session_state: st.session_state.logged_in = False
if "username" not in st.session_state: st.session_state.username = ""
users_db = load_users()

# عرض الشعار الدائري
try:
    with open("logo.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    st.markdown(f'<div class="cyber-logo-box"><img src="data:image/png;base64,{encoded_image}" class="cyber-logo-img"></div>', unsafe_allow_html=True)
except FileNotFoundError:
    st.warning("⚠️ يرجى التأكد من رفع ملف 'logo.png' في المجلد.")

# المنطق الأساسي للموقع
if not st.session_state.logged_in:
    st.title("🔐 AnesSecurity Portal")
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب"])
    with tab1:
        u = st.text_input("اسم المستخدم:")
        p = st.text_input("كلمة المرور:", type="password")
        if st.button("دخول"):
            if u in users_db and users_db[u]["password"] == p:
                st.session_state.logged_in = True
                st.session_state.username = u
                st.rerun()
            else: st.error("بيانات خاطئة!")
    with tab2:
        pass
else:
    st.title(f"⚡ Welcome Agent: {st.session_state.username}")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.rerun()
