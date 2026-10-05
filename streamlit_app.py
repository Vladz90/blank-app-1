import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Set page title
st.set_page_config(page_title="Water Quality Analysis", layout="centered")

# Language selector
language = st.sidebar.selectbox("Select Language / Pilih Bahasa", ["English", "Bahasa Melayu"])

# Dictionary for translations
TEXT = {
    "title": {
        "English": "💧 Water Quality Analysis Dashboard",
        "Bahasa Melayu": "💧 Papan Pemuka Analisis Kualiti Air"
    },
    "upload": {
        "English": "Upload Water Quality CSV",
        "Bahasa Melayu": "Muat naik fail CSV Kualiti Air"
    },
    "raw_data": {
        "English": "📄 Raw Data",
        "Bahasa Melayu": "📄 Data Mentah"
    },
    "classification": {
        "English": "✅ Water Quality Classification",
        "Bahasa Melayu": "✅ Klasifikasi Kualiti Air"
    },
    "summary": {
        "English": "📊 Summary",
        "Bahasa Melayu": "📊 Ringkasan"
    },
    "scatter": {
        "English": "📈 pH vs Turbidity Scatter Plot",
        "Bahasa Melayu": "📈 Plot Taburan pH vs Kekeruhan"
    },
    "missing_cols": {
        "English": "CSV must include 'pH', 'Turbidity', and 'TDS' columns.",
        "Bahasa Melayu": "Fail CSV mesti mengandungi lajur 'pH', 'Turbidity', dan 'TDS'."
    },
    "upload_prompt": {
        "English": "Please upload a CSV file to begin.",
        "Bahasa Melayu": "Sila muat naik fail CSV untuk bermula."
    }
}

# App title
st.title(TEXT["title"][language])

# Upload CSV
uploaded_file = st.file_uploader(TEXT["upload"][language], type=["csv"])

# Dummy rule-based predictor
def classify_water(row):
    if row['pH'] >= 6.5 and row['pH'] <= 8.5 and row['Turbidity'] < 5 and row['TDS'] < 500:
        return "Safe" if language == "English" else "Selamat"
    else:
        return "Unsafe" if language == "English" else "Tidak Selamat"

# Main logic
if uploaded_file:
    df = pd.read_csv(uploaded_file)

    st.subheader(TEXT["raw_data"][language])
    st.dataframe(df)

    if all(col in df.columns for col in ['pH', 'Turbidity', 'TDS']):
        df['Water Quality'] = df.apply(classify_water, axis=1)

        st.subheader(TEXT["classification"][language])
        st.dataframe(df[['pH', 'Turbidity', 'TDS', 'Water Quality']])

        # Count of classifications
        counts = df['Water Quality'].value_counts()
        st.subheader(TEXT["summary"][language])
        st.bar_chart(counts)

        # Scatter plot
        st.subheader(TEXT["scatter"][language])
        fig, ax = plt.subplots()
        scatter = ax.scatter(df['pH'], df['Turbidity'], c=(df['Water Quality'] == ("Safe" if language == "English" else "Selamat")).astype(int), cmap='coolwarm')
        ax.set_xlabel("pH")
        ax.set_ylabel("Turbidity")
        st.pyplot(fig)
    else:
        st.warning(TEXT["missing_cols"][language])
else:
    st.info(TEXT["upload_prompt"][language])
