import streamlit_authenticator as stauth
import yaml

with open('data/pass.yaml') as file:
    config = yaml.load(file, Loader=yaml.SafeLoader)

# Hash passwords
hashed_passwords = stauth.Hasher(config['credentials']['usernames']).generate()

# Update config file
for username, values in config['credentials']['usernames'].items():
    values['password'] = hashed_passwords[username]

with open('data/pass.yaml', 'w') as file:
    yaml.dump(config, file, default_flow_style=False)