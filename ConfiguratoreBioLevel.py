import streamlit as st
import pandas as pd

# --- STILE PERSONALIZZATO ---
st.markdown(
    """
    <style>
    .stApp {
        background-color: #2c003e;  /* viola scuro */
        color: #ffffff;
    }
    .stButton>button {
        background-color: #8000ff;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌿 Calcolatore coibentazione in canapa")

# --- INPUT IN EXPANDER ---
with st.expander("🔧 Selezione Ambiente e Pannello"):
    ambiente = st.selectbox("Ambiente da coibentare", ["Intercapedine", "Tetto"], help="Scegli l'ambiente da coibentare")
    
    superficie = st.number_input("Superficie da coibentare (mq)", min_value=1.0, step=1.0, help="Inserisci la superficie in metri quadri")
    
    if ambiente == "Intercapedine":
        pannelli_disponibili = ["Panel Flex Bio Level"]
        spessore_pannello = st.slider("Spessore pannello (mm)", 40, 200, 100, step=10)
        lambda_pannello = 0.039
    else:
        pannelli_disponibili = ["Panel Wall Bio Level"]
        spessore_pannello = st.slider("Spessore pannello (mm)", 20, 180, 100, step=10)
        lambda_pannello = 0.038
    
    pannello = st.selectbox("Seleziona pannello", pannelli_disponibili, help="Tipo di pannello in canapa")

with st.expander("🧱 Selezione Intonaco"):
    intonaco_dict = {
        "Termoitonaco Omnia": 0.25,
        "Bio intonaco naturale": 0.29,
        "Intonaco in calce pura": 0.53
    }
    intonaco = st.selectbox("Seleziona intonaco", list(intonaco_dict.keys()), help="Seleziona il tipo di intonaco")
    lambda_intonaco = intonaco_dict[intonaco]

with st.expander("🪵 Selezione Rasante"):
    rasante_dict = {
        "Rasante standard": 0.49,
        "Rasante bio": 0.45
    }
    rasante = st.selectbox("Seleziona rasante", list(rasante_dict.keys()))
    lambda_rasante = rasante_dict[rasante]

with st.expander("🎨 Selezione Finitura"):
    finitura_dict = {
        "Finitura liscia": 0.31,
        "Finitura naturale": 0.28
    }
    finitura = st.selectbox("Seleziona finitura", list(finitura_dict.keys()))
    lambda_finitura = finitura_dict[finitura]

# Malta fissa
lambda_malta = 0.36

# --- CALCOLI E RISULTATI ---
if st.button("Calcola"):
    volume_m3 = superficie * (spessore_pannello / 1000)
    CO2_per_m3 = 110  # kg CO2 per m³
    co2_assorbita = volume_m3 * CO2_per_m3

    # Trasmittanza totale
    U_totale = 1 / ((spessore_pannello/1000)/lambda_pannello +
                    0.02/lambda_intonaco +
                    0.01/lambda_rasante +
                    0.01/lambda_malta +
                    0.005/lambda_finitura)
    
    gradi_giorno = 2500
    risparmio_kwh = superficie * (1.5 - U_totale) * gradi_giorno / 1000
    risparmio_euro = risparmio_kwh * 0.25
    alberi = co2_assorbita / 15

    # --- OUTPUT ---
    st.subheader("📋 Riepilogo selezioni")
    st.write(f"Ambiente: {ambiente}")
    st.write(f"Pannello: {pannello} ({spessore_pannello} mm)")
    st.write(f"Intonaco: {intonaco}")
    st.write(f"Rasante: {rasante}")
    st.write(f"Finitura: {finitura}")

    st.subheader("🌱 CO2 assorbita e risparmio energetico")
    st.write(f"CO2 assorbita: {co2_assorbita:.1f} kg")
    st.write(f"Risparmio stimato: {risparmio_kwh:.0f} kWh/anno (~{risparmio_euro:.0f} €)")
    st.write(f"Equivalente alberi piantati: {alberi:.0f} alberi")

    # Grafico
    st.subheader("📊 Visualizzazione grafica")
    df = pd.DataFrame({
        "Categoria": ["CO2 assorbita (kg)", "Risparmio energetico (kWh)"],
        "Valore": [co2_assorbita, risparmio_kwh]
    })
    st.bar_chart(df.set_index("Categoria"))
