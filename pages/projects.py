import streamlit as st
import matplotlib.pyplot as plt

st.title("Projects")
st.write("You have entered", st.session_state["my_input"])


with st.sidebar:
    selected = option_menu(
        menu_title="Go to",
        options=["Home", "Account", "Trending"],
    )

if selected == "Home":
    st.title(f'You selected "{selected}"')


st.title("FloPy Example:")

import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import flopy
