import streamlit as st


if st.session_state["authentication_status"]:
    st.title("Configuration Page")
    st.write("This is the configuration page")
    st.write("You can add your configuration settings here")
else:
    st.error('You are not logged in')