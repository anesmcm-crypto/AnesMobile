import streamlit as st
import time
import json
import os
import requests
import random
import string

# إعدادات الصفحة مع طابع الهاكرز
st.set_page_config(page_title="AnesSecurity - Hacker Portal", page_icon="🛡️", layout="centered")

# --- حقن تصميم الـ CSS لتغيير الألوان إلى الأسود والأخضر مع تصميم اللوجو (الدرع) ---
st.markdown("""
    <style>
    .stApp {
        background-color: #0b0f0c;
        color: #00ff66;
    }
    
    h1, h2, h3, h4, h5, h6 {
        color: #00ff66 !important;
        font-family: 'Courier New', Courier, monospace;
        text-shadow: 0 0 10px rgba(0, 255, 102, 0.4);
    }
    
    p, label, span {
        color: #c0c0c0 !important;
    }
    
    /* تصميم لوجو الدرع فقط في المنتصف */
    .cyber-logo-box {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        background: radial-gradient(circle, rgba(0,255,102,0.1) 0%, rgba(11,15,12,1) 80%);
        border: 2px solid #00ff66;
        padding: 30px;
        border-radius: 20px;
        margin: 20px auto 30px auto;
        box-shadow: 0 0 25px rgba(0, 255, 102, 0.3);
        width: fit-content;
    }
    
    .cyber-shield-icon {
        font-size: 70px;
        color: #00ff66;
        text-shadow: 0 0 20px #00ff66;
        animation: pulse 2s infinite;
    }
    
    .cyber-shield-word {
        font-size: 28px;
        font-weight: bold;
        color: #00ff66;
        letter-spacing: 4px;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 12px;
        text-transform: uppercase;
        text-shadow: 0 0 15px #00ff66;
    }

    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }

    /* تخصيص أزرار الهاكرز الخضراء */
    .stButton>button {
        background-color: #000000 !important;
        color: #00ff66 !important;
        border: 2px solid #00ff66 !important;
        border-radius: 8px;
        font-weight: bold;
        width: 100%;
        transition: all 0.3s ease;
        box-shadow: 0 0 5px rgba(0, 255, 102, 0.3);
    }
    
    .stButton>button:hover {
        background-color: #00ff66 !important;
        color: #000000 !important;
        box-shadow: 0 0 20px #00ff66;
    }

    /* تخصيص خانات الإدخال */
    .stTextInput>div>div>input, .stSelectbox>div>div>div {
        background-color: #121814 !important;
        color: #00ff66 !important;
        border: 1px solid #00ff66 !important;
        border-radius: 5px;
    }
    </style>
""", unsafe_allow_html=True)

# ملف تخزين بيانات المستخدمين وسجل الفحوصات
DB_FILE = "users_db.json"

def load_users():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            try:
                return json.load(f)
            except:
                return {}
    return {}

def save_users(users):
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

# تهيئة الجلسة
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

users_db = load_users()

# --- عرض لوجو الدرع لوحده في المنتصف مع كلمة أمان ---
st.markdown("""
    <div class="cyber-logo-box">
        <div class="cyber-shield-icon">🛡️</div>
        <div class="cyber-shield-word">أمان</div>
    </div>
""", unsafe_allow_html=True)

# --- إذا لم يكن المستخدم مسجلاً الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 AnesSecurity - Login Portal")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    # 1. نافذة تسجيل الدخول
    with tab1:
        st.subheader("تسجيل الدخول إلى حسابك")
        login_user = st.text_input("اسم المستخدم أو البريد الإلكتروني:", key="login_u")
        login_pass = st.text_input("كلمة المرور:", type="password", key="login_p")
        
        if st.button("دخول النظام"):
            found = False
            for u, data in users_db.items():
                if (u == login_user or data["email"] == login_user) and data["password"] == login_pass:
                    found = True
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success(f"مرحباً بك مجدداً في النظام، {u}!")
                    time.sleep(1)
                    st.rerun()
            if not found:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

    # 2. نافذة إنشاء حساب جديد
    with tab2:
        st.subheader("إنشاء حساب جديد")
        new_email = st.text_input("البريد الإلكتروني (Gmail):")
        new_user = st.text_input("اسم المستخدم (فريد ولا يتكرر):")
        new_pass = st.text_input("كلمة المرور:", type="password")
        
        if st.button("تسجيل الحساب"):
            if not new_email or not new_user or not new_pass:
                st.warning("الرجاء ملء جميع الحقول!")
            elif "@" not in new_email:
                st.error("الرجاء إدخال بريد إلكتروني صحيح!")
            elif new_user in users_db:
                st.error("اسم المستخدم هذا مستخدم مسبقاً! الرجاء اختيار اسم آخر.")
            else:
                email_exists = any(data["email"] == new_email for data in users_db.values())
                if email_exists:
                    st.error("هذا البريد الإلكتروني مسجل بحساب آخر مسبقاً!")
                else:
                    users_db[new_user] = {
                        "email": new_email,
                        "password": new_pass,
                        "history": []
                    }
                    save_users(users_db)
                    st.success("تم إنشاء الحساب بنجاح! انتقل لتبويب تسجيل الدخول.")

else:
    # --- الواجهة الرئيسية بعد تسجيل الدخول بنجاح ---
    current_user = st.session_state.username
    
    st.title(f"⚡ Welcome Agent: {current_user}")
    st.write("لوحة تحكم الأمان وحماية الأجهزة المتقدمة.")

    col1, col2 = st.columns(2)
    with col1:
        st.info("📊 حالة الاتصال: **مؤمن ومشفر**")
    with col2:
        st.success("🔒 جدار الحماية: **نشط**")

    st.divider()

    # --- القسم 1: فحص وتتبع الـ IP والموقع الجغرافي ---
    st.subheader("🌍 فحص وتتبع الـ IP والموقع الجغرافي")
    target_ip = st.text_input("أدخل عنوان IP أو اتركه فارغاً لفحص الـ IP الخاص بك:")
    
    if st.button("كشف معلومات الموقع الجغرافي"):
        ip_query = target_ip.strip() if target_ip.strip() else ""
        api_url = f"http://ip-api.com/json/{ip_query}"
        
        with st.spinner("جاري اختراق واقتفاء أثر السيرفر..."):
            try:
                res = requests.get(api_url, timeout=5).json()
                if res.get("status") == "success":
                    st.success("تم جلب بيانات الـ IP بنجاح:")
                    st.write(f"- **عنوان الـ IP:** `{res.get('query')}`")
                    st.write(f"- **الدولة:** {res.get('country')} ({res.get('countryCode')})")
                    st.write(f"- **المنطقة / الولاية:** {res.get('regionName')}")
                    st.write(f"- **المدينة:** {res.get('city')}")
                    st.write(f"- **مزود الخدمة (ISP):** {res.get('isp')}")
                else:
                    st.error("تعذر العثور على معلومات لهذا الـ IP.")
            except:
                st.warning("حدث خطأ في الاتصال بخدمة الشبكة.")

    st.divider()

    # --- القسم 2: فحص الروابط والأمان الحقيقي ---
    st.subheader("🔍 فحص الروابط والأمان الحقيقي")
    url_input = st.text_input("أدخل رابط الموقع كاملاً (مثال: https://google.com):")

    if st.button("بدء الفحص السيبراني"):
        if url_input:
            if not url_input.startswith("http://") and not url_input.startswith("https://"):
                url_input = "https://" + url_input
                
            with st.spinner("جاري فحص الثغرات واستقرار السيرفر..."):
                try:
                    response = requests.get(url_input, timeout=5)
                    if response.status_code < 400:
                        result_msg = f"✅ آمن ويعمل (كود: {response.status_code})"
                        st.success(f"النتيجة: الرابط `{url_input}` نظامي وآمن للاستخدام!")
                    else:
                        result_msg = f"⚠️ تحذير (كود: {response.status_code})"
                        st.warning(f"النتيجة: استجاب السيرفر برمز ({response.status_code}).")
                except requests.exceptions.RequestException:
                    result_msg = "❌ خطر أو غير صالح"
                    st.error("النتيجة: عذراً، الرابط غير صالح أو وهمي!")
                
                if "history" not in users_db[current_user]:
                    users_db[current_user]["history"] = []
                
                scan_record = f"رابط: {url_input} ── النتيجة: {result_msg}"
                users_db[current_user]["history"].append(scan_record)
                save_users(users_db)
        else:
            st.warning("الرجاء إدخال رابط صحيح أولاً.")

    st.divider()

    # --- القسم 3: فحص قوة كلمات المرور ---
    st.subheader("🔒 فحص قوة كلمة المرور الخاصة بك")
    test_pass = st.text_input("اكتب كلمة سر لفحص قوتها:", type="password", key="check_p")
    
    if st.button("تحليل قوة التشفير"):
        if test_pass:
            score = 0
            if len(test_pass) >= 8: score += 1
            if any(c.isupper() for c in test_pass): score += 1
            if any(c.isdigit() for c in test_pass): score += 1
            if any(c in "!@#$%^&*" for c in test_pass): score += 1
            
            if score == 4:
                st.success("كلمة المرور قوية جداً وتصعب كسرها! 🛡️")
            elif score >= 2:
                st.warning("كلمة المرور متوسطة، أضف رموزاً وأرقاماً. ⚠️")
            else:
                st.error("كلمة المرور ضعيفة جداً وقابلة للاختراق الفوري! ❌")
        else:
            st.warning("الرجاء كتابة كلمة مرور أولاً.")

    st.divider()

    # --- القسم 4: سجل الفحوصات الشخصي ---
    st.subheader("📋 سجل العمليات الخاص بك")
    user_history = users_db.get(current_user, {}).get("history", [])
    
    if user_history:
        st.write(f"سجل العمليات لـ **{current_user}**:")
        for idx, rec in enumerate(reversed(user_history[-10:]), 1):
            st.text(f"{idx}. {rec}")
        
        if st.button("مسح السجل"):
            users_db[current_user]["history"] = []
            save_users(users_db)
            st.success("تم مسح السجل بنجاح!")
            st.rerun()
    else:
        st.info("لا توجد عمليات مسجلة في سجلك حتى الآن.")

    st.divider()

    # --- القسم 5: الأدوات الإضافية (مولدات) ---
    with st.expander("⚡ ترسانة الأدوات والمولدات الأمنية"):
        st.subheader("🔑 مولد كلمات المرور المعقدة")
        pass_length = st.slider("اختر طول كلمة المرور:", min_value=8, max_value=32, value=12)
        if st.button("توليد كلمة سر سرية"):
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            gen_pass = "".join(random.choice(chars) for _ in range(pass_length))
            st.code(gen_pass, language="")

        st.divider()
        st.subheader("🔢 مولد رقم سري PIN")
        pin_len = st.radio("اختر طول الـ PIN:", [4, 6], horizontal=True)
        if st.button("توليد رمز PIN"):
            pin_code = "".join(random.choice(string.digits) for _ in range(pin_len))
            st.code(pin_code, language="")

        st.divider()
        st.subheader("⚡ فحص سرعة واستجابة الشبكة (Ping)")
        if st.button("اختبار استجابة البينغ"):
            with st.spinner("جاري اختبار النبض..."):
                start_t = time.time()
                try:
                    requests.get("https://www.google.com", timeout=3)
                    p_time = int((time.time() - start_t) * 1000)
                    st.success(f"سرعة النبض (Ping): **{p_time} ms**")
                except:
                    st.warning("فشل قياس استجابة الشبكة.")

    st.markdown("---")
    if st.button("تسجيل الخروج من النظام"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    st.markdown("---")
    st.markdown("<p style='text-align: center; color: #00ff66;'>AnesSecurity Cyber Intelligence Crafted in Python</p>", unsafe_allow_html=True)
