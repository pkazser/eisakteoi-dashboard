import streamlit as st
import pandas as pd
import plotly.express as px
from st_aggrid import AgGrid, GridOptionsBuilder

# === Ρυθμίσεις σελίδας ===
st.set_page_config(page_title="Εισακτέοι 2025 - Dashboard", layout="wide")

# === Φόρτωση δεδομένων ===
df = pd.read_csv("eisakteoi_2025_dashboard_with_coords.csv")

# === Sidebar φίλτρα ===
st.sidebar.header("🔍 Φίλτρα")
search = st.sidebar.text_input("Αναζήτηση Τμήματος")
min_coverage = st.sidebar.slider("Ελάχιστο ποσοστό κάλυψης", 0, 100, 0)

df_filtered = df[df["ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ"].astype(float) >= min_coverage]
if search:
    df_filtered = df_filtered[df_filtered["Τμήμα"].str.contains(search, case=False, na=False)]

# Απόκρυψη συντεταγμένων από τον πίνακα
df_table = df_filtered.drop(columns=["Latitude", "Longitude"], errors="ignore")

# === Tabs ===
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Πίνακας", "📈 Γραφήματα", "🗺️ Χάρτης Τμημάτων", "📥 Εξαγωγή", "📊 Συγκεντρωτικός Πίνακας"])

with tab1:
    st.subheader("📋 Διαδραστικός Πίνακας Τμημάτων")
    selected_row = st.selectbox("Επιλέξτε Τμήμα", df_filtered["Τμήμα"].unique())
    selected_data = df_filtered[df_filtered["Τμήμα"] == selected_row].iloc[0]

    col1, col2 = st.columns([2, 3])

    with col1:
        st.markdown("### 📍 Στοιχεία Τμήματος")
        st.markdown(f"**Τμήμα:** {selected_data['Τμήμα']}")
        st.markdown(f"**Ποσοστό Κάλυψης Θέσεων:** {selected_data['ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ']}%")
        st.markdown(f"**Μόρια Πρώτου ΓΕΛ:** {selected_data['Μόρια Πρώτου ΓΕΛ']}")
        st.markdown(f"**Μόρια Τελευταίου ΓΕΛ:** {selected_data['Μόρια Τελευταίου ΓΕΛ']}")
        st.markdown(f"**Βάση ΓΕΛ 2025:** {selected_data['Βάση ΓΕΛ 2025']}")
        st.markdown("[🌐 Επίσκεψη στην ιστοσελίδα του ΔΙΠΑΕ](https://www.dipae.gr)")

    with col2:
        st.map(pd.DataFrame({"latitude": [selected_data["Latitude"]], "longitude": [selected_data["Longitude"]]}), zoom=14)

with tab2:
    st.subheader("📈 Ποσοστά Κάλυψης Θέσεων")
    fig1 = px.bar(df_filtered.sort_values("ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ", ascending=False),
                  x="Τμήμα", y="ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ", height=500,
                  labels={"ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ": "Ποσοστό Κάλυψης (%)"})
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("🏅 Μόρια Πρώτου Εισακτέου (ΓΕΛ)")
    fig2 = px.bar(df_filtered.sort_values("Μόρια Πρώτου ΓΕΛ", ascending=False),
                  x="Τμήμα", y="Μόρια Πρώτου ΓΕΛ", height=500)
    st.plotly_chart(fig2, use_container_width=True)

with tab3:
    st.subheader("🗺️ Χάρτης Τμημάτων")
    df_map = df_filtered.rename(columns={"Latitude": "latitude", "Longitude": "longitude"}).copy()
    df_map["latitude"] = pd.to_numeric(df_map["latitude"], errors="coerce")
    df_map["longitude"] = pd.to_numeric(df_map["longitude"], errors="coerce")
    df_map = df_map.dropna(subset=["latitude", "longitude"])
    st.map(df_map[["latitude", "longitude"]], zoom=7)

with tab4:
    st.subheader("📥 Εξαγωγή Δεδομένων")
    st.download_button("⬇ Κατέβασε CSV Φίλτρου", df_filtered.to_csv(index=False), file_name="filtered_data.csv")
    st.dataframe(df_table)

with tab5:
    st.subheader("📊 Συγκεντρωτικός Πίνακας Τμημάτων")
    summary_cols = ["Τμήμα", "ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ", "Μόρια Πρώτου ΓΕΛ", "Μόρια Τελευταίου ΓΕΛ", "Βάση ΓΕΛ 2025"]
    df_summary = df[summary_cols].copy()
    st.dataframe(df_summary.sort_values("ΠΟΣΟΣΤΟ ΚΑΛΥΨΗΣ ΘΕΣΕΩΝ", ascending=False), use_container_width=True)
