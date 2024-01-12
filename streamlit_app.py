# app.py
import altair as alt
import numpy as np
import pandas as pd
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

    st.title("Test!")

    st.title("Different Tables in Streamlit")

    # Basic Table
    data = {"Column 1": [1, 2, 3], "Column 2": ["A", "B", "C"]}
    df = pd.DataFrame(data)

    st.subheader("Basic Table")
    st.table(df)

    st.title("Different Tables in Streamlit")

    # DataFrame Table

    st.subheader("DataFrame Table")
    st.dataframe(df)

    st.title("Different Tables in Streamlit")

    # Styling the Table

    st.subheader("Styled Table")
    st.table(df.style.highlight_max(axis=0))


if __name__ == "__main__":
    main()


st.header("st.button")

if st.button("Say hello"):
    st.write("Why hello there")
else:
    st.write("Goodbye")


st.header("st.write")

# Example 1

st.write("Hello, *World!* :sunglasses:")

# Example 2

st.write(1234)

# Example 3

df = pd.DataFrame({"first column": [1, 2, 3, 4], "second column": [10, 20, 30, 40]})
st.write(df)

# Example 4

st.write("Below is a DataFrame:", df, "Above is a dataframe.")

# Example 5

df2 = pd.DataFrame(np.random.randn(200, 3), columns=["a", "b", "c"])
c = (
    alt.Chart(df2)
    .mark_circle()
    .encode(x="a", y="b", size="c", color="c", tooltip=["a", "b", "c"])
)
st.write(c)
