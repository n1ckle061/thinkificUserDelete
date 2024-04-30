import streamlit as st
import pandas as pd
import requests
import time
from thinkific import HEADERS, grab_ids, delete_users


st.write("""
# Thinkific User Delete
This app provides an intuitive user interface that will allow you to upload a list of Thinkfic users' emails and have them deleted on Thinkific, via the provided API.   
""")

uploaded_file = st.file_uploader("Upload a CSV file", type={"csv", "text"})
if uploaded_file is not None:
    col1, col2 = st.columns(2)
    with col1:
        uploaded_file_df = pd.read_csv(uploaded_file)
        st.write(uploaded_file_df)
    with col2:
        option = st.selectbox(
        'Which column contains the emails of users that you wish to delete?',
        tuple(uploaded_file_df.columns),
        index=None,
        placeholder="Select email column")
        thinkific_api_key = st.text_input("Thinkific API Key", placeholder="Please enter your Thinkific API key")            
        thinkific_subdomain = st.text_input("Thinkific Sub-Domain", placeholder="Please enter your Thinkific sub-domain")            
        st.write("Column selected:", f"""`{option}`""")
        disable_button = (not bool(thinkific_api_key)) or (not bool(thinkific_subdomain)) or (not bool(option))
        if st.button("Delete users", disabled=disable_button, type="primary"):
            HEADERS["X-Auth-API-Key"] = thinkific_api_key
            HEADERS["X-Auth-Subdomain"] = thinkific_subdomain
            with st.status("Executing deletion process...", expanded=True) as status:
                try:
                    st.write("Grabing user ids from Thinkific...")
                    ids_to_delete = grab_ids(email_list=list(uploaded_file_df[option]), header=HEADERS)
                    st.write("Ids retrieved, sending deletion request to Thinkific...")
                    time.sleep(5)
                    # delete_users(ids_to_delete, header=HEADERS)
                    status.update(label="All done!", state="complete", expanded=False)
                except Exception as e:
                    # st.error("An error has occured while sending requests to Thinkific, please make sure your API key and subdomain were entered correctly")
                    st.error(e)
                    status.update(label="Incomplete", state="error", expanded=True)
                
            
        
            