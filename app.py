import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ΔΙ.ΠΑ.Ε. Ανάλυση 2024–2025", layout="wide")

# === Εικόνα λογοτύπου ===
st.image("dipaelogo.png", width=200)

st.title("📊 Ανάλυση Εισακτέων ΔΙ.ΠΑ.Ε. 2024–2025")

# === Φόρτωση δεδομένων ===
df = pd.read_csv("dipae_analysis_2024_2025.csv")

# === Sidebar φίλτρα ===
st.sidebar.header("🔍 Φίλτρα")
search = st.sidebar.text_input("Αναζήτηση Τμήματος")

# Μετατροπή "Κάλυψη" σε αριθμούς για φιλτράρισμα
df["Κάλυψη_2025"] = pd.to_numeric(df["Κάλυψη_2025"], errors="coerce")
df["Κάλυψη_2024"] = pd.to_numeric(df["Κάλυψη_2024"], errors="coerce")
df["Θέσεις_2025"] = pd.to_numeric(df["Θέσεις_2025"], errors="coerce")
df["Θέσεις_2024"] = pd.to_numeric(df["Θέσεις_2024"], errors="coerce")
df["Επιτυχόντες_2025"] = pd.to_numeric(df["Επιτυχόντες_2025"], errors="coerce")
df["Επιτυχόντες_2024"] = pd.to_numeric(df["Επιτυχόντες_2024"], errors="coerce")

# Στρογγυλοποίηση ποσοστών κάλυψης σε 2 δεκαδικά
df["Κάλυψη_2025"] = df["Κάλυψη_2025"].round(2)
df["Κάλυψη_2024"] = df["Κάλυψη_2024"].round(2)

# Φιλτράρισμα δεδομένων
if search:
    df_filtered = df[df["ΟΝΟΜΑ ΣΧΟΛΗΣ"].str.contains(search, case=False, na=False)]
else:
    df_filtered = df.copy()

# === Tabs ===
tab1, tab2, tab3, tab4 = st.tabs([
    "📋 Πίνακας Τμημάτων", "📈 Σύγκριση Κάλυψης", "📊 Μόρια & Βάσεις", "📑 Στοιχεία ανά Τμήμα"
])

with tab1:
    st.subheader("📋 Πίνακας Τμημάτων ΔΙ.ΠΑ.Ε.")
    display_cols = [
        "ΟΝΟΜΑ ΣΧΟΛΗΣ",
        "Θέσεις_2025", "Επιτυχόντες_2025", "Κάλυψη_2025",
        "Θέσεις_2024", "Επιτυχόντες_2024", "Κάλυψη_2024",
        "Μόρια_Πρώτου_2025", "Βάση_2025",
        "Μόρια_Πρώτου_2024", "Βάση_2024"
    ]
    st.dataframe(df_filtered[display_cols], use_container_width=True)

    # Προβολή συνόλων για Θέσεις και Επιτυχόντες
    total_2025_positions = df_filtered["Θέσεις_2025"].sum()
    total_2025_success = df_filtered["Επιτυχόντες_2025"].sum()
    total_2024_positions = df_filtered["Θέσεις_2024"].sum()
    total_2024_success = df_filtered["Επιτυχόντες_2024"].sum()

    st.markdown("### 📌 Σύνολα")
    st.markdown(f"**2025:** Θέσεις: {int(total_2025_positions)}, Επιτυχόντες: {int(total_2025_success)}")
    st.markdown(f"**2024:** Θέσεις: {int(total_2024_positions)}, Επιτυχόντες: {int(total_2024_success)}")

    # Γράφημα Επιτυχόντων
    st.subheader("📊 Σύγκριση Επιτυχόντων 2024 vs 2025")
    fig_success = px.bar(df_filtered, x="ΟΝΟΜΑ ΣΧΟΛΗΣ",
                         y=["Επιτυχόντες_2024", "Επιτυχόντες_2025"],
                         barmode="group",
                         labels={"value": "Επιτυχόντες", "variable": "Έτος"}, height=600)
    st.plotly_chart(fig_success, use_container_width=True)

with tab2:
    st.subheader("📈 Σύγκριση Ποσοστού Κάλυψης Θέσεων")
    chart_df = df_filtered.dropna(subset=["Κάλυψη_2024", "Κάλυψη_2025"])
    fig = px.bar(chart_df, x="ΟΝΟΜΑ ΣΧΟΛΗΣ", y=["Κάλυψη_2024", "Κάλυψη_2025"], barmode="group",
                 labels={"value": "Ποσοστό Κάλυψης", "variable": "Έτος"}, height=600)
    st.plotly_chart(fig, use_container_width=True)

with tab3:
    st.subheader("🎯 Βάσεις Εισαγωγής (Τελευταίου)")
    df_vaseis = df_filtered.dropna(subset=["Βάση_2024", "Βάση_2025"])
    fig3 = px.bar(df_vaseis, x="ΟΝΟΜΑ ΣΧΟΛΗΣ", 
                  y=["Βάση_2024", "Βάση_2025"], barmode="group",
                  labels={"value": "Βάση Τελευταίου", "variable": "Έτος"}, height=600)
    st.plotly_chart(fig3, use_container_width=True)

with tab4:
    st.subheader("📑 Στοιχεία ανά Τμήμα")
    selected_dept = st.selectbox("Επιλέξτε Τμήμα", df_filtered["ΟΝΟΜΑ ΣΧΟΛΗΣ"].unique())
    row = df_filtered[df_filtered["ΟΝΟΜΑ ΣΧΟΛΗΣ"] == selected_dept].iloc[0]

    st.markdown(f"### {selected_dept}")

    table_data = {
        "Κατηγορία": [
            "Θέσεις", "Επιτυχόντες", "Κάλυψη (%)", "Μόρια Πρώτου", "Βάση"
        ],
        "2024": [
            int(row['Θέσεις_2024']),
            int(row['Επιτυχόντες_2024']),
            f"{row['Κάλυψη_2024']:.2f}%",
            row['Μόρια_Πρώτου_2024'],
            row['Βάση_2024']
        ],
        "2025": [
            int(row['Θέσεις_2025']),
            int(row['Επιτυχόντες_2025']),
            f"{row['Κάλυψη_2025']:.2f}%",
            row['Μόρια_Πρώτου_2025'],
            row['Βάση_2025']
        ],
        "Διαφορά": [
            int(row['Θέσεις_2025'] - row['Θέσεις_2024']),
            int(row['Επιτυχόντες_2025'] - row['Επιτυχόντες_2024']),
            f"{(row['Κάλυψη_2025'] - row['Κάλυψη_2024']):.2f}%",
            row['Μόρια_Πρώτου_2025'] - row['Μόρια_Πρώτου_2024'],
            row['Βάση_2025'] - row['Βάση_2024']
        ]
    }

    st.table(pd.DataFrame(table_data))

    if pd.notna(row["Ιστοσελίδα Τμήματος"]):
        st.markdown(f"[🔗 Επίσκεψη στην Ιστοσελίδα]({row['Ιστοσελίδα Τμήματος']})")
