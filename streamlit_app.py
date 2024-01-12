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
