import streamlit as st
import pandas as pd
import altair as alt

# --- STILE GRADIENTE ---
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(to top right, #f4c303, #f47c00, #b652f4);
        color: #000000;
    }
    .stButton>button {
        background-color: #8000ff;
        color: white;
    }
    </style>
    """,
    unsafe_allow_html=True
)
# Logo in alto, centrato
st.image("cb7e327c-7c69-40e3-9b4d-d2e7557358fe.png", width=300, use_column_width=True)
st.title("🌿 Configura il tuo ambiente BioLevel")

# --- INPUT ---
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
        "Nessuno": None,
        "Termoitonaco Omnia": 0.25,
        "Bio intonaco naturale": 0.29,
        "Intonaco in calce pura": 0.53
    }
    intonaco = st.selectbox("Seleziona intonaco", list(intonaco_dict.keys()), help="Seleziona il tipo di intonaco o Nessuno")
    lambda_intonaco = intonaco_dict[intonaco]

with st.expander("🪵 Selezione Rasante"):
    rasante_dict = {
        "Nessuno": None,
        "Rasante standard": 0.49,
        "Rasante bio": 0.45
    }
    rasante = st.selectbox("Seleziona rasante", list(rasante_dict.keys()))
    lambda_rasante = rasante_dict[rasante]

with st.expander("🎨 Selezione Finitura"):
    finitura_dict = {
        "Nessuno": None,
        "Marmorino di finitura Bio Level": 0.31
    }
    finitura = st.selectbox("Seleziona finitura", list(finitura_dict.keys()))
    lambda_finitura = finitura_dict[finitura]

# Malta fissa
lambda_malta = 0.36

# --- CALCOLI ---
if st.button("Calcola"):
    volume_m3 = superficie * (spessore_pannello / 1000)
    CO2_per_m3 = 110
    co2_assorbita = volume_m3 * CO2_per_m3

    # Lista strati e lambda
    strati = [(spessore_pannello/1000, lambda_pannello)]
    if lambda_intonaco: strati.append((0.02, lambda_intonaco))
    if lambda_rasante: strati.append((0.01, lambda_rasante))
    if lambda_malta: strati.append((0.01, lambda_malta))
    if lambda_finitura: strati.append((0.005, lambda_finitura))
    
    U_totale = 1 / sum([s/l for s,l in strati])
    
    gradi_giorno = 2500
    risparmio_kwh = superficie * (1.5 - U_totale) * gradi_giorno / 1000
    alberi = co2_assorbita / 15

    # --- OUTPUT ---
    st.subheader("📋 Riepilogo")
    st.write(f"Ambiente: {ambiente}")
    st.write(f"Pannello: {pannello} ({spessore_pannello} mm)")
    st.write(f"Intonaco: {intonaco}")
    st.write(f"Rasante: {rasante}")
    st.write(f"Finitura: {finitura}")

    st.subheader("🌱 CO2 assorbita e risparmio energetico")
    st.write(f"CO2 assorbita: {co2_assorbita:.1f} kg")
    st.write(f"Risparmio stimato: {risparmio_kwh:.0f} kWh/anno")
    st.write(f"Equivalente alberi piantati: {alberi:.0f} alberi")

    # --- GRAFICO UNICO ---
    df = pd.DataFrame({
        "Parametro": ["CO2 assorbita (kg)", "Risparmio energetico (kWh)"],
        "Valore": [co2_assorbita, risparmio_kwh]
    })

    chart = alt.Chart(df).mark_bar(size=60).encode(
        x=alt.X('Parametro', sort=None),
        y='Valore',
        color=alt.Color('Parametro', scale=alt.Scale(range=["#00b894", "#0984e3"]))
    ).properties(height=400)
    
    st.altair_chart(chart, use_container_width=True)
