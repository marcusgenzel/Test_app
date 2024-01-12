# app.py
import streamlit as st


def main():
    st.title("My Streamlit App")
    st.write("Hello, Streamlit!")

    st.title("Hello, Streamlit!")

    # Get user input
    user_input = st.text_input("Enter your name:")

    # Display a greeting
    if user_input:
        st.write(f"Hello, {user_input}!")


if __name__ == "__main__":
    main()


st.title("Test!")
