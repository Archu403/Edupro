import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

df = pd.read_csv("EduPro_Final_Dataset.csv")

st.title("Instructor Performance and Course Quality Evaluation on EduPro")

st.metric("Total Teachers", df["TeacherID"].nunique())
st.metric("Total Courses", df["CourseID"].nunique())
st.metric("Average Teacher Rating", round(df["TeacherRating"].mean(),2))
st.metric("Average Course Rating", round(df["CourseRating"].mean(),2))

st.subheader("Teacher Rating Distribution")

fig, ax = plt.subplots()
sns.histplot(df["TeacherRating"], bins=10, kde=True, ax=ax)
st.pyplot(fig)

st.subheader("Top 10 Teachers")

top = df.groupby("TeacherName")["TeacherRating"].mean().sort_values(ascending=False).head(10)

st.dataframe(top)
