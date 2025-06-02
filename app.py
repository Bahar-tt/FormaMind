import streamlit as st
from formamind.workout import WorkoutEngine
import pandas as pd
import plotly.express as px

# تنظیمات صفحه
st.set_page_config(
    page_title="فرامایند - سیستم هوشمند تمرینات ورزشی",
    page_icon="💪",
    layout="wide"
)

# استایل‌های سفارشی
st.markdown("""
    <style>
    .main {
        direction: rtl;
        text-align: right;
    }
    .stButton>button {
        width: 100%;
    }
    .workout-card {
        padding: 20px;
        border-radius: 10px;
        background-color: #f8f9fa;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ایجاد موتور تمرینات
engine = WorkoutEngine(goal="fitness")

# عنوان اصلی
st.title("💪 فرامایند - سیستم هوشمند تمرینات ورزشی")

# انتخاب نوع تمرین
workout_type = st.selectbox(
    "نوع تمرین را انتخاب کنید",
    engine.get_available_types(),
    format_func=lambda x: {
        "cardio": "کاردیو",
        "strength": "قدرتی",
        "flexibility": "انعطاف‌پذیری",
        "yoga": "یوگا"
    }[x]
)

# انتخاب سطح
level = st.selectbox(
    "سطح تمرین را انتخاب کنید",
    engine.get_available_levels(),
    format_func=lambda x: {
        "beginner": "مبتدی",
        "intermediate": "متوسط",
        "advanced": "پیشرفته"
    }[x]
)

# دریافت برنامه تمرینی
if st.button("دریافت برنامه تمرینی"):
    plan = engine.get_plan(workout_type=workout_type, level=level)
    if plan:
        st.markdown("### برنامه تمرینی پیشنهادی")
        st.markdown(plan)
        
        # نمایش آمار تمرینات
        st.markdown("### آمار تمرینات")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("تعداد تمرینات", "3")
        with col2:
            st.metric("مدت زمان کل", "80 دقیقه")
        with col3:
            st.metric("کالری سوزانده شده", "350")
            
        # نمودار شدت تمرینات
        intensity_data = {
            "شدت": ["کم", "متوسط", "زیاد"],
            "تعداد": [1, 2, 1]
        }
        df = pd.DataFrame(intensity_data)
        fig = px.bar(df, x="شدت", y="تعداد", title="توزیع شدت تمرینات")
        st.plotly_chart(fig)
    else:
        st.error("متأسفانه برنامه‌ای برای این سطح و نوع تمرین یافت نشد.")

# بخش ایجاد تمرین سفارشی
st.markdown("### ایجاد تمرین سفارشی")
with st.form("custom_workout"):
    name = st.text_input("نام تمرین")
    duration = st.number_input("مدت زمان (دقیقه)", min_value=1, max_value=180)
    difficulty = st.selectbox(
        "سطح دشواری",
        ["beginner", "intermediate", "advanced"],
        format_func=lambda x: {
            "beginner": "مبتدی",
            "intermediate": "متوسط",
            "advanced": "پیشرفته"
        }[x]
    )
    
    submitted = st.form_submit_button("ایجاد تمرین")
    if submitted:
        try:
            workout = engine.create_workout(
                name=name,
                duration=duration,
                difficulty=difficulty
            )
            st.success("تمرین با موفقیت ایجاد شد!")
            st.json(workout)
        except ValueError as e:
            st.error(str(e))

# بخش ثبت پیشرفت
st.markdown("### ثبت پیشرفت تمرین")
with st.form("progress"):
    workout_id = st.text_input("شناسه تمرین")
    user_id = st.text_input("شناسه کاربر")
    duration = st.number_input("مدت زمان انجام شده (دقیقه)", min_value=1)
    calories = st.number_input("کالری سوزانده شده", min_value=1)
    
    submitted = st.form_submit_button("ثبت پیشرفت")
    if submitted:
        try:
            progress = engine.record_progress(
                workout_id=workout_id,
                user_id=user_id,
                completed_exercises=[],
                duration=duration,
                calories_burned=calories
            )
            st.success("پیشرفت با موفقیت ثبت شد!")
            st.json(progress)
        except ValueError as e:
            st.error(str(e)) 