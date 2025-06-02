# FormaMind

FormaMind یک سیستم هوشمند برای مدیریت و برنامه‌ریزی تمرینات ورزشی است.

## ویژگی‌ها

- برنامه‌ریزی هوشمند تمرینات
- پشتیبانی از انواع مختلف تمرینات (کاردیو، قدرتی، انعطاف‌پذیری)
- سطوح مختلف تمرین (مبتدی، متوسط، پیشرفته)
- ثبت و پیگیری پیشرفت

## نصب

```bash
pip install -r requirements.txt
```

## استفاده

```python
from formamind import WorkoutEngine

engine = WorkoutEngine(goal="fitness")
plan = engine.get_plan(level="beginner", workout_type="cardio")
print(plan)
```

---

## معرفی پروژه (Persian)
این پروژه یک موتور هوشمند برای تولید و مدیریت برنامه‌های تمرین ورزشی و مدیتیشن است که با توجه به هدف، سطح و وضعیت روحی کاربر، برنامه مناسب را پیشنهاد می‌دهد. این سیستم قابلیت تست، توسعه و گسترش آسان را دارد.

## Project Introduction (English)
Formamind is a smart engine for generating and managing workout and meditation plans, tailored to user goals, levels, and mood. The system is designed for easy testing, development, and extensibility.

---

## ساختار پوشه‌ها (Folder Structure)

```
formamind/         # هسته اصلی سیستم (کدهای Workout و Mind)
tests/             # تست‌های واحد و یکپارچه
requirements.txt   # وابستگی‌های پروژه
README.md          # این فایل راهنما
data/              # داده‌های تمرینات و مدیتیشن (در صورت نیاز)
app.py             # رابط کاربری وب (Streamlit)
```

---

## مثال استفاده (Usage Example)

### استفاده از API
```python
from formamind.workout import WorkoutEngine
engine = WorkoutEngine(goal="fitness")
plan = engine.get_plan(level="beginner", workout_type="cardio", duration=30)
print(plan)
```

### اجرای رابط کاربری وب
```bash
streamlit run app.py
```

---

## اجرای تست‌ها (Running Tests)

```bash
pytest tests/test_workout.py -v
```

---

## مشارکت در توسعه (Contribution)
- لطفاً قبل از هر commit تست‌ها را اجرا کنید.
- برای هر قابلیت جدید، تست مناسب بنویسید.
- کدها را با استاندارد pep8 و ابزار black فرمت کنید.

---

## توسعه‌دهندگان (Developers)
- این پروژه با عشق توسط تیم Formamind توسعه یافته است.

---

برای هرگونه سوال یا همکاری، خوشحال می‌شویم با ما در ارتباط باشید!
