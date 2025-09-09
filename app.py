# app.py
# -*- coding: utf-8 -*-
"""
Created on Sun Sep  7 08:36:43 2025
@author: johvik
"""

import streamlit as st

# Navigation mellom sider
pg = st.navigation([
    st.Page("pages/start.py", title="Start"),
    st.Page("pages/mechanisms.py", title="Evolusjonsmekanismer"),
    st.Page("pages/results.py", title="Resultater"),
])

pg.run()