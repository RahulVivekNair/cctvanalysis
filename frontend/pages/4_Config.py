import streamlit as st
import json

if st.session_state["authentication_status"]:
    st.title("Configuration Page")
    if 'save_config' not in st.session_state:
        st.session_state['save_config'] = None 
    option = st.selectbox(
    'Select number of cameras',
    ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10'))

    if st.button('Save'):
        st.session_state['save_config'] = 1

    if st.session_state['save_config'] == 1:
        # JSON saving logic
        try:
            config = {
                "num_cameras": option  # Key-value pair
            }
            with open("data/config.json", "w") as f:
                json.dump(config, f)
            st.success('Configuration saved to config.json')
        except IOError:
            st.error('Error saving configuration to file')
        finally:
            st.session_state['save_config'] = None

else:
    st.error('You are not logged in')