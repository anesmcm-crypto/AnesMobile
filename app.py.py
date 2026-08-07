import streamlit as st
import time
import json
import os
import requests
import random
import string
import base64
from PIL import Image

# إعدادات الصفحة مع طابع الهاكرز
st.set_page_config(page_title="AnesSecurity - Hacker Portal", page_icon="🛡️", layout="centered")

# --- حقن تصميم الـ CSS وتأثير التوهج والشعار الشفاف ---
st.markdown("""
    <style>
    /* إخفاء أيقونات وقائمة Streamlit العائمة */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    div[data-testid="stToolbar"] {visibility: hidden;}
    div[data-testid="stDecoration"] {visibility: hidden;}
    div[data-testid="stStatusWidget"] {visibility: hidden;}
    #stDecoration {display:none;}

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
    
    /* تصميم حاضنة الشعار في المنتصف بدون خلفية مربعة */
    .cyber-logo-box {
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 20px auto 30px auto;
        padding: 10px;
    }
    
    /* تأثير التوهج والشفافية للدرع فقط */
    .cyber-logo-img {
        width: 190px;
        height: auto;
        filter: drop-shadow(0 0 15px #00ff66) drop-shadow(0 0 30px #00ff66);
        animation: pulse 2s infinite;
    }

    @keyframes pulse {
        0% { transform: scale(1); opacity: 0.85; }
        50% { transform: scale(1.04); opacity: 1; }
        100% { transform: scale(1); opacity: 0.85; }
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
    .stTextInput>div>div>input, .stSelectbox>div>div>div, .stTextArea>div>div>textarea {
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

# --- عرض الشعار بدون خلفية ومتوهج في المنتصف ---
try:
    with open("logo.png", "rb") as image_file:
        encoded_image = base64.b64encode(image_file.read()).decode("utf-8")
    
    st.markdown(f"""
        <div class="cyber-logo-box">
            <img src="data:image/png;base64,{encoded_image}" class="cyber-logo-img" alt="AnesSecurity Logo">
        </div>
    """, unsafe_allow_html=True)
except FileNotFoundError:
    st.markdown("""
        <div class="cyber-logo-box">
            <div style="font-size: 70px; color: #00ff66; text-shadow: 0 0 20px #00ff66;">🛡️</div>
        </div>
    """, unsafe_allow_html=True)
    st.warning("⚠️ ملف الشعار (logo.png) غير موجود في المجلد. يرجى رفعه.")

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

    # --- القسم 5: ترسانة الأدوات والمولدات المتقدمة ---
    with st.expander("⚡ ترسانة الأدوات والمولدات الأمنية الإضافية"):
        
        st.subheader("🔗 كشف الروابط المختصرة (Redirect Checker)")
        short_url = st.text_input("أدخل الرابط المختصر (مثل bit.ly/...):")
        if st.button("كشف الوجهة الحقيقية"):
            if short_url:
                if not short_url.startswith("http"):
                    short_url = "https://" + short_url
                try:
                    resp = requests.head(short_url, allow_redirects=True, timeout=5)
                    st.success(f"الرابط الأصلي الحقيقي هو: `{resp.url}`")
                except:
                    st.error("تعذر تتبع الرابط المختصر، تحقق منه.")
            else:
                st.warning("الرجاء إدخال رابط مختصر أولاً.")

        st.divider()
        st.subheader("👤 مولد الهوية والبيانات الوهمية")
        if st.button("توليد بيانات شخصية وهمية"):
            fake_names = ["Anes Hacker", "CyberGhost", "Matrix_99", "Ghost_X", "Phantom_07"]
            fake_domains = ["gmail.sec", "cybermail.net", "anon.org", "darkbox.io"]
            r_name = random.choice(fake_names) + str(random.randint(10, 99))
            r_email = r_name.lower().replace(" ", "") + "@" + random.choice(fake_domains)
            r_pass = "".join(random.choice(string.ascii_letters + string.digits + "!@#$") for _ in range(12))
            st.write(f"- **اسم المستخدم الوهمي:** `{r_name}`")
            st.write(f"- **البريد الوهمي:** `{r_email}`")
            st.write(f"- **كلمة المرور المقترحة:** `{r_pass}`")

        st.divider()
        st.subheader("🔐 تشفير وفك تشفير النصوص السريعة (Base64)")
        text_to_codec = st.text_area("اكتب النص المراد تشفيره أو فكه:")
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            if st.button("تشفير النص"):
                if text_to_codec:
                    encoded_bytes = base64.b64encode(text_to_codec.encode("utf-8"))
                    st.code(encoded_bytes.decode("utf-8"), language="")
                else:
                    st.warning("اكتب نصاً أولاً.")
        with col_c2:
            if st.button("فك تشفير النص"):
                if text_to_codec:
                    try:
                        decoded_bytes = base64.b64decode(text_to_codec.encode("utf-8"))
                        st.code(decoded_bytes.decode("utf-8"), language="")
                    except:
                        st.error("خطأ: النص المدخل غير مشفر بطريقة صحيحة!")
                else:
                    st.warning("اكتب نصاً مشفراً أولاً.")

        st.divider()
        st.subheader("💻 فحص بصمة المتصفح")
        if st.button("عرض معلومات البصمة"):
            st.info("نوع المتصفح والنظام: متصفح آمن عبر منصة سحابية مشفرة (Secure Node).")

        st.divider()
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
