import streamlit as st

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

# Matplotlib example


a = np.arange(100)
st.pyplot(a)
