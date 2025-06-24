import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

st.set_page_config(page_title="CSV Data Analyzer", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("📂 CSV Analyzer Controls")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)

    # ---------- SIDEBAR FILTERING ----------
    st.sidebar.subheader("🔍 Filter Data")
    filter_cols = df.select_dtypes(include=['object']).columns.tolist()
    for col in filter_cols:
        unique_vals = df[col].dropna().unique().tolist()
        selected_vals = st.sidebar.multiselect(f"Filter by {col}", unique_vals)
        if selected_vals:
            df = df[df[col].isin(selected_vals)]

    # ---------- MAIN CONTENT ----------
    st.title("📊 CSV Data Analyzer")
    st.markdown("Analyze, filter, visualize and export your CSV data easily.")

    # ---------- METRICS ----------
    st.subheader("📈 Quick Data Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Rows", df.shape[0])
    col2.metric("Total Columns", df.shape[1])
    col3.metric("Missing Values", df.isnull().sum().sum())



    # ---------- TABS ----------
    tab1, tab2, tab3, tab4 = st.tabs(["🧾 Data Preview", "📊 Charts", "📉 Correlation", "📥 Export"])

    with tab1:
        st.subheader("🔎 Preview Your Data")
        st.dataframe(df)

        st.subheader("📋 Summary Statistics")
        st.write(df.describe(include='all'))

    with tab2:
        st.subheader("📊 Visualizations")
        numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()

        if numeric_cols:
            selected_col = st.selectbox("Select numeric column", numeric_cols)
            chart_type = st.radio("Choose chart type", ["Histogram", "Boxplot", "Line Chart", "Pie Chart"])

            fig, ax = plt.subplots()

            if chart_type == "Histogram":
                ax.hist(df[selected_col].dropna(), bins=20, color='skyblue', edgecolor='black')
                ax.set_title(f"Histogram of {selected_col}")

            elif chart_type == "Boxplot":
                ax.boxplot(df[selected_col].dropna())
                ax.set_title(f"Boxplot of {selected_col}")

            elif chart_type == "Line Chart":
                ax.plot(df[selected_col].dropna())
                ax.set_title(f"Line Chart of {selected_col}")

            elif chart_type == "Pie Chart":
                value_counts = df[selected_col].value_counts().head(10)
                ax.pie(value_counts, labels=value_counts.index, autopct='%1.1f%%')
                ax.set_title(f"Top 10 values in {selected_col}")

            st.pyplot(fig)
        else:
            st.warning("No numeric columns available to plot.")

    with tab3:
        st.subheader("📉 Correlation Heatmap")
        numeric_df = df.select_dtypes(include=['float64', 'int64'])

        if numeric_df.shape[1] >= 2:
            fig, ax = plt.subplots(figsize=(10, 6))
            sns.heatmap(numeric_df.corr(), annot=True, cmap='coolwarm', ax=ax)
            st.pyplot(fig)
        else:
            st.warning("Need at least two numeric columns for correlation heatmap.")

    with tab4:
        st.subheader("📥 Download Filtered Data")
        csv_buffer = io.StringIO()
        df.to_csv(csv_buffer, index=False)
        st.download_button(
            label="Download CSV",
            data=csv_buffer.getvalue(),
            file_name="filtered_data.csv",
            mime="text/csv"
        )

else:
    st.title("📊 CSV Data Analyzer")
    st.info("Upload a CSV file from the sidebar to begin.")
