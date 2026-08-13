import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# ==========================================================
# PAGE CONFIGURATION
# ==========================================================

st.set_page_config(
    page_title="EduPro | Instructor Analytics",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==========================================================
# CUSTOM CSS
# ==========================================================

st.markdown("""
<style>

.main {
    background-color: #f7f9fc;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.dashboard-title {
    font-size: 38px;
    font-weight: 700;
    text-align: center;
    margin-bottom: 5px;
}

.dashboard-subtitle {
    text-align: center;
    color: #6b7280;
    font-size: 17px;
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
    padding: 18px;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    box-shadow: 0px 2px 8px rgba(0,0,0,0.05);
}

[data-testid="stSidebar"] {
    background-color: #f8fafc;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# HEADER
# ==========================================================

st.markdown(
    '<div class="dashboard-title">🎓 EduPro Analytics</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="dashboard-subtitle">'
    'Instructor Performance & Course Quality Evaluation'
    '</div>',
    unsafe_allow_html=True
)

# ==========================================================
# LOAD DATA
# ==========================================================

@st.cache_data
def load_data():

    data = pd.read_csv("EduPro_Final_Dataset.csv")

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
        if column in data.columns:
            data[column] = pd.to_numeric(
                data[column],
                errors="coerce"
            )

    if "TransactionDate" in data.columns:
        data["TransactionDate"] = pd.to_datetime(
            data["TransactionDate"],
            errors="coerce"
        )

    return data


df = load_data()

# ==========================================================
# DATA VALIDATION
# ==========================================================

required_columns = [
    "TransactionID",
    "CourseID",
    "TeacherID",
    "CourseCategory",
    "CourseLevel",
    "PaymentMethod",
    "Expertise",
    "CourseRating",
    "TeacherRating",
    "YearsOfExperience",
    "TeacherName",
    "Amount",
    "TransactionDate"
]

missing_columns = [
    column for column in required_columns
    if column not in df.columns
]

if missing_columns:

    st.error("The following required columns are missing:")

    st.write(missing_columns)

    st.stop()

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.title("🎛️ Dashboard Controls")

st.sidebar.markdown(
    "Use the filters below to explore instructor and course performance."
)

# ----------------------------------------------------------
# CATEGORY
# ----------------------------------------------------------

category_options = sorted(
    df["CourseCategory"].dropna().unique().tolist()
)

selected_category = st.sidebar.multiselect(
    "📚 Course Category",
    options=category_options,
    default=category_options
)

# ----------------------------------------------------------
# COURSE LEVEL
# ----------------------------------------------------------

level_options = sorted(
    df["CourseLevel"].dropna().unique().tolist()
)

selected_level = st.sidebar.multiselect(
    "🎓 Course Level",
    options=level_options,
    default=level_options
)

# ----------------------------------------------------------
# EXPERTISE
# ----------------------------------------------------------

expertise_options = sorted(
    df["Expertise"].dropna().unique().tolist()
)

selected_expertise = st.sidebar.multiselect(
    "👨‍🏫 Instructor Expertise",
    options=expertise_options,
    default=expertise_options
)

# ----------------------------------------------------------
# PAYMENT
# ----------------------------------------------------------

payment_options = sorted(
    df["PaymentMethod"].dropna().unique().tolist()
)

selected_payment = st.sidebar.multiselect(
    "💳 Payment Method",
    options=payment_options,
    default=payment_options
)

# ----------------------------------------------------------
# RATING
# ----------------------------------------------------------

rating_min = float(df["TeacherRating"].min())
rating_max = float(df["TeacherRating"].max())

selected_rating = st.sidebar.slider(
    "⭐ Teacher Rating Range",
    min_value=rating_min,
    max_value=rating_max,
    value=(rating_min, rating_max),
    step=0.1
)

# ----------------------------------------------------------
# EXPERIENCE
# ----------------------------------------------------------

experience_min = int(
    df["YearsOfExperience"].min()
)

experience_max = int(
    df["YearsOfExperience"].max()
)

selected_experience = st.sidebar.slider(
    "📈 Experience Range",
    min_value=experience_min,
    max_value=experience_max,
    value=(experience_min, experience_max)
)

# ==========================================================
# APPLY FILTERS
# ==========================================================

filtered = df[
    df["CourseCategory"].isin(selected_category)
    &
    df["CourseLevel"].isin(selected_level)
    &
    df["Expertise"].isin(selected_expertise)
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

# ==========================================================
# EMPTY DATA CHECK
# ==========================================================

if filtered.empty:

    st.warning(
        "⚠️ No records match the selected filters. "
        "Please broaden your filter selection."
    )

    st.stop()

# ==========================================================
# KPI SECTION
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Executive Overview</div>',
    unsafe_allow_html=True
)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.metric(
        "👨‍🏫 Total Instructors",
        f"{filtered['TeacherID'].nunique():,}"
    )

with k2:
    st.metric(
        "📚 Total Courses",
        f"{filtered['CourseID'].nunique():,}"
    )

with k3:
    st.metric(
        "⭐ Avg Teacher Rating",
        f"{filtered['TeacherRating'].mean():.2f}"
    )

with k4:
    st.metric(
        "🌟 Avg Course Rating",
        f"{filtered['CourseRating'].mean():.2f}"
    )

k5, k6, k7 = st.columns(3)

with k5:
    st.metric(
        "💰 Total Revenue",
        f"₹{filtered['Amount'].sum():,.0f}"
    )

with k6:
    st.metric(
        "📝 Transactions",
        f"{filtered['TransactionID'].nunique():,}"
    )

with k7:
    st.metric(
        "📈 Avg Experience",
        f"{filtered['YearsOfExperience'].mean():.1f} Years"
    )

st.markdown("---")

# ==========================================================
# INSTRUCTOR PERFORMANCE
# ==========================================================

st.markdown(
    '<div class="section-title">👨‍🏫 Instructor Performance</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# TEACHER RATING DISTRIBUTION
# ----------------------------------------------------------

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
    ax.set_ylabel("Number of Instructors")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ----------------------------------------------------------
# COURSE RATING DISTRIBUTION
# ----------------------------------------------------------

with col2:

    st.subheader("🌟 Course Rating Distribution")

    fig, ax = plt.subplots(figsize=(8, 4))

    sns.histplot(
        filtered["CourseRating"].dropna(),
        bins=10,
        kde=True,
        ax=ax
    )

    ax.set_xlabel("Course Rating")
    ax.set_ylabel("Number of Courses")

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ==========================================================
# EXPERIENCE VS TEACHER RATING
# ==========================================================

st.subheader("📈 Teaching Experience vs Teacher Rating")

fig, ax = plt.subplots(figsize=(11, 5))

sns.scatterplot(
    data=filtered,
    x="YearsOfExperience",
    y="TeacherRating",
    hue="Expertise",
    alpha=0.75,
    ax=ax
)

ax.set_xlabel("Years of Experience")
ax.set_ylabel("Teacher Rating")

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ==========================================================
# TEACHER RATING VS COURSE RATING
# ==========================================================

st.subheader("🎯 Teacher Rating vs Course Rating")

fig, ax = plt.subplots(figsize=(11, 5))

sns.scatterplot(
    data=filtered,
    x="TeacherRating",
    y="CourseRating",
    hue="CourseLevel",
    alpha=0.75,
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Course Rating")

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ==========================================================
# COURSE QUALITY
# ==========================================================

st.markdown(
    '<div class="section-title">📚 Course Quality Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# CATEGORY
# ----------------------------------------------------------

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

# ----------------------------------------------------------
# COURSE LEVEL
# ----------------------------------------------------------

with col2:

    st.subheader("🎓 Rating by Course Level")

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

# ==========================================================
# EXPERTISE PERFORMANCE
# ==========================================================

st.subheader("🎯 Expertise-wise Instructor Performance")

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

# ==========================================================
# LEADERBOARD
# ==========================================================

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

teacher_summary["TeacherRating"] = teacher_summary[
    "TeacherRating"
].round(2)

teacher_summary["CourseRating"] = teacher_summary[
    "CourseRating"
].round(2)

teacher_summary["Experience"] = teacher_summary[
    "Experience"
].round(1)

teacher_summary["Revenue"] = teacher_summary[
    "Revenue"
].round(0)

top_teachers = teacher_summary.sort_values(
    "TeacherRating",
    ascending=False
).head(10)

st.subheader("🏆 Top 10 Instructors")

st.dataframe(
    top_teachers,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# LOW PERFORMING INSTRUCTORS
# ==========================================================

st.subheader("📉 Instructors Requiring Attention")

bottom_teachers = teacher_summary.sort_values(
    "TeacherRating",
    ascending=True
).head(10)

st.dataframe(
    bottom_teachers,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# ENROLLMENT INFLUENCE
# ==========================================================

st.markdown(
    '<div class="section-title">📊 Enrollment Influence</div>',
    unsafe_allow_html=True
)

rating_enrollment = (
    filtered
    .groupby("TeacherRating")["TransactionID"]
    .count()
    .sort_index()
)

fig, ax = plt.subplots(figsize=(11, 5))

rating_enrollment.plot(
    kind="bar",
    ax=ax
)

ax.set_xlabel("Teacher Rating")
ax.set_ylabel("Number of Enrollments")

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ==========================================================
# TRANSACTION & REVENUE
# ==========================================================

st.markdown(
    '<div class="section-title">💰 Transaction & Revenue Analysis</div>',
    unsafe_allow_html=True
)

col1, col2 = st.columns(2)

# ----------------------------------------------------------
# PAYMENT METHOD
# ----------------------------------------------------------

with col1:

    st.subheader("💳 Payment Method Distribution")

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

# ----------------------------------------------------------
# REVENUE CATEGORY
# ----------------------------------------------------------

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

    st.pyplot(fig, use_container_width=True)

    plt.close(fig)

# ==========================================================
# MONTHLY REVENUE
# ==========================================================

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

# ==========================================================
# CORRELATION
# ==========================================================

st.markdown(
    '<div class="section-title">🔥 Correlation Analysis</div>',
    unsafe_allow_html=True
)

correlation_columns = [
    "TeacherRating",
    "CourseRating",
    "YearsOfExperience",
    "CoursePrice",
    "CourseDuration",
    "Amount"
]

correlation_data = filtered[
    correlation_columns
].corr()

fig, ax = plt.subplots(figsize=(9, 6))

sns.heatmap(
    correlation_data,
    annot=True,
    fmt=".2f",
    cmap="coolwarm",
    linewidths=0.5,
    ax=ax
)

st.pyplot(fig, use_container_width=True)

plt.close(fig)

# ==========================================================
# RATING CONSISTENCY INDEX
# ==========================================================

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

consistency = consistency.sort_values(
    "RatingConsistencyIndex",
    ascending=False
)

st.dataframe(
    consistency.head(10).round(3),
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# EXPERIENCE IMPACT
# ==========================================================

st.markdown(
    '<div class="section-title">📈 Experience Impact Score</div>',
    unsafe_allow_html=True
)

experience_correlation = filtered[
    ["YearsOfExperience", "TeacherRating"]
].corr().iloc[0, 1]

st.metric(
    "Experience → Teacher Rating Correlation",
    f"{experience_correlation:.3f}"
)

if experience_correlation >= 0.5:

    st.success(
        "Strong positive relationship between experience "
        "and teacher rating."
    )

elif experience_correlation >= 0.2:

    st.info(
        "Moderate positive relationship between experience "
        "and teacher rating."
    )

elif experience_correlation >= -0.2:

    st.warning(
        "Weak relationship between experience "
        "and teacher rating."
    )

else:

    st.error(
        "Negative relationship between experience "
        "and teacher rating."
    )

# ==========================================================
# EXECUTIVE INSIGHTS
# ==========================================================

st.markdown(
    '<div class="section-title">💡 Executive Insights</div>',
    unsafe_allow_html=True
)

highest_category = (
    filtered
    .groupby("CourseCategory")["CourseRating"]
    .mean()
    .idxmax()
)

highest_expertise = (
    filtered
    .groupby("Expertise")["TeacherRating"]
    .mean()
    .idxmax()
)

best_teacher = (
    teacher_summary
    .sort_values("TeacherRating", ascending=False)
    .iloc[0]["TeacherName"]
)

st.info(
    f"""
    **Key observations from the selected data:**

    • Highest-rated course category: **{highest_category}**

    • Highest-performing expertise area: **{highest_expertise}**

    • Top-rated instructor: **{best_teacher}**

    • Average teacher rating: **{filtered['TeacherRating'].mean():.2f}**

    • Average course rating: **{filtered['CourseRating'].mean():.2f}**

    • Total transactions: **{filtered['TransactionID'].nunique():,}**
    """
)

# ==========================================================
# FILTERED DATA
# ==========================================================

st.markdown(
    '<div class="section-title">📋 Filtered Dataset</div>',
    unsafe_allow_html=True
)

st.dataframe(
    filtered,
    use_container_width=True,
    hide_index=True
)

# ==========================================================
# DOWNLOAD
# ==========================================================

csv_data = filtered.to_csv(
    index=False
).encode("utf-8")

st.download_button(
    label="📥 Download Filtered Dataset",
    data=csv_data,
    file_name="EduPro_Filtered_Data.csv",
    mime="text/csv"
)

# ==========================================================
# FOOTER
# ==========================================================

st.markdown("---")

st.markdown(
    """
    <div style="text-align:center; color:#6b7280;">
        <b>🎓 EduPro Instructor Performance & Course Quality Evaluation</b><br>
        Data Analytics Project | Unified Mentor
    </div>
    """,
    unsafe_allow_html=True
)
