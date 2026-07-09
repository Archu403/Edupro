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

st.subheader(" Key Performance Indicators")

c1,c2,c3,c4 = st.columns(4)

c1.metric(
    " Teachers",
    filtered["TeacherID"].nunique()
)

c2.metric(
    " Courses",
    filtered["CourseID"].nunique()
)

c3.metric(
    " Avg Teacher Rating",
    round(filtered["TeacherRating"].mean(),2)
)

c4.metric(
    " Avg Course Rating",
    round(filtered["CourseRating"].mean(),2)
)

c5,c6,c7 = st.columns(3)

c5.metric(
    " Total Revenue",
    f"${filtered['Amount'].sum():,.0f}"
)

c6.metric(
    " Transactions",
    filtered["TransactionID"].nunique()
)

c7.metric(
    " Avg Experience",
    round(filtered["YearsOfExperience"].mean(),1)
)

st.markdown("---")
# =====================================
# Teacher Rating Distribution
# =====================================

st.subheader(" Teacher Rating Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["TeacherRating"],
    bins=10,
    kde=True,
    color="royalblue",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Count")

st.pyplot(fig)


# =====================================
# Course Rating Distribution
# =====================================

st.subheader(" Course Rating Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["CourseRating"],
    bins=10,
    kde=True,
    color="green",
    ax=ax
)

ax.set_xlabel("Course Rating")
ax.set_ylabel("Count")

st.pyplot(fig)


# =====================================
# Teacher Experience Distribution
# =====================================

st.subheader(" Years of Experience Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["YearsOfExperience"],
    bins=15,
    kde=True,
    color="orange",
    ax=ax
)

ax.set_xlabel("Years of Experience")

st.pyplot(fig)


# =====================================
# Experience vs Teacher Rating
# =====================================

st.subheader(" Experience vs Teacher Rating")

fig, ax = plt.subplots(figsize=(9,5))

sns.scatterplot(
    data=filtered,
    x="YearsOfExperience",
    y="TeacherRating",
    hue="TeacherGender",
    size="CourseRating",
    palette="Set2",
    ax=ax
)

st.pyplot(fig)


# =====================================
# Teacher Rating vs Course Rating
# =====================================

st.subheader(" Teacher Rating vs Course Rating")

fig, ax = plt.subplots(figsize=(9,5))

sns.scatterplot(
    data=filtered,
    x="TeacherRating",
    y="CourseRating",
    hue="CourseCategory",
    palette="tab10",
    ax=ax
)

st.pyplot(fig)


# =====================================
# Teacher Gender Distribution
# =====================================

st.subheader(" Teacher Gender Distribution")

fig, ax = plt.subplots(figsize=(6,4))

sns.countplot(
    data=filtered,
    x="TeacherGender",
    palette="Set2",
    ax=ax
)

st.pyplot(fig)


# =====================================
# User Gender Distribution
# =====================================

st.subheader(" User Gender Distribution")

fig, ax = plt.subplots(figsize=(6,4))

sns.countplot(
    data=filtered,
    x="UserGender",
    palette="Set3",
    ax=ax
)

st.pyplot(fig)


# =====================================
# Teacher Age Distribution
# =====================================

st.subheader(" Teacher Age Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["TeacherAge"],
    bins=15,
    kde=True,
    color="purple",
    ax=ax
)

st.pyplot(fig)


# =====================================
# User Age Distribution
# =====================================

st.subheader(" User Age Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["UserAge"],
    bins=15,
    kde=True,
    color="brown",
    ax=ax
)

st.pyplot(fig)

st.markdown("---")
# ==========================================
# COURSE CATEGORY ANALYSIS
# ==========================================

st.subheader(" Average Course Rating by Category")

category_rating = (
    filtered.groupby("CourseCategory")["CourseRating"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=category_rating.index,
    y=category_rating.values,
    palette="viridis",
    ax=ax
)

plt.xticks(rotation=45)

ax.set_xlabel("Course Category")
ax.set_ylabel("Average Rating")

st.pyplot(fig)


# ==========================================
# COURSE LEVEL ANALYSIS
# ==========================================

st.subheader(" Course Level Analysis")

fig, ax = plt.subplots(figsize=(8,5))

sns.boxplot(
    data=filtered,
    x="CourseLevel",
    y="CourseRating",
    palette="Pastel1",
    ax=ax
)

st.pyplot(fig)


# ==========================================
# TEACHER EXPERTISE
# ==========================================

st.subheader(" Expertise-wise Teacher Ratings")

expert = (
    filtered.groupby("Expertise")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(12,5))

sns.barplot(
    x=expert.index,
    y=expert.values,
    palette="magma",
    ax=ax
)

plt.xticks(rotation=45)

ax.set_xlabel("Expertise")
ax.set_ylabel("Teacher Rating")

st.pyplot(fig)


# ==========================================
# COURSE PRICE ANALYSIS
# ==========================================

st.subheader("💲 Course Price Distribution")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["CoursePrice"],
    bins=20,
    kde=True,
    color="green",
    ax=ax
)

st.pyplot(fig)


# ==========================================
# COURSE DURATION
# ==========================================

st.subheader("⏳ Course Duration")

fig, ax = plt.subplots(figsize=(8,4))

sns.histplot(
    filtered["CourseDuration"],
    bins=15,
    kde=True,
    color="orange",
    ax=ax
)

st.pyplot(fig)


# ==========================================
# PAYMENT METHOD
# ==========================================

st.subheader("💳 Payment Method Distribution")

fig, ax = plt.subplots(figsize=(7,4))

sns.countplot(
    data=filtered,
    x="PaymentMethod",
    palette="Set2",
    ax=ax
)

plt.xticks(rotation=45)

st.pyplot(fig)


# ==========================================
# REVENUE BY CATEGORY
# ==========================================

st.subheader(" Revenue by Course Category")

revenue = (
    filtered.groupby("CourseCategory")["Amount"]
    .sum()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=revenue.index,
    y=revenue.values,
    palette="rocket",
    ax=ax
)

plt.xticks(rotation=45)

ax.set_ylabel("Revenue")

st.pyplot(fig)


# ==========================================
# MONTHLY REVENUE
# ==========================================

st.subheader(" Monthly Revenue Trend")

filtered["TransactionDate"] = pd.to_datetime(filtered["TransactionDate"])

monthly = (
    filtered.groupby(filtered["TransactionDate"].dt.to_period("M"))["Amount"]
    .sum()
)

monthly.index = monthly.index.astype(str)

fig, ax = plt.subplots(figsize=(12,5))

monthly.plot(
    marker="o",
    linewidth=3,
    ax=ax
)

ax.set_ylabel("Revenue")

plt.xticks(rotation=45)

st.pyplot(fig)

st.markdown("---")
# ==========================================
# TOP 10 TEACHERS
# ==========================================

st.subheader(" Top 10 Teachers")

top_teachers = (
    filtered.groupby("TeacherName")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=top_teachers.values,
    y=top_teachers.index,
    palette="Greens_r",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Teacher")

st.pyplot(fig)

# ==========================================
# BOTTOM 10 TEACHERS
# ==========================================

st.subheader(" Bottom 10 Teachers")

bottom_teachers = (
    filtered.groupby("TeacherName")["TeacherRating"]
    .mean()
    .sort_values()
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=bottom_teachers.values,
    y=bottom_teachers.index,
    palette="Reds",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Teacher")

st.pyplot(fig)

# ==========================================
# TOP COURSES
# ==========================================

st.subheader(" Top 10 Courses")

top_courses = (
    filtered.groupby("CourseName")["CourseRating"]
    .mean()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=top_courses.values,
    y=top_courses.index,
    palette="Blues_r",
    ax=ax
)

ax.set_xlabel("Course Rating")

st.pyplot(fig)

# ==========================================
# CORRELATION HEATMAP
# ==========================================

st.subheader(" Correlation Heatmap")

corr_columns = [
    "TeacherRating",
    "CourseRating",
    "YearsOfExperience",
    "CoursePrice",
    "CourseDuration",
    "Amount"
]

corr = filtered[corr_columns].corr()

fig, ax = plt.subplots(figsize=(8,6))

sns.heatmap(
    corr,
    annot=True,
    cmap="coolwarm",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig)

# ==========================================
# RATING TIERS
# ==========================================

st.subheader(" Teacher Rating Tier")

def rating_tier(r):
    if r >= 4.5:
        return "High"
    elif r >= 3.5:
        return "Medium"
    else:
        return "Low"

filtered["RatingTier"] = filtered["TeacherRating"].apply(rating_tier)

fig, ax = plt.subplots(figsize=(6,4))

sns.countplot(
    data=filtered,
    x="RatingTier",
    palette="Set2",
    ax=ax
)

st.pyplot(fig)

# ==========================================
# EXPERIENCE VS COURSE RATING
# ==========================================

st.subheader(" Experience vs Course Rating")

fig, ax = plt.subplots(figsize=(8,5))

sns.regplot(
    data=filtered,
    x="YearsOfExperience",
    y="CourseRating",
    scatter_kws={"alpha":0.6},
    line_kws={"color":"red"},
    ax=ax
)

st.pyplot(fig)

# ==========================================
# ENROLLMENTS BY EXPERTISE
# ==========================================

st.subheader(" Enrollments by Expertise")

enroll = (
    filtered.groupby("Expertise")["TransactionID"]
    .count()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10,5))

sns.barplot(
    x=enroll.index,
    y=enroll.values,
    palette="viridis",
    ax=ax
)

plt.xticks(rotation=45)

ax.set_ylabel("Enrollments")

st.pyplot(fig)

# ==========================================
# INTERACTIVE DATA TABLE
# ==========================================

st.subheader(" Filtered Dataset")

st.dataframe(filtered)

# ==========================================
# DOWNLOAD BUTTON
# ==========================================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label=" Download Filtered Dataset",
    data=csv,
    file_name="EduPro_Filtered_Data.csv",
    mime="text/csv"
)

st.markdown("---")

st.success(" EduPro Instructor Performance Dashboard Completed Successfully!")
