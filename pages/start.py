# pages/start.py
# -*- coding: utf-8 -*-
"""
Startside for populasjonsgenetikk-simulatoren
"""

import streamlit as st

st.title("Populasjonsgenetikk-utforsker")



# --- Tid ---
with st.expander("⏳ Tid", expanded=True):
    st.session_state["generations"] = st.slider(
        "Antall generasjoner",
        min_value=10, max_value=500, value=100
    )

# --- Antall populasjoner ---
with st.expander("👥 Antall populasjoner", expanded=True):
    st.session_state["num_pops"] = st.radio("Antall populasjoner:", [1, 2])

# --- Startfrekvens(er) ---
with st.expander("🌱 Startfrekvens A₁", expanded=True):
    if st.session_state["num_pops"] == 1:
        st.session_state["p0"] = st.slider(
            "Allelfrekvens A₁",
            min_value=0.0, max_value=1.0, value=0.5, step=0.01
        )
    else:
        col1, col2 = st.columns(2)
        with col1:
            st.session_state["p0_1"] = st.slider(
                "Populasjon 1",
                min_value=0.0, max_value=1.0, value=0.5, step=0.01
            )
        with col2:
            st.session_state["p0_2"] = st.slider(
                "Populasjon 2",
                min_value=0.0, max_value=1.0, value=0.5, step=0.01
            )