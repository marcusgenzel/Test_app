# app.py
from datetime import datetime, time

import altair as alt
import numpy as np
import pandas as pd
import pandas_profiling
import streamlit as st
from streamlit_pandas_profiling import st_profile_report


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


st.subheader("This is a subheader with a divider", divider="rainbow")
st.subheader("_Streamlit_ is :blue[cool] :sunglasses:")


st.caption("This is a string that explains something above.")
st.caption("A caption with _italics_ :blue[colors] and emojis :sunglasses:")


st.text("This is some text.")

st.latex(
    r"""
    a + ar + a r^2 + a r^3 + \cdots + a r^{n-1} =
    \sum_{k=0}^{n-1} ar^k =
    a \left(\frac{1-r^{n}}{1-r}\right)
    """
)

code = """def hello():
    print("Hello, Streamlit!")"""
st.code(code, language="python")


st.header("st.slider")

# Example 1

st.subheader("Slider")

age = st.slider("How old are you?", 0, 130, 25)
st.write("I'm ", age, "years old")

# Example 2

st.subheader("Range slider")

values = st.slider("Select a range of values", 0.0, 100.0, (25.0, 75.0))
st.write("Values:", values)

# Example 3

st.subheader("Range time slider")

appointment = st.slider(
    "Schedule your appointment:", value=(time(11, 30), time(12, 45))
)
st.write("You're scheduled for:", appointment)

# Example 4

st.subheader("Datetime slider")

start_time = st.slider(
    "When do you start?", value=datetime(2020, 1, 1, 9, 30), format="MM/DD/YY - hh:mm"
)
st.write("Start time:", start_time)
st.header("Line chart")

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["a", "b", "c"])

st.line_chart(chart_data)


# source = chart_data

# chart = (
#     alt.Chart(source)
#     .mark_circle()
#     .encode(
#         x="Horsepower",
#         y="Miles_per_Gallon",
#         color="Origin",
#     )
#     .interactive()
# )

# tab1, tab2 = st.tabs(["Streamlit theme (default)", "Altair native theme"])

# with tab1:
#     # Use the Streamlit theme.
#     # This is the default. So you can also omit the theme argument.
#     st.altair_chart(chart, theme="streamlit", use_container_width=True)
# with tab2:
#     # Use the native Altair theme.
#     st.altair_chart(chart, theme=None, use_container_width=True)


st.header("st.selectbox")

option = st.selectbox("What is your favorite color?", ("Blue", "Red", "Green"))

st.write("Your favorite color is ", option)


st.header("st.checkbox")

st.write("What would you like to order?")

icecream = st.checkbox("Ice cream")
coffee = st.checkbox("Coffee")
cola = st.checkbox("Cola")

if icecream:
    st.write("Great! Here's some more 🍦")

if coffee:
    st.write("Okay, here's some coffee ☕")

if cola:
    st.write("Here you go 🥤")

st.header("`streamlit_pandas_profiling`")

df = pd.read_csv(
    "https://raw.githubusercontent.com/dataprofessor/data/master/penguins_cleaned.csv"
)

pr = df.profile_report()
st_profile_report(pr)
