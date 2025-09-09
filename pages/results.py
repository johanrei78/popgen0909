# pages/results.py
# -*- coding: utf-8 -*-
"""
Resultatvisning for populasjonsgenetikk-simulatoren
"""

import streamlit as st
import matplotlib.pyplot as plt

st.title("Resultater")

if "freqs" not in st.session_state:
    st.warning("Ingen simulering funnet. Kjør først en simulering.")
else:
    freqs = st.session_state["freqs"]
    genotypes = st.session_state["genotypes"]
    num_pops = freqs.shape[1]

    choice = st.radio("Velg visning:", ["Allelfrekvenser", "Genotypefrekvenser"])

    if num_pops == 1:
        fig, ax = plt.subplots()
        if choice == "Allelfrekvenser":
            ax.plot(freqs, label="A₁")
            ax.set_ylabel("Frekvens av A₁")
        else:
            ax.plot(genotypes[:, 0, 0], label="A₁A₁")
            ax.plot(genotypes[:, 0, 1], label="A₁A₂")
            ax.plot(genotypes[:, 0, 2], label="A₂A₂")
            ax.set_ylabel("Genotypefrekvens")
            ax.legend()

        ax.set_xlabel("Generasjon")
        ax.set_ylim(0, 1)
        ax.grid(True)  # legg til rutenett
        st.pyplot(fig)

    elif num_pops == 2:
        col1, col2 = st.columns(2)
        for pop_idx, col in enumerate([col1, col2]):
            with col:
                fig, ax = plt.subplots()
                if choice == "Allelfrekvenser":
                    ax.plot(freqs[:, pop_idx], label="A₁")
                    ax.set_ylabel("Frekvens av A₁")
                else:
                    ax.plot(genotypes[:, pop_idx, 0], label="A₁A₁")
                    ax.plot(genotypes[:, pop_idx, 1], label="A₁A₂")
                    ax.plot(genotypes[:, pop_idx, 2], label="A₂A₂")
                    ax.set_ylabel("Genotypefrekvens")
                    ax.legend()

                ax.set_xlabel("Generasjon")
                ax.set_ylim(0, 1)
                ax.grid(True)  # legg til rutenett
                ax.set_title(f"Populasjon {pop_idx+1}")
                st.pyplot(fig)