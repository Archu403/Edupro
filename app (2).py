import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(page_title="EduPro Dashboard", layout="wide")

df = pd.read_csv("EduPro_Final_Dataset.csv")
st.dataframe(top)
st.download_button(...)
...
st.dataframe(top)

# ============================
# Teacher Rating Distribution
# ============================

st.subheader("⭐ Teacher Rating Distribution")

fig, ax = plt.subplots(figsize=(8,4))
st.dataframe(filtered)
st.pyplot(fig)
