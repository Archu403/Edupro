import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="EduPro | Instructor Performance",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CUSTOM STYLE
# ============================================================

st.markdown("""
<style>

.block-container {
    padding-top: 1.5rem;
    padding-bottom: 2rem;
}

.main-title {
    font-size: 36px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    font-size: 17px;
    color: #6b7280;
    margin-bottom: 25px;
}

.section-title {
    font-size: 25px;
    font-weight: 650;
    margin-top: 25px;
    margin-bottom: 15px;
}

div[data-testid="stMetric"] {
    background-color: white;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 12px;
}

[data-testid="stSidebar"] {
    background-color: #f7f9fc;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER
# ============================================================

st.markdown(
    '<div class="main-title">🎓 EduPro Analytics Dashboard</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    'Instructor Performance & Course Quality Evaluation'
    '</div>',
    unsafe_allow_html=True
)

st.markdown("---")

# ============================================================
# LOAD DATA
# ============================================================

@st.cache_data
def load_data():

    df = pd.read_csv("EduPro_Final_Dataset.csv")

    numeric_columns = [
        "Age_x",
        "Age_y",
        "Amount",
        "CoursePrice",
        "CourseDuration",
        "CourseRating",
        "TeacherRating",
        "YearsOfExperience"
    ]

    for column in numeric_columns:
        if column in df.columns:
            df[column] = pd.to_numeric(
                df[column],
                errors="coerce"
            )

    df["TransactionDate"] = pd.to_datetime(
        df["TransactionDate"],
        errors="coerce"
    )

    return df


df = load_data()

# ============================================================
# SIDEBAR
# ============================================================

st.sidebar.title("🎛️ Dashboard Filters")

st.sidebar.markdown(
    "### Select Analysis Filters"
)

st.sidebar.markdown("---")

# ------------------------------------------------------------
# COURSE CATEGORY
# ------------------------------------------------------------

category_options = sorted(
    df["CourseCategory"]
    .dropna()
    .unique()
    .tolist()
)

selected_category = st.sidebar.multiselect(
    "📚 Course Category",
    options=category_options,
    default=category_options
)

# ------------------------------------------------------------
# COURSE LEVEL
# ------------------------------------------------------------

level_options = sorted(
    df["CourseLevel"]
    .dropna()
    .unique()
    .tolist()
)

selected_level = st.sidebar.multiselect(
    "🎓 Course Level",
    options=level_options,
    default=level_options
)

# ------------------------------------------------------------
# COURSE TYPE
# ------------------------------------------------------------

course_type_options = sorted(
    df["CourseType"]
    .dropna()
    .unique()
    .tolist()
)

selected_course_type = st.sidebar.multiselect(
    "📖 Course Type",
    options=course_type_options,
    default=course_type_options
)

# ------------------------------------------------------------
# TEACHER EXPERTISE
# ------------------------------------------------------------

expertise_options = sorted(
    df["Expertise"]
    .dropna()
    .unique()
    .tolist()
)

selected_expertise = st.sidebar.multiselect(
    "👨‍🏫 Instructor Expertise",
    options=expertise_options,
    default=expertise_options
)

# ------------------------------------------------------------
# TEACHER GENDER
# ------------------------------------------------------------

gender_options = sorted(
    df["Gender_y"]
    .dropna()
    .unique()
    .tolist()
)

selected_gender = st.sidebar.multiselect(
    "👤 Instructor Gender",
    options=gender_options,
    default=gender_options
)

# ------------------------------------------------------------
# PAYMENT METHOD
# ------------------------------------------------------------

payment_options = sorted(
    df["PaymentMethod"]
    .dropna()
    .unique()
    .tolist()
)

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    options=payment_options,
    default=payment_options
)

# ------------------------------------------------------------
# TEACHER RATING
# ------------------------------------------------------------

rating_min = float(
    df["TeacherRating"].min()
)

rating_max = float(
    df["TeacherRating"].max()
)

selected_rating = st.sidebar.slider(
    "⭐ Teacher Rating",
    min_value=rating_min,
    max_value=rating_max,
    value=(rating_min, rating_max),
    step=0.1
)

# ------------------------------------------------------------
# EXPERIENCE
# ------------------------------------------------------------

experience_min = int(
    df["YearsOfExperience"].min()
)

experience_max = int(
    df["YearsOfExperience"].max()
)

selected_experience = st.sidebar.slider(
    "📈 Years of Experience",
    min_value=experience_min,
    max_value=experience_max,
    value=(experience_min, experience_max)
)

st.sidebar.markdown("---")

st.sidebar.info(
    "💡 Use the filters to dynamically explore "
    "instructor and course performance."
)

# ============================================================
# APPLY FILTERS
# ============================================================

filtered = df[
    df["CourseCategory"].isin(selected_category)
    &
    df["CourseLevel"].isin(selected_level)
    &
    df["CourseType"].isin(selected_course_type)
    &
    df["Expertise"].isin(selected_expertise)
    &
    df["Gender_y"].isin(selected_gender)
    &
    df["PaymentMethod"].isin(selected_payment)
    &
    df["TeacherRating"].between(
        selected_rating[0],
        selected_rating[1]
    )
    &
    df["YearsOfExperience"].between(
        selected_experience[0],
        selected_experience[1]
    )
].copy()

# ============================================================
# EMPTY DATA
# ============================================================

if filtered.empty:

    st.warning(
        "⚠️ No records found for the selected filters."
    )

    st.stop()

# ============================================================
# KPI DASHBOARD
# ============================================================

st.markdown(
    '<div class="section-title">📊 Executive Overview</div>',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🏫 Total Instructors",
        f"{filtered['TeacherID'].nunique():,}"
    )

with col2:
    st.metric(
        "📚 Total Courses",
        f"{filtered['CourseID'].nunique():,}"
    )

with col3:
    st.metric(
        "⭐ Avg Teacher Rating",
        f"{filtered['TeacherRating'].mean():.2f}"
    )

with col4:
    st.metric(
        "🌟 Avg Course Rating",
        f"{filtered['CourseRating'].mean():.2f}"
    )

col5, col6, col7 = st.columns(3)

with col5:
    st.metric(
        "💰 Total Revenue",
        f"₹{filtered['Amount'].sum():,.0f}"
    )

with col6:
    st.metric(
        "📝 Total Transactions",
        f"{filtered['TransactionID'].nunique():,}"
    )

with col7:
    st.metric(
        "📈 Avg Experience",
        f"{filtered['YearsOfExperience'].mean():.1f} Years"
    )

st.markdown("---")

# ============================================================
# INSTRUCTOR PERFORMANCE
# ============================================================

st.markdown(
    '<div class="section-title">👨‍🏫 Instructor Performance</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# TEACHER RATING DISTRIBUTION
# ------------------------------------------------------------

with col1:

    st.subheader("⭐ Teacher Rating Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.histplot(
        filtered["TeacherRating"].dropna(),
        bins=10,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("Teacher Rating")
    ax.set_ylabel("Number of Records")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ------------------------------------------------------------
# EXPERIENCE VS RATING
# ------------------------------------------------------------

with col2:

    st.subheader("📈 Experience vs Teacher Rating")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.scatterplot(
        data=filtered,
        x="YearsOfExperience",
        y="TeacherRating",
        hue="Expertise",
        ax=ax
    )

    ax.set_xlabel("Years of Experience")
    ax.set_ylabel("Teacher Rating")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ============================================================
# TEACHER VS COURSE RATING
# ============================================================

st.subheader("🎯 Teacher Rating vs Course Rating")

fig, ax = plt.subplots(figsize=(11, 5))

sns.scatterplot(
    data=filtered,
    x="TeacherRating",
    y="CourseRating",
    hue="CourseLevel",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Course Rating")

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ============================================================
# COURSE QUALITY
# ============================================================

st.markdown(
    '<div class="section-title">📚 Course Quality Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ------------------------------------------------------------
# CATEGORY RATING
# ------------------------------------------------------------

with col1:

    st.subheader("📚 Average Rating by Category")

    category_rating = (
        filtered
        .groupby("CourseCategory")["CourseRating"]
        .mean()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    category_rating.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Course Category")
    ax.set_ylabel("Average Course Rating")

    plt.xticks(rotation=45)

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ------------------------------------------------------------
# COURSE LEVEL
# ------------------------------------------------------------

with col2:

    st.subheader("🎓 Course Rating by Level")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.boxplot(
        data=filtered,
        x="CourseLevel",
        y="CourseRating",
        ax=ax
    )

    ax.set_xlabel("Course Level")
    ax.set_ylabel("Course Rating")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ============================================================
# EXPERTISE PERFORMANCE
# ============================================================

st.subheader("🎯 Expertise-wise Performance")

expertise_rating = (
    filtered
    .groupby("Expertise")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(11, 5))

expertise_rating.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Expertise")
ax.set_ylabel("Average Teacher Rating")

plt.xticks(rotation=45)

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ============================================================
# GENDER VS COURSE LEVEL
# ============================================================

st.subheader("👤 Instructor Gender vs Course Level")

gender_level = pd.crosstab(
    filtered["Gender_y"],
    filtered["CourseLevel"]
)

fig, ax = plt.subplots(figsize=(10, 5))

gender_level.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Instructor Gender")
ax.set_ylabel("Number of Courses")

plt.xticks(rotation=0)

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ============================================================
# INSTRUCTOR LEADERBOARD
# ============================================================

st.markdown(
    '<div class="section-title">🏆 Instructor Leaderboard</div>',
    unsafe_allow_html=True
)

teacher_summary = (
    filtered
    .groupby("TeacherName")
    .agg(
        TeacherRating=("TeacherRating", "mean"),
        CourseRating=("CourseRating", "mean"),
        Experience=("YearsOfExperience", "mean"),
        Enrollments=("TransactionID", "count"),
        Revenue=("Amount", "sum")
    )
    .reset_index()
)

teacher_summary = teacher_summary.sort_values(
    "TeacherRating",
    ascending=False
)

st.subheader("🏆 Top 10 Instructors")

st.dataframe(
    teacher_summary.head(10).round(2),
    use_container_width=True,
    hide_index=True
)

st.subheader("📉 Bottom 10 Instructors")

st.dataframe(
    teacher_summary
    .sort_values("TeacherRating")
    .head(10)
    .round(2),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# ENROLLMENT INFLUENCE
# ============================================================

st.markdown(
    '<div class="section-title">📊 Enrollment Influence</div>',
    unsafe_allow_html=True
)

teacher_enrollment = (
    filtered
    .groupby("TeacherName")["TransactionID"]
    .count()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(11, 5))

teacher_enrollment.sort_values().plot(
    kind="barh",
    ax=ax
)

ax.set_xlabel("Number of Enrollments")
ax.set_ylabel("Instructor")

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ============================================================
# REVENUE ANALYSIS
# ============================================================

st.markdown(
    '<div class="section-title">💰 Revenue Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

with col1:

    st.subheader("💳 Payment Method")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.countplot(
        data=filtered,
        x="PaymentMethod",
        ax=ax
    )

    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Transactions")

    plt.xticks(rotation=45)

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

with col2:

    st.subheader("💰 Revenue by Category")

    revenue_category = (
        filtered
        .groupby("CourseCategory")["Amount"]
        .sum()
        .sort_values(ascending=False)
    )

    fig, ax = plt.subplots(figsize=(8, 5))

    revenue_category.plot(
        kind="bar",
        ax=ax
    )

    ax.set_xlabel("Course Category")
    ax.set_ylabel("Revenue")

    plt.xticks(rotation=45)

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ============================================================
# MONTHLY REVENUE
# ============================================================

st.subheader("📅 Monthly Revenue Trend")

monthly_data = filtered.dropna(
    subset=["TransactionDate"]
).copy()

monthly_revenue = (
    monthly_data
    .groupby(
        monthly_data["TransactionDate"].dt.to_period("M")
    )["Amount"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

st.line_chart(
    monthly_revenue,
    use_container_width=True
)

# ============================================================
# CORRELATION HEATMAP
# ============================================================

st.markdown(
    '<div class="section-title">🔥 Correlation Analysis</div>',
    unsafe_allow_html=True
)

corr_columns = [
    "TeacherRating",
    "CourseRating",
    "YearsOfExperience",
    "CoursePrice",
    "CourseDuration",
    "Amount"
]

corr = filtered[corr_columns].corr()

fig, ax = plt.subplots(figsize=(9, 6))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ============================================================
# RATING CONSISTENCY
# ============================================================

st.markdown(
    '<div class="section-title">📏 Rating Consistency Index</div>',
    unsafe_allow_html=True
)

consistency = (
    filtered
    .groupby("TeacherName")["CourseRating"]
    .agg(
        AverageRating="mean",
        RatingStdDev="std",
        CourseCount="count"
    )
    .reset_index()
)

consistency["RatingStdDev"] = (
    consistency["RatingStdDev"].fillna(0)
)

consistency["RatingConsistencyIndex"] = (
    1 / (1 + consistency["RatingStdDev"])
)

st.dataframe(
    consistency
    .sort_values(
        "RatingConsistencyIndex",
        ascending=False
    )
    .head(10)
    .round(3),
    use_container_width=True,
    hide_index=True
)

# ============================================================
# EXPERIENCE IMPACT
# ============================================================

st.markdown(
    '<div class="section-title">📈 Experience Impact Score</div>',
    unsafe_allow_html=True
)

experience_corr = filtered[
    ["YearsOfExperience", "TeacherRating"]
].corr().iloc[0, 1]

st.metric(
    "Experience → Teacher Rating Correlation",
    f"{experience_corr:.3f}"
)

if experience_corr >= 0.5:

    st.success(
        "Strong positive relationship between teaching "
        "experience and teacher rating."
    )

elif experience_corr >= 0.2:

    st.info(
        "Moderate positive relationship between teaching "
        "experience and teacher rating."
    )

elif experience_corr >= -0.2:

    st.warning(
        "Weak relationship between teaching experience "
        "and teacher rating."
    )

else:

    st.error(
        "Negative relationship between teaching experience "
        "and teacher rating."
    )

# ============================================================
# FILTERED DATA
# ============================================================

st.markdown(
    '<div class="section-title">📋 Filtered Dataset</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# DOWNLOAD BUTTON
# ============================================================

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="EduPro_Filtered_Data.csv",
    mime="text/csv"
)

# ============================================================
# FOOTER
# ============================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;color:#6b7280;">
    <b>🎓 EduPro Instructor Performance & Course Quality Evaluation</b>
    <br>
    Data Analytics Project | Unified Mentor
    </div>
    """,
    unsafe_allow_html=True
)
