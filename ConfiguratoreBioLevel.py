import streamlit as st
import pandas as pd
import altair as alt
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet

# ---------------- SESSION STATE ----------------
if "ambiente" not in st.session_state:
    st.session_state.ambiente = None
if "lambda_pannello" not in st.session_state:
    st.session_state.lambda_pannello = None
if "spessore" not in st.session_state:
    st.session_state.spessore = 100
if "intonaco" not in st.session_state:
    st.session_state.intonaco = None
if "rasante" not in st.session_state:
    st.session_state.rasante = None
if "finitura" not in st.session_state:
    st.session_state.finitura = None

# ---------------- STILE ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(to top right, #f4c303, #f47c00, #b652f4);
}
div.stButton > button {
    width: 100%;
    height: 50px;
    font-weight: bold;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOGO ----------------
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image("LogoBioLevel.png")

st.title("Configura il tuo ambiente BioLevel")

# ==================================================
# STEP 1 - AMBIENTE
# ==================================================
st.subheader("Dove vuoi isolare?")

col1, col2 = st.columns(2)

with col1:
    st.image("immagini/tetto.png")
    if st.button("TETTO"):
        st.session_state.ambiente = "Tetto"
        st.session_state.lambda_pannello = 0.038

with col2:
    st.image("immagini/muro.png")
    if st.button("INTERCAPEDINE"):
        st.session_state.ambiente = "Intercapedine"
        st.session_state.lambda_pannello = 0.039

# ==================================================
# STEP 2 - SPESSORE
# ==================================================
if st.session_state.ambiente:

    st.subheader("Spessore pannello")
    st.session_state.spessore = st.slider("mm", 40, 200, 100, step=10)

# ==================================================
# STEP 3 - MATERIALI
# ==================================================
if st.session_state.ambiente:

    st.subheader("Materiali")

    # INTONACO
    st.write("### Intonaco")
    col1, col2, col3 = st.columns(3)

    with col1:
        st.image("immagini/intonaco1.png")
        if st.button("Termointonaco"):
            st.session_state.intonaco = 0.25

    with col2:
        st.image("immagini/intonaco2.png")
        if st.button("Bio intonaco"):
            st.session_state.intonaco = 0.29

    with col3:
        if st.button("Nessuno intonaco"):
            st.session_state.intonaco = None

    # RASANTE
    st.write("### Rasante")
    col1, col2 = st.columns(2)

    with col1:
        st.image("immagini/rasante1.png")
        if st.button("Rasante standard"):
            st.session_state.rasante = 0.49

    with col2:
        if st.button("Nessuno rasante"):
            st.session_state.rasante = None

    # FINITURA
    st.write("### Finitura")
    col1, col2 = st.columns(2)

    with col1:
        st.image("immagini/marmorino.png")
        if st.button("Marmorino BioLevel"):
            st.session_state.finitura = 0.31

    with col2:
        if st.button("Nessuna finitura"):
            st.session_state.finitura = None

# ==================================================
# STEP 4 - LOCALITÀ
# ==================================================
if st.session_state.ambiente:

    st.subheader("Località")

    gradi_giorno = {
        "Milano": 2404,
        "Torino": 2617,
        "Genova": 1435,
        "Bologna": 2259,
        "Roma": 1415,
        "Napoli": 1034,
        "Palermo": 751
    }

    citta = st.selectbox("Seleziona città", list(gradi_giorno.keys()))
    GG = gradi_giorno[citta]

# ==================================================
# CALCOLO
# ==================================================
if st.session_state.ambiente:

    superficie = st.number_input("Superficie (mq)", min_value=1.0)

def genera_pdf(dati):
    doc = SimpleDocTemplate("report_biolevel.pdf")
    styles = getSampleStyleSheet()

    contenuto = []

    contenuto.append(Paragraph("Report Configurazione BioLevel", styles["Title"]))
    contenuto.append(Spacer(1, 12))

    for key, value in dati.items():
        contenuto.append(Paragraph(f"<b>{key}:</b> {value}", styles["Normal"]))
        contenuto.append(Spacer(1, 8))

    doc.build(contenuto)

    return "report_biolevel.pdf"
    
    if st.button("Calcola"):

        spessore = st.session_state.spessore / 1000
        lambda_p = st.session_state.lambda_pannello

        # RESISTENZE SUPERFICIALI
        Rsi = 0.13
        Rse = 0.04

        strati = [(spessore, lambda_p)]

        if st.session_state.intonaco:
            strati.append((0.02, st.session_state.intonaco))
        if st.session_state.rasante:
            strati.append((0.01, st.session_state.rasante))
        if st.session_state.finitura:
            strati.append((0.005, st.session_state.finitura))

        R_tot = Rsi + sum([s/l for s,l in strati]) + Rse
        U_finale = 1 / R_tot

        # U iniziale standard
        U_iniziale = 1.5

        volume = superficie * spessore
        co2 = volume * 110

        risparmio = superficie * (U_iniziale - U_finale) * GG / 1000
        miglioramento = ((U_iniziale - U_finale) / U_iniziale) * 100
        alberi = co2 / 15

        # OUTPUT
        st.subheader("📊 Risultati")

        st.write(f"Trasmittanza finale: {U_finale:.3f} W/m²K")
        st.write(f"Miglioramento: {miglioramento:.0f}%")

        st.write(f"CO2 assorbita: {co2:.1f} kg")
        st.write(f"Risparmio energetico: {risparmio:.0f} kWh/anno")
        st.write(f"Equivalente alberi: {alberi:.0f}")

        # GRAFICO
        df = pd.DataFrame({
            "Parametro": ["CO2 (kg)", "kWh risparmiati"],
            "Valore": [co2, risparmio]
        })

        chart = alt.Chart(df).mark_bar(size=60).encode(
            x='Parametro',
            y='Valore',
            color='Parametro'
        )

        st.altair_chart(chart, use_container_width=True)

        # CTA
        st.markdown("""
        ---
        ### Hai bisogno di ulteriori informazioni riguardo i nostri prodotti?

        🔗 [Visita il sito BioLevel](https://www.tuosito.it)
        """)
                # ---------------- PDF ----------------
        dati_report = {
            "Ambiente": st.session_state.ambiente,
            "Spessore pannello (mm)": st.session_state.spessore,
            "Trasmittanza finale": f"{U_finale:.3f} W/m²K",
            "Miglioramento": f"{miglioramento:.0f} %",
            "CO2 assorbita": f"{co2:.1f} kg",
            "Risparmio energetico": f"{risparmio:.0f} kWh/anno"
        }

        file_pdf = genera_pdf(dati_report)

        with open(file_pdf, "rb") as f:
            st.download_button(
                label="📄 Scarica report PDF",
                data=f,
                file_name="Report_BioLevel.pdf",
                mime="application/pdf"
            )
