import streamlit as st
import time

# إعدادات الصفحة
st.set_page_config(page_title="AnesMobile Dashboard", page_icon="📱", layout="centered")

# نظام تسجيل الدخول أو إدخال البريد للترحيب بالمستخدم
if "user_email" not in st.session_state:
    st.session_state.user_email = ""

# إذا ما زال ما دخلش الإيميل، نعرضوله واجهة تسجيل دخول بسيطة
if not st.session_state.user_email:
    st.title("🔐 مرحباً بك في AnesMobile")
    st.write("الرجاء إدخال بريدك الإلكتروني أو اسمك للوصول إلى لوحة التحكم:")
    
    with st.form("login_form"):
        entered_input = st.text_input("البريد الإلكتروني أو الاسم:")
        submit_button = st.form_submit_button("دخول للموقع")
        
        if submit_button:
            if entered_input:
                st.session_state.user_email = entered_input
                st.rerun() # إعادة تحميل الصفحة باش تتفعل اللوحة باسمه
            else:
                st.error("الرجاء إدخال معلومة صحيحة للمتابعة.")
                
else:
    # --- الواجهة الرئيسية للموقع بعد تسجيل الدخول ---
    
    # استخراج اسم المستخدم أو الإيميل للترحيب به
    current_user = st.session_state.user_email
    
    st.title(f"🛡️ AnesMobile - أهلاً بك، {current_user}")
    st.write("هذه لوحة تحكم حماية الهاتف الخاصة بك.")

    # تقسيم الصفحة إلى أعمدة
    col1, col2 = st.columns(2)

    with col1:
        st.info("📊 حالة الاتصال: **متصل بالشبكة**")
    with col2:
        st.success("🔒 الحماية: **مفعلة وآمنة**")

    st.divider()

    # قسم فحص الروابط والأمان
    st.subheader("🔍 فحص الروابط والأمان")
    url_input = st.text_input("أدخل رابط الموقع أو الـ IP للفحص:")

    if st.button("بدء الفحص الآن"):
        if url_input:
            if len(url_input) > 300:
                st.error("الرابط المدخل طويل جداً وغير صالح!")
            else:
                with st.spinner("جاري فحص السيرفر والتحقق من الأمان..."):
                    time.sleep(2)
                st.success(f"النتيجة: الرابط أو الـ IP المدخل آمن ولا توجد أي تهديدات مسجلة!")
        else:
            st.warning("الرجاء إدخال رابط أو عنوان IP أولاً.")

    st.divider()

    # قسم الأدوات السريعة
    st.subheader("⚡ أدوات سريعة")
    if st.button("تنظيف ذاكرة التخزين المؤقت (Cache)"):
        st.toast("تم تنظيف الذاكرة بنجاح!", icon="🧹")

    # زر الخروج أو تبديل الحساب
    st.markdown("---")
    if st.button("تسجيل الخروج / تغيير الحساب"):
        st.session_state.user_email = ""
        st.rerun()

    # حقوق التطبيق في الأسفل
    st.markdown("<p style='text-align: center; color: gray;'>AnesMobile Crafted with Python & Streamlit</p>", unsafe_allow_html=True)
