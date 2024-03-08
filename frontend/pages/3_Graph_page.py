import streamlit as st


if st.session_state["authentication_status"]:
    st.title("Graph Page")
else:
    st.error('You are not logged in')