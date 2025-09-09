"""
Evolusjonsmekanismer
"""

import streamlit as st
from utils import simulate_one_pop, simulate_two_pops

st.title("Evolusjonsmekanismer")

# --- Seleksjon ---
with st.expander("Naturlig seleksjon", expanded=True):
    if st.session_state.get("num_pops", 1) == 1:
        st.session_state["wAA_1"] = st.slider(
            "Fitness A₁A₁", 0.0, 1.0, 1.0, step=0.01,
            help="Relativ fitness for genotypen A₁A₁. 1.0 betyr ingen seleksjon mot denne genotypen."
        )
        st.session_state["wAa_1"] = st.slider(
            "Fitness A₁A₂", 0.0, 1.0, 1.0, step=0.01,
            help="Relativ fitness for genotypen A₁A₂."
        )
        st.session_state["waa_1"] = st.slider(
            "Fitness A₂A₂", 0.0, 1.0, 1.0, step=0.01,
            help="Relativ fitness for genotypen A₂A₂."
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Populasjon 1")
            st.session_state["wAA_1"] = st.slider(
                "Fitness A₁A₁", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₁A₁ i populasjon 1."
            )
            st.session_state["wAa_1"] = st.slider(
                "Fitness A₁A₂", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₁A₂ i populasjon 1."
            )
            st.session_state["waa_1"] = st.slider(
                "Fitness A₂A₂", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₂A₂ i populasjon 1."
            )
        with col2:
            st.subheader("Populasjon 2")
            st.session_state["wAA_2"] = st.slider(
                "Fitness A₁A₁", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₁A₁ i populasjon 2."
            )
            st.session_state["wAa_2"] = st.slider(
                "Fitness A₁A₂", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₁A₂ i populasjon 2."
            )
            st.session_state["waa_2"] = st.slider(
                "Fitness A₂A₂", 0.0, 1.0, 1.0, step=0.01,
                help="Relativ fitness for genotypen A₂A₂ i populasjon 2."
            )

# --- Mutasjon ---
with st.expander("Mutasjoner", expanded=True):
    st.session_state["mu"] = st.number_input(
        "Mutasjonsrate A₁ → A₂", 0.0, 1.0, 0.0, step=0.0001,
        help="Sannsynlighet per generasjon for at allel A₁ muterer til A₂."
    )
    st.session_state["nu"] = st.number_input(
        "Mutasjonsrate A₂ → A₁", 0.0, 1.0, 0.0, step=0.0001,
        help="Sannsynlighet per generasjon for at allel A₂ muterer til A₁."
    )

# --- Genetisk drift ---
with st.expander("Genetisk drift", expanded=True):
    use_drift = st.checkbox(
        "Inkluder genetisk drift (endelig populasjonsstørrelse)", value=False,
        help="Hvis aktivert simuleres populasjonen med endelig størrelse N, ellers uendelig stor populasjon."
    )
    if use_drift:
        st.session_state["N"] = st.number_input(
            "Populasjonsstørrelse (N)", 10, 10000, 100,
            help="Antall individer i populasjonen. Lavere N gir sterkere genetisk drift."
        )
    else:
        st.session_state["N"] = None

# --- Flaskehals (kun hvis én populasjon og endelig N) ---
if st.session_state.get("num_pops", 1) == 1 and st.session_state["N"] is not None:
    with st.expander("Flaskehalshendelse"):
        use_bottleneck = st.checkbox(
            "Inkluder flaskehalshendelse", value=False,
            help="Kortvarig reduksjon i populasjonsstørrelse som øker genetisk drift."
        )
        if use_bottleneck:
            st.session_state["bottleneck_start"] = st.number_input(
                "Startgenerasjon", 0, 500, 20,
                help="Generasjon når flaskehalsen starter."
            )
            st.session_state["bottleneck_duration"] = st.number_input(
                "Varighet", 1, 500, 10,
                help="Hvor mange generasjoner flaskehalsen varer."
            )
            st.session_state["bottleneck_size"] = st.number_input(
                "Populasjonsstørrelse under flaskehals", 2, st.session_state["N"], 10,
                help="Antall individer under flaskehalsen."
            )

# --- Genflyt (kun hvis to populasjoner) ---
if st.session_state.get("num_pops", 1) == 2:
    with st.expander("Genflyt"):
        migrate = st.checkbox(
            "Inkluder migrasjon", value=False,
            help="Midlertidig utveksling av individer mellom populasjonene."
        )
        if migrate:
            st.session_state["m12"] = st.slider(
                "Migrasjonsrate fra pop 1 → 2", 0.0, 1.0, 0.0, step=0.01,
                help="Sannsynlighet for at et individ fra populasjon 1 migrerer til populasjon 2 per generasjon."
            )
            st.session_state["m21"] = st.slider(
                "Migrasjonsrate fra pop 2 → 1", 0.0, 1.0, 0.0, step=0.01,
                help="Sannsynlighet for at et individ fra populasjon 2 migrerer til populasjon 1 per generasjon."
            )

# --- Kjør simulering ---
st.markdown("---")
if st.button("🚀 Kjør simulering"):
    if st.session_state["num_pops"] == 1:
        freqs, genotypes = simulate_one_pop(
            p0=st.session_state["p0"],
            N=st.session_state["N"],
            wAA=st.session_state["wAA_1"],
            wAa=st.session_state["wAa_1"],
            waa=st.session_state["waa_1"],
            mu=st.session_state["mu"],
            nu=st.session_state["nu"],
            generations=st.session_state["generations"],
            bottleneck_start=st.session_state.get("bottleneck_start"),
            bottleneck_duration=st.session_state.get("bottleneck_duration"),
            bottleneck_size=st.session_state.get("bottleneck_size")
        )
    else:
        freqs, genotypes = simulate_two_pops(
            p0_1=st.session_state["p0_1"],
            p0_2=st.session_state["p0_2"],
            N=st.session_state["N"],
            fitness1=(st.session_state["wAA_1"], st.session_state["wAa_1"], st.session_state["waa_1"]),
            fitness2=(st.session_state["wAA_2"], st.session_state["wAa_2"], st.session_state["waa_2"]),
            mu=st.session_state["mu"],
            nu=st.session_state["nu"],
            generations=st.session_state["generations"],
            migrate=st.session_state.get("m12", 0) > 0 or st.session_state.get("m21", 0) > 0,
            m12=st.session_state.get("m12", 0),
            m21=st.session_state.get("m21", 0),
        )

    st.session_state["freqs"] = freqs
    st.session_state["genotypes"] = genotypes

    st.success("Simulering ferdig!")
    st.switch_page("pages/results.py")