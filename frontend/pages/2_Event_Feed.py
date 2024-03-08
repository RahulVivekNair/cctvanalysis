import streamlit as st

if st.session_state["authentication_status"]:
    st.title("Event Page")
else:
    st.error('You are not logged in')