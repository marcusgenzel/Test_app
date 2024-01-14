import streamlit as st


st.title("Projects")
st.write("You have entered", st.session_state["my_input"])


# provide options to either select an image form the gallery, upload one, or fetch from URL
gallery_tab, upload_tab, url_tab = st.tabs(["Gallery", "Upload", "Image URL"])

with gallery_tab:
    st.write("Gallery")

    st.title("FloPy Example:")

    import matplotlib as mpl
    import flopy

    # Load packages
    # 1. Standard/Built-in library imports
    # 2. Related third party library imports
    # 3. Local application/library specific imports.
    import os
    import sys

    import flopy
    import matplotlib.pyplot as plt
    import numpy as np
    import ipywidgets as widgets
    from ipywidgets import interactive

    from topic_func.EX_Modpath import *
    from topic_func.postprocess import *

    # sys.path.append("C:/GW_GitHub/TUD_GW_MOD/basic_func")
    # from basic_func.postprocess import *
