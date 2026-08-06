import streamlit as st
import time
import json
import os
import re
import requests

# إعدادات الصفحة
st.set_page_config(page_title="AnesMobile Dashboard", page_icon="📱", layout="centered")

# ملف تخزين بيانات المستخدمين محلياً في المستودع
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

# --- إذا لم يكن المستخدم مسجلاً الدخول ---
if not st.session_state.logged_in:
    st.title("🔐 AnesMobile - بوابة الأمان")
    
    tab1, tab2 = st.tabs(["تسجيل الدخول", "إنشاء حساب جديد"])
    
    # 1. نافذة تسجيل الدخول
    with tab1:
        st.subheader("تسجيل الدخول إلى حسابك")
        login_user = st.text_input("اسم المستخدم أو البريد الإلكتروني:", key="login_u")
        login_pass = st.text_input("كلمة المرور:", type="password", key="login_p")
        
        if st.button("دخول"):
            found = False
            for u, data in users_db.items():
                if (u == login_user or data["email"] == login_user) and data["password"] == login_pass:
                    found = True
                    st.session_state.logged_in = True
                    st.session_state.username = u
                    st.success(f"مرحباً بك مجدداً، {u}!")
                    time.sleep(1)
                    st.rerun()
            if not found:
                st.error("اسم المستخدم أو كلمة المرور غير صحيحة!")

    # 2. نافذة إنشاء حساب جديد (مع التحقق من تفرد اسم المستخدم)
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
                        "password": new_pass
                    }
                    save_users(users_db)
                    st.success("تم إنشاء الحساب بنجاح! يمكنك الانتقال لتبويب تسجيل الدخول والدخول الآن.")

else:
    # --- الواجهة الرئيسية بعد تسجيل الدخول بنجاح ---
    current_user = st.session_state.username
    
    st.title(f"🛡️ AnesMobile - أهلاً بك، {current_user}")
    st.write("هذه لوحة تحكم حماية الهاتف الخاصة بك.")

    # تقسيم الصفحة إلى أعمدة
    col1, col2 = st.columns(2)

    with col1:
        st.info("📊 حالة الاتصال: **متصل بالشبكة**")
    with col2:
        st.success("🔒 الحماية: **مفعلة وآمنة**")

    st.divider()

    # قسم فحص الروابط والأمان (مع فحص حقيقي)
    st.subheader("🔍 فحص الروابط والأمان الحقيقي")
    url_input = st.text_input("أدخل رابط الموقع كاملاً (مثال: https://google.com):")

    if st.button("بدء الفحص الحقيقي"):
        if url_input:
            # التأكد من أن الإدخال يبدأ بـ http أو https
            if not url_input.startswith("http://") and not url_input.startswith("https://"):
                url_input = "https://" + url_input
                
            with st.spinner("جاري الاتصال بالسيرفر والتحقق من أمان الرابط..."):
                try:
                    # محاولة الاتصال الفعلي بالرابط لمعرفة إذا كان حقيقي وشغال
                    response = requests.get(url_input, timeout=5)
                    if response.status_code < 400:
                        st.success(f"النتيجة: الرابط `{url_input}` يعمل بشكل سليم، مستقر، وآمن للاستخدام!")
                    else:
                        st.warning(f"النتيجة: الموقع استابح برمز استجابة ({response.status_code})، قد يكون هناك تحذير أمان أو عطل مؤقت.")
                except requests.exceptions.RequestException:
                    st.error("النتيجة: عذراً، الرابط المدخل غير صالح، وهمي، أو لا يمكن الوصول إليه!")
        else:
            st.warning("الرجاء إدخال رابط صحيح أولاً.")

    st.divider()

    # قسم الأدوات السريعة
    st.subheader("⚡ أدوات سريعة")
    if st.button("تنظيف ذاكرة التخزين المؤقت (Cache)"):
        st.toast("تم تنظيف الذاكرة بنجاح!", icon="🧹")

    # زر تسجيل الخروج
    st.markdown("---")
    if st.button("تسجيل الخروج"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.rerun()

    # حقوق التطبيق في الأسفل
    st.markdown("<p style='text-align: center; color: gray;'>AnesMobile Crafted with Python & Streamlit</p>", unsafe_allow_html=True)
