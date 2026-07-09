import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="🎓",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------

st.title("🎓 Instructor Performance & Course Quality Evaluation")
st.markdown("### EduPro Analytics Dashboard")

# -----------------------------
# LOAD DATA
# -----------------------------

df = pd.read_csv("EduPro_Final_Dataset.csv")

# -----------------------------
# SIDEBAR
# -----------------------------

st.sidebar.header("Dashboard Filters")

category = st.sidebar.multiselect(
    "Course Category",
    sorted(df["CourseCategory"].unique()),
    default=sorted(df["CourseCategory"].unique())
)

level = st.sidebar.multiselect(
    "Course Level",
    sorted(df["CourseLevel"].unique()),
    default=sorted(df["CourseLevel"].unique())
)

expertise = st.sidebar.multiselect(
    "Teacher Expertise",
    sorted(df["Expertise"].unique()),
    default=sorted(df["Expertise"].unique())
)

teacher_gender = st.sidebar.multiselect(
    "Teacher Gender",
    sorted(df["TeacherGender"].unique()),
    default=sorted(df["TeacherGender"].unique())
)

payment = st.sidebar.multiselect(
    "Payment Method",
    sorted(df["PaymentMethod"].unique()),
    default=sorted(df["PaymentMethod"].unique())
)

rating = st.sidebar.slider(
    "Teacher Rating",
    float(df.TeacherRating.min()),
    float(df.TeacherRating.max()),
    (
        float(df.TeacherRating.min()),
        float(df.TeacherRating.max())
    )
)

experience = st.sidebar.slider(
    "Years of Experience",
    int(df.YearsOfExperience.min()),
    int(df.YearsOfExperience.max()),
    (
        int(df.YearsOfExperience.min()),
        int(df.YearsOfExperience.max())
    )
)

# -----------------------------
# FILTER DATA
# -----------------------------

filtered = df[
    (df["CourseCategory"].isin(category)) &
    (df["CourseLevel"].isin(level)) &
    (df["Expertise"].isin(expertise)) &
    (df["TeacherGender"].isin(teacher_gender)) &
    (df["PaymentMethod"].isin(payment)) &
    (df["TeacherRating"]>=rating[0]) &
    (df["TeacherRating"]<=rating[1]) &
    (df["YearsOfExperience"]>=experience[0]) &
    (df["YearsOfExperience"]<=experience[1])
]

# -----------------------------
# KPI SECTION
# -----------------------------

st.markdown("---")

st.subheader("📊 Key Performance Indicators")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    "👨‍🏫 Teachers",
    filtered["TeacherID"].nunique()
)

c2.metric(
    "📚 Courses",
    filtered["CourseID"].nunique()
)

c3.metric(
    "⭐ Avg Teacher Rating",
    round(filtered["TeacherRating"].mean(),2)
)

c4.metric(
    "🌟 Avg Course Rating",
    round(filtered["CourseRating"].mean(),2)
)

c5,c6,c7 = st.columns(3)

c5.metric(
    "💰 Total Revenue",
    f"${filtered['Amount'].sum():,.0f}"
)

c6.metric(
    "📝 Transactions",
    filtered["TransactionID"].nunique()
)

c7.metric(
    "📈 Avg Experience",
    round(filtered["YearsOfExperience"].mean(),1)
)

st.markdown("---")
