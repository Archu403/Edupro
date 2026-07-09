import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# PAGE CONFIG
# -----------------------------

st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="",
    layout="wide"
)

# -----------------------------
# TITLE
# -----------------------------

st.title(" Instructor Performance & Course Quality Evaluation")
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



st.header("📊 Key Performance Indicators")

col1,col2,col3,col4 = st.columns(4)

col1.metric("👨‍🏫 Total Teachers", df["TeacherID"].nunique())
col2.metric("📚 Total Courses", df["CourseID"].nunique())
col3.metric("⭐ Avg Teacher Rating", round(df["TeacherRating"].mean(),2))
col4.metric("🌟 Avg Course Rating", round(df["CourseRating"].mean(),2))

col5,col6,col7 = st.columns(3)

col5.metric("💰 Total Revenue", f"${df['Amount'].sum():,.2f}")
col6.metric("📝 Total Transactions", df["TransactionID"].nunique())
col7.metric("📈 Avg Experience", round(df["YearsOfExperience"].mean(),1))
st.subheader("⭐ Teacher Rating Distribution")

fig, ax = plt.subplots(figsize=(8,4))
sns.histplot(df["TeacherRating"], bins=10, kde=True, ax=ax)
st.pyplot(fig)
st.subheader("📈 Experience vs Teacher Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.scatterplot(
    data=df,
    x="YearsOfExperience",
    y="TeacherRating",
    hue="Expertise",
    ax=ax
)

st.pyplot(fig)
st.subheader("📚 Average Course Rating by Category")

category=df.groupby("CourseCategory")["CourseRating"].mean()

fig, ax=plt.subplots(figsize=(10,5))

category.plot(kind="bar", ax=ax)

st.pyplot(fig)
st.subheader("🎓 Course Level")

fig, ax=plt.subplots(figsize=(8,5))

sns.boxplot(
    data=df,
    x="CourseLevel",
    y="CourseRating",
    ax=ax
)

st.pyplot(fig)
st.subheader("🏆 Top 10 Teachers")

top=df.groupby("TeacherName")["TeacherRating"].mean().sort_values(ascending=False).head(10)

st.bar_chart(top)
st.subheader("📉 Bottom 10 Teachers")

bottom=df.groupby("TeacherName")["TeacherRating"].mean().sort_values().head(10)

st.bar_chart(bottom)
st.subheader("👨‍🏫 Expertise Performance")

expert=df.groupby("Expertise")["TeacherRating"].mean()

fig, ax=plt.subplots(figsize=(10,5))

expert.plot(kind="bar", ax=ax)

st.pyplot(fig)

st.subheader("💳 Payment Method")

fig, ax=plt.subplots(figsize=(7,4))

sns.countplot(
    data=df,
    x="PaymentMethod",
    ax=ax
)

st.pyplot(fig)
st.subheader("🔥 Correlation Heatmap")

corr=df[
[
"TeacherRating",
"CourseRating",
"YearsOfExperience",
"CoursePrice",
"CourseDuration",
"Amount"
]
].corr()

fig, ax=plt.subplots(figsize=(8,6))

sns.heatmap(
corr,
annot=True,
cmap="coolwarm",
ax=ax
)

st.pyplot(fig)
st.subheader("📈 Monthly Revenue")

df["TransactionDate"]=pd.to_datetime(df["TransactionDate"])

monthly=df.groupby(df["TransactionDate"].dt.to_period("M"))["Amount"].sum()

monthly.index=monthly.index.astype(str)

st.line_chart(monthly)
st.subheader("📋 Dataset")

st.dataframe(df)
csv=df.to_csv(index=False).encode("utf-8")

st.download_button(
label="📥 Download Dataset",
data=csv,
file_name="EduPro.csv",
mime="text/csv"
)
