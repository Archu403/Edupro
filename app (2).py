import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="EduPro Dashboard",
    page_icon="🎓",
    layout="wide"
)

# =========================================================
# TITLE
# =========================================================

st.title("🎓 EduPro Instructor Performance & Course Quality Evaluation")
st.markdown(
    "### Instructor Performance, Course Quality & Enrollment Analytics"
)

st.markdown("---")

# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("EduPro_Final_Dataset.csv")

    # Convert numeric columns
    numeric_columns = [
        "TeacherRating",
        "CourseRating",
        "YearsOfExperience",
        "CoursePrice",
        "CourseDuration",
        "Amount"
    ]

    for col in numeric_columns:
        if col in df.columns:
            df[col] = pd.to_numeric(
                df[col],
                errors="coerce"
            )

    # Convert date
    if "TransactionDate" in df.columns:
        df["TransactionDate"] = pd.to_datetime(
            df["TransactionDate"],
            errors="coerce"
        )

    return df


df = load_data()

# =========================================================
# CHECK DATA
# =========================================================

if df.empty:
    st.error("❌ Dataset is empty.")
    st.stop()

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header("🎛️ Dashboard Filters")

# ---------------------------------------------------------
# CATEGORY FILTER
# ---------------------------------------------------------

category_list = sorted(
    df["CourseCategory"].dropna().unique().tolist()
)

selected_category = st.sidebar.multiselect(
    "📚 Course Category",
    category_list,
    default=category_list
)

# ---------------------------------------------------------
# COURSE LEVEL FILTER
# ---------------------------------------------------------

level_list = sorted(
    df["CourseLevel"].dropna().unique().tolist()
)

selected_level = st.sidebar.multiselect(
    "🎓 Course Level",
    level_list,
    default=level_list
)

# ---------------------------------------------------------
# EXPERTISE FILTER
# ---------------------------------------------------------

expertise_list = sorted(
    df["Expertise"].dropna().unique().tolist()
)

selected_expertise = st.sidebar.multiselect(
    "👨‍🏫 Teacher Expertise",
    expertise_list,
    default=expertise_list
)

# ---------------------------------------------------------
# PAYMENT FILTER
# ---------------------------------------------------------

payment_list = sorted(
    df["PaymentMethod"].dropna().unique().tolist()
)

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    payment_list,
    default=payment_list
)

# ---------------------------------------------------------
# TEACHER RATING FILTER
# ---------------------------------------------------------

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
    value=(rating_min, rating_max)
)

# ---------------------------------------------------------
# EXPERIENCE FILTER
# ---------------------------------------------------------

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

# =========================================================
# APPLY FILTERS
# =========================================================

filtered = df[
    (df["CourseCategory"].isin(selected_category))
    &
    (df["CourseLevel"].isin(selected_level))
    &
    (df["Expertise"].isin(selected_expertise))
    &
    (df["PaymentMethod"].isin(selected_payment))
    &
    (df["TeacherRating"] >= selected_rating[0])
    &
    (df["TeacherRating"] <= selected_rating[1])
    &
    (df["YearsOfExperience"] >= selected_experience[0])
    &
    (df["YearsOfExperience"] <= selected_experience[1])
].copy()

# =========================================================
# EMPTY FILTER CHECK
# =========================================================

if filtered.empty:

    st.warning(
        "⚠️ No data found for the selected filters. "
        "Please change the filters."
    )

    st.stop()

# =========================================================
# KPI SECTION
# =========================================================

st.header("📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "👨‍🏫 Total Teachers",
        filtered["TeacherID"].nunique()
    )

with col2:
    st.metric(
        "📚 Total Courses",
        filtered["CourseID"].nunique()
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
        f"₹{filtered['Amount'].sum():,.2f}"
    )

with col6:
    st.metric(
        "📝 Total Transactions",
        filtered["TransactionID"].nunique()
    )

with col7:
    st.metric(
        "📈 Avg Experience",
        f"{filtered['YearsOfExperience'].mean():.1f} Years"
    )

st.markdown("---")

# =========================================================
# INSTRUCTOR PERFORMANCE
# =========================================================

st.header("👨‍🏫 Instructor Performance Analysis")

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# TEACHER RATING DISTRIBUTION
# ---------------------------------------------------------

with col1:

    st.subheader("⭐ Teacher Rating Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        filtered["TeacherRating"].dropna(),
        bins=10,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("Teacher Rating")
    ax.set_ylabel("Number of Records")

    st.pyplot(fig)

    plt.close(fig)

# ---------------------------------------------------------
# EXPERIENCE VS TEACHER RATING
# ---------------------------------------------------------

with col2:

    st.subheader("📈 Experience vs Teacher Rating")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.scatterplot(
        data=filtered,
        x="YearsOfExperience",
        y="TeacherRating",
        ax=ax
    )

    ax.set_xlabel("Years of Experience")
    ax.set_ylabel("Teacher Rating")

    st.pyplot(fig)

    plt.close(fig)

# =========================================================
# TEACHER RATING VS COURSE RATING
# =========================================================

st.subheader("🎯 Teacher Rating vs Course Rating")

fig, ax = plt.subplots(figsize=(10, 5))

sns.scatterplot(
    data=filtered,
    x="TeacherRating",
    y="CourseRating",
    hue="CourseCategory",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Course Rating")

st.pyplot(fig)

plt.close(fig)

# =========================================================
# COURSE QUALITY
# =========================================================

st.header("📚 Course Quality Analysis")

col1, col2 = st.columns(2)

# ---------------------------------------------------------
# COURSE RATING DISTRIBUTION
# ---------------------------------------------------------

with col1:

    st.subheader("🌟 Course Rating Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.histplot(
        filtered["CourseRating"].dropna(),
        bins=10,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("Course Rating")
    ax.set_ylabel("Number of Courses")

    st.pyplot(fig)

    plt.close(fig)

# ---------------------------------------------------------
# CATEGORY RATING
# ---------------------------------------------------------

with col2:

    st.subheader("📚 Average Course Rating by Category")

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

    st.pyplot(fig)

    plt.close(fig)

# =========================================================
# COURSE LEVEL
# =========================================================

st.subheader("🎓 Course Rating by Course Level")

fig, ax = plt.subplots(figsize=(10, 5))

sns.boxplot(
    data=filtered,
    x="CourseLevel",
    y="CourseRating",
    ax=ax
)

ax.set_xlabel("Course Level")
ax.set_ylabel("Course Rating")

st.pyplot(fig)

plt.close(fig)

# =========================================================
# EXPERTISE ANALYSIS
# =========================================================

st.header("🎯 Expertise-Based Performance")

expertise_rating = (
    filtered
    .groupby("Expertise")["TeacherRating"]
    .mean()
    .sort_values(ascending=False)
)

fig, ax = plt.subplots(figsize=(10, 5))

expertise_rating.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Teacher Expertise")
ax.set_ylabel("Average Teacher Rating")

plt.xticks(rotation=45)

st.pyplot(fig)

plt.close(fig)

# =========================================================
# INSTRUCTOR LEADERBOARD
# =========================================================

st.header("🏆 Instructor Performance Leaderboard")

teacher_summary = (
    filtered
    .groupby("TeacherName")
    .agg(
        TeacherRating=("TeacherRating", "mean"),
        CourseRating=("CourseRating", "mean"),
        Experience=("YearsOfExperience", "mean"),
        Enrollments=("TransactionID", "count")
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
    use_container_width=True
)

st.subheader("📉 Bottom 10 Instructors")

st.dataframe(
    teacher_summary.tail(10).sort_values(
        "TeacherRating"
    ).round(2),
    use_container_width=True
)

# =========================================================
# ENROLLMENT INFLUENCE
# =========================================================

st.header("📊 Instructor Rating vs Enrollments")

rating_enrollment = (
    filtered
    .groupby("TeacherRating")["TransactionID"]
    .count()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(10, 5))

rating_enrollment.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Number of Enrollments")

st.pyplot(fig)

plt.close(fig)

# =========================================================
# PAYMENT METHOD
# =========================================================

st.header("💳 Transaction Analysis")

col1, col2 = st.columns(2)

with col1:

    st.subheader("Payment Method Distribution")

    fig, ax = plt.subplots(figsize=(8, 5))

    sns.countplot(
        data=filtered,
        x="PaymentMethod",
        ax=ax
    )

    ax.set_xlabel("Payment Method")
    ax.set_ylabel("Transactions")

    plt.xticks(rotation=45)

    st.pyplot(fig)

    plt.close(fig)

# =========================================================
# REVENUE BY CATEGORY
# =========================================================

with col2:

    st.subheader("💰 Revenue by Course Category")

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

    st.pyplot(fig)

    plt.close(fig)

# =========================================================
# MONTHLY REVENUE
# =========================================================

st.header("📅 Revenue Trend Analysis")

monthly_revenue = (
    filtered
    .dropna(subset=["TransactionDate"])
    .groupby(
        filtered.dropna(
            subset=["TransactionDate"]
        )["TransactionDate"].dt.to_period("M")
    )["Amount"]
    .sum()
)

monthly_revenue.index = monthly_revenue.index.astype(str)

st.line_chart(
    monthly_revenue
)

# =========================================================
# CORRELATION HEATMAP
# =========================================================

st.header("🔥 Correlation Analysis")

correlation_columns = [
    "TeacherRating",
    "CourseRating",
    "YearsOfExperience",
    "CoursePrice",
    "CourseDuration",
    "Amount"
]

corr = filtered[
    correlation_columns
].corr()

fig, ax = plt.subplots(figsize=(9, 6))

sns.heatmap(
    corr,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig)

plt.close(fig)

# =========================================================
# RATING CONSISTENCY INDEX
# =========================================================

st.header("📏 Rating Consistency Analysis")

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

consistency = consistency.sort_values(
    "RatingConsistencyIndex",
    ascending=False
)

st.dataframe(
    consistency.head(10).round(3),
    use_container_width=True
)

# =========================================================
# EXPERIENCE IMPACT SCORE
# =========================================================

st.header("📈 Experience Impact Score")

experience_correlation = filtered[
    [
        "YearsOfExperience",
        "TeacherRating"
    ]
].corr().iloc[0, 1]

st.metric(
    "Experience Impact Score",
    f"{experience_correlation:.3f}"
)

if experience_correlation >= 0.5:

    st.success(
        "Strong positive relationship between teaching "
        "experience and teacher rating."
    )

elif experience_correlation >= 0.2:

    st.info(
        "Moderate positive relationship between teaching "
        "experience and teacher rating."
    )

elif experience_correlation >= -0.2:

    st.warning(
        "Weak relationship between teaching experience "
        "and teacher rating."
    )

else:

    st.error(
        "Negative relationship between teaching experience "
        "and teacher rating."
    )

# =========================================================
# DATASET
# =========================================================

st.header("📋 Filtered Dataset")

st.dataframe(
    filtered,
    use_container_width=True
)

# =========================================================
# DOWNLOAD
# =========================================================

csv = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv,
    file_name="EduPro_Filtered_Data.csv",
    mime="text/csv"
)

# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center;">
        <h4>🎓 EduPro Instructor Performance & Course Quality Evaluation</h4>
        <p>Unified Mentor Data Analytics Project</p>
    </div>
    """,
    unsafe_allow_html=True
)

