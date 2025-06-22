import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("📊 CSV Data Analyzer")

uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.subheader("Data Preview")
    st.write(df.head())

    st.subheader("📥 Download This Data")
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download CSV",
        data=csv,
        file_name='analyzed_data.csv',
        mime='text/csv',
    )

    st.subheader("Summary Statistics")
    st.write(df.describe())

    numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

    if numeric_cols:
        col = st.selectbox("Choose column to visualize", numeric_cols)

        st.subheader("Histogram")
        fig, ax = plt.subplots()
        ax.hist(df[col].dropna(), bins=20, color='skyblue', edgecolor='black')
        st.pyplot(fig)

        st.subheader("Box Plot")
        fig2, ax2 = plt.subplots()
        ax2.boxplot(df[col].dropna())
        st.pyplot(fig2)
    else:
        st.warning("No numeric columns found.")
