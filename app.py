import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="ΔΙ.ΠΑ.Ε. Ανάλυση 2024–2025", layout="wide")

# === Εικόνα λογοτύπου ===
st.image("dipaelogo.png", width=200)

st.title("📊 Ανάλυση Εισακτέων ΔΙ.ΠΑ.Ε. 2024–2025")

# === Φόρτωση δεδομένων ===
df = pd.read_csv("dipae_analysis_2024_2025.csv")

# === Αφαίρεση μη έγκυρων τμημάτων ===
df = df.iloc[:23]  # Διατήρηση μόνο των 23 κανονικών τμημάτων

# Υπολογισμός στήλης διαφοράς βάσης (πριν από φιλτράρισμα)
df["Διαφορά_Βάσης"] = df["Βάση_2025"] - df["Βάση_2024"]

# === Sidebar φίλτρα ===
st.sidebar.header("🔍 Φίλτρα")
search = st.sidebar.text_input("Αναζήτηση Τμήματος")

st.sidebar.image("modip100v2-1.png", use_container_width=True)



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
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📋 Πίνακας Τμημάτων", "📈 Σύγκριση Κάλυψης", "📊 Μόρια & Βάσεις", "📑 Στοιχεία ανά Τμήμα", "🏆 Top-5"
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

    total_2025_positions = df_filtered["Θέσεις_2025"].sum()
    total_2025_success = df_filtered["Επιτυχόντες_2025"].sum()
    total_2024_positions = df_filtered["Θέσεις_2024"].sum()
    total_2024_success = df_filtered["Επιτυχόντες_2024"].sum()

    st.markdown("<span style='font-size: 0.85em; color: gray;'>Οι θέσεις και οι επιτυχόντες είναι από όλες τις κατηγορίες</span>", unsafe_allow_html=True)


    st.markdown("### 📌 Σύνολα")
    st.markdown(f"**2025:** Θέσεις: {int(total_2025_positions)}, Επιτυχόντες: {int(total_2025_success)}")
    st.markdown(f"**2024:** Θέσεις: {int(total_2024_positions)}, Επιτυχόντες: {int(total_2024_success)}")

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

    st.markdown("<span style='font-size: 0.85em; color: gray;'>Οι θέσεις και οι επιτυχόντες είναι από όλες τις κατηγορίες</span>", unsafe_allow_html=True)

    if pd.notna(row["Ιστοσελίδα Τμήματος"]):
        st.markdown(f"[🔗 Επίσκεψη στην Ιστοσελίδα]({row['Ιστοσελίδα Τμήματος']})")

    st.markdown("### 📊 Γραφήματα Σύγκρισης για το Τμήμα")
    fig_s1 = px.bar(
        x=["2024", "2025"],
        y=[row['Επιτυχόντες_2024'], row['Επιτυχόντες_2025']],
        labels={"x": "Έτος", "y": "Επιτυχόντες"},
        title="Σύγκριση Επιτυχόντων",
        text=[row['Επιτυχόντες_2024'], row['Επιτυχόντες_2025']]
    )
    fig_s1.update_traces(textposition='outside')
    fig_s1.update_layout(xaxis=dict(tickmode='array', tickvals=["2024", "2025"]))

    fig_s2 = px.bar(
        x=["2024", "2025"],
        y=[row['Κάλυψη_2024'], row['Κάλυψη_2025']],
        labels={"x": "Έτος", "y": "Κάλυψη %"},
        title="Σύγκριση Ποσοστού Κάλυψης",
        text=[f"{row['Κάλυψη_2024']:.2f}%", f"{row['Κάλυψη_2025']:.2f}%"]
    )
    fig_s2.update_traces(textposition='outside')
    fig_s2.update_layout(xaxis=dict(tickmode='array', tickvals=["2024", "2025"]))

    fig_s3 = px.bar(
        x=["2024", "2025"],
        y=[row['Βάση_2024'], row['Βάση_2025']],
        labels={"x": "Έτος", "y": "Βάση"},
        title="Σύγκριση Βάσης Εισαγωγής",
        text=[row['Βάση_2024'], row['Βάση_2025']]
    )
    fig_s3.update_traces(textposition='outside')
    fig_s3.update_layout(xaxis=dict(tickmode='array', tickvals=["2024", "2025"]))

    st.plotly_chart(fig_s1, use_container_width=True)
    st.plotly_chart(fig_s2, use_container_width=True)
    st.plotly_chart(fig_s3, use_container_width=True)

with tab5:
    st.subheader("🏆 Top-5 Κατηγορίες")

    top_base = df_filtered.sort_values(by="Βάση_2025", ascending=False).head(5)
    st.markdown("### 📌 Μεγαλύτερη Βάση Εισαγωγής 2025")
    st.dataframe(top_base[["ΟΝΟΜΑ ΣΧΟΛΗΣ", "Βάση_2025"]], use_container_width=True)
    fig1 = px.bar(top_base, x="ΟΝΟΜΑ ΣΧΟΛΗΣ", y="Βάση_2025", title="Top-5 Βάσεις 2025",
                 range_y=[0, 20000], height=450)
    st.plotly_chart(fig1, use_container_width=True)

    top_increase = df_filtered.sort_values(by="Διαφορά_Βάσης", ascending=False).head(5)
    st.markdown("### 📈 Μεγαλύτερη Αύξηση Βάσης Εισαγωγής (2025 vs 2024)")
    st.dataframe(
        top_increase[["ΟΝΟΜΑ ΣΧΟΛΗΣ", "Βάση_2024", "Βάση_2025", "Διαφορά_Βάσης"]],
        use_container_width=True,
        column_config={
            "Διαφορά_Βάσης": st.column_config.NumberColumn(
                "Διαφορά Βάσης",
                help="Αύξηση ή μείωση βάσης 2025 σε σχέση με 2024",
                format="%.0f",
                min_value=int(top_increase["Διαφορά_Βάσης"].min()),
                max_value=int(top_increase["Διαφορά_Βάσης"].max()),
                step=1
            )
        },
        hide_index=True
    )
    fig2 = px.bar(top_increase, x="ΟΝΟΜΑ ΣΧΟΛΗΣ", y="Διαφορά_Βάσης", title="Top-5 Αύξηση Βάσης", height=450)
    st.plotly_chart(fig2, use_container_width=True)

    exclude_keywords = ["ΣΥΝΟΛΟ", "ΜΑΧ"]
    top_success = df_filtered[~df_filtered["ΟΝΟΜΑ ΣΧΟΛΗΣ"].str.upper().isin(exclude_keywords)]
    top_success = top_success.sort_values(by="Επιτυχόντες_2025", ascending=False).head(5)

    st.markdown("### 🧑‍🎓 Περισσότεροι Επιτυχόντες 2025")
    st.dataframe(top_success[["ΟΝΟΜΑ ΣΧΟΛΗΣ", "Επιτυχόντες_2025"]], use_container_width=True)
    fig3 = px.bar(top_success, x="ΟΝΟΜΑ ΣΧΟΛΗΣ", y="Επιτυχόντες_2025",
                  title="Top-5 Επιτυχόντες 2025", height=450)
    st.plotly_chart(fig3, use_container_width=True)
