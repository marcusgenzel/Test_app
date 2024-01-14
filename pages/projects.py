import streamlit as st

st.title("Projects")
st.write("You have entered", st.session_state["my_input"])


# provide options to either select an image form the gallery, upload one, or fetch from URL
gallery_tab, upload_tab, url_tab = st.tabs(["Gallery", "Upload", "Image URL"])

with gallery_tab:
    st.write("Gallery")

    st.title("FloPy Example:")
