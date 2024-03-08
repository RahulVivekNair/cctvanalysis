import streamlit as st
import streamlit_authenticator as stauth
import yaml

# Load the configuration file for authentication
with open('data/pass.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Initialize the authenticator
authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

# Function to display the main content of the home page after successful login
def display_home_after_login():
    st.write(f'Welcome *{name}*')  # Personalized greeting
    st.title("Your Main Home Page")
    if st.sidebar.button('Logout'):
        authenticator.logout('logout','unrendered')
    # ... add other components of your home page here

# --- Authentication Area ---
name, authentication_status, username = authenticator.login('main')

if authentication_status:
    # Successful authentication
    display_home_after_login()  # Display regular home page content
      # Add logout button
elif authentication_status == False:
    st.error('Username/password is incorrect')
elif authentication_status == None:
    st.warning('Please enter your username and password')
    # Optionally, you can hide other pages or elements here if not logged in
    # For example, you can conditionally display pages if `authentication_status` is True