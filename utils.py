
# utils.py
# -*- coding: utf-8 -*-
"""
Hjelpefunksjoner for populasjonsgenetikk-simulatoren.
"""

import numpy as np


def simulate_one_pop(p0, N, wAA, wAa, waa, mu, nu, generations,
                     bottleneck_start=None, bottleneck_duration=None, bottleneck_size=None):
    """
    Simuler én populasjon med seleksjon, mutasjon, drift og evt. flaskehals.
    
    Parametre:
        p0 : startfrekvens for A₁
        N : populasjonsstørrelse (None = uendelig)
        wAA, wAa, waa : fitnessverdier (0–1)
        mu : mutasjonsrate A₁ → A₂
        nu : mutasjonsrate A₂ → A₁
        generations : antall generasjoner
        bottleneck_start, bottleneck_duration, bottleneck_size : definerer evt. flaskehals
    """
    p = p0
    freqs = [p0]
    genotypes = []

    for gen in range(generations):
        # Hardy–Weinberg frekvenser
        p2 = p**2
        pq = 2*p*(1-p)
        q2 = (1-p)**2
        genotypes.append([p2, pq, q2])

        # Seleksjon
        w_bar = p2*wAA + pq*wAa + q2*waa
        if w_bar == 0:
            break
        p_prime = (p2*wAA + 0.5*pq*wAa) / w_bar

        # Mutasjon
        p_prime = p_prime*(1 - mu) + (1 - p_prime)*nu

        # Drift + evt. flaskehals
        if N is not None:
            if (bottleneck_start is not None and bottleneck_duration is not None and bottleneck_size is not None
                and bottleneck_start <= gen < bottleneck_start + bottleneck_duration):
                N_eff = bottleneck_size
            else:
                N_eff = N
            p = np.random.binomial(2*N_eff, p_prime) / (2*N_eff)
        else:
            p = p_prime

        freqs.append(np.clip(p, 0, 1))

    # Standardiser returformat
    freqs = np.array(freqs).reshape(-1, 1)       # (T, 1)
    genotypes = np.array(genotypes).reshape(-1, 1, 3)  # (T, 1, 3)
    return freqs, genotypes


def simulate_two_pops(p0_1, p0_2, N, fitness1, fitness2, mu, nu,
                      generations, migrate=False, m12=0, m21=0):
    """
    Simuler to populasjoner med seleksjon, mutasjon, drift og evt. migrasjon.
    
    Parametre:
        p0_1, p0_2 : startfrekvenser for A₁ i populasjon 1 og 2
        fitness1, fitness2 : tupler (wAA, wAa, waa) for hver populasjon
        mu : mutasjonsrate A₁ → A₂
        nu : mutasjonsrate A₂ → A₁
        generations : antall generasjoner
        migrate : om migrasjon skal inkluderes
        m12 : migrasjonsrate fra populasjon 1 → 2
        m21 : migrasjonsrate fra populasjon 2 → 1
    """
    p = np.array([p0_1, p0_2])
    freqs = [p.copy()]
    genotypes = [[[p[0]**2, 2*p[0]*(1-p[0]), (1-p[0])**2],
                  [p[1]**2, 2*p[1]*(1-p[1]), (1-p[1])**2]]]

    for _ in range(generations):
        new_p = []
        gen = []
        for i, pi in enumerate(p):
            wAA, wAa, waa = fitness1 if i == 0 else fitness2

            p2 = pi**2
            pq = 2*pi*(1-pi)
            q2 = (1-pi)**2
            gen.append([p2, pq, q2])

            w_bar = p2*wAA + pq*wAa + q2*waa
            if w_bar == 0:
                p_prime = pi
            else:
                p_prime = (p2*wAA + 0.5*pq*wAa) / w_bar

            # Mutasjon
            p_prime = p_prime*(1 - mu) + (1 - p_prime)*nu

            # Drift
            if N is not None:
                pi_next = np.random.binomial(2*N, p_prime) / (2*N)
            else:
                pi_next = p_prime

            new_p.append(pi_next)

        p = np.array(new_p)

        # Migrasjon
        if migrate:
            p1 = (1-m21)*p[0] + m21*p[1]
            p2 = (1-m12)*p[1] + m12*p[0]
            p = np.array([p1, p2])

        freqs.append(np.clip(p.copy(), 0, 1))
        genotypes.append(gen)

    freqs = np.vstack(freqs)        # (T, 2)
    genotypes = np.array(genotypes) # (T, 2, 3)
    return freqs, genotypes