import streamlit as st
import random

# إعدادات الصفحة
st.set_page_config(page_title="تطبيق سلمى التعليمي", page_icon="🎓", layout="centered")

# CSS لتحسين الشكل
st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3em; background-color: #005088; color: white; }
    .stProgress > div > div > div > div { background-color: #11CAA0; }
    </style>
    """, unsafe_allow_status_with_description=True)

# تهيئة "حالة الجلسة" (Session State) لحفظ النقاط والقلوب
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'hearts' not in st.session_state:
    st.session_state.hearts = 3
if 'current_question' not in st.session_state:
    st.session_state.current_question = 0

# العنوان العلوي
st.title("🏆 تحدي المعرفة مع سلمى")
st.sidebar.header(f"❤️ القلوب: {st.session_state.hearts}")
st.sidebar.header(f"⭐ النقاط: {st.session_state.score}")

# قائمة الأسئلة (مثال)
questions = [
    {"q": "ما هي عاصمة مصر؟", "options": ["القاهرة", "الإسكندرية", "أسوان"], "a": "القاهرة"},
    {"q": "ما هي لغة البرمجة التي نستخدمها الآن؟", "options": ["Java", "Python", "C++"], "a": "Python"}
]

# التحقق من انتهاء القلوب أو الأسئلة
if st.session_state.hearts <= 0:
    st.error("للأسف نفدت المحاولات! حاول مرة أخرى.")
    if st.button("إعادة اللعبة"):
        st.session_state.hearts = 3
        st.session_state.score = 0
        st.session_state.current_question = 0
        st.rerun()
elif st.session_state.current_question >= len(questions):
    st.balloons()
    st.success(f"مبروك! أنهيت التحدي بنجاح بمجموع نقاط: {st.session_state.score}")
else:
    # عرض السؤال الحالي
    q_data = questions[st.session_state.current_question]
    st.subheader(f"السؤال {st.session_state.current_question + 1}: {q_data['q']}")
    
    # استخدام أزرار للاختيارات
    choice = st.radio("اختر الإجابة الصحيحة:", q_data['options'])
    
    if st.button("تأكيد الإجابة"):
        if choice == q_data['a']:
            st.session_state.score += 10
            st.success("إجابة صحيحة! 🎉 +10 نقاط")
            st.session_state.current_question += 1
            st.rerun()
        else:
            st.session_state.hearts -= 1
            st.error("إجابة خاطئة! 💔 فقدت قلباً")
            if st.session_state.hearts > 0:
                st.rerun()

### 🚀 كيف تظهرين هذا التطبيق للدكتور كـ URL؟
1. **حملي مكتبة Streamlit:** في الـ Terminal عندك، اكتبي `pip install streamlit`.
2. **شغلي التطبيق محلياً:** اكتبي `streamlit run app.py` لمشاهدة النتيجة في متصفحك.
3. **النشر (Deployment):**
   - ارفعي ملف الكود على **GitHub**.
   - اذهبي لموقع [streamlit.io/cloud](https://streamlit.io/cloud).
   - اربطي حساب GitHub واختاري الملف.. سيعطيكِ الموقع رابطاً مثل: `salma-edu-app.streamlit.app`.

هذا الرابط هو ما سترسلينه للدكتور يوم الاثنين. هل تريدينني أن أساعدكِ في كتابة الأسئلة الخاصة بمادتكِ داخل هذا الكود؟

عرضك التقديمي الخاص بترقية المشروع جاهز! ألقِ نظرة عليه وأخبريني إذا كنتِ تودين تعديل أي تفاصيل في خطة العمل.
