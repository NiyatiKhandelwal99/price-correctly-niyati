import streamlit as st
from page1 import show as show_page1
from page2 import show as show_page2

st.sidebar.markdown("# Welcome to Price Right")

# Your navigation options below the sidebar "header"
page = st.sidebar.radio("", ["Right Price for your Place", "Find your Neighborhood"])

# Adding a description in the sidebar below the navigation options
st.sidebar.markdown("Choose an option to get started with our services. Whether you're looking to find the right price for your place to put on Airbnb or searching for your ideal neighborhood, we've got you covered.")

if page == "Right Price for your Place":
    show_page1()
elif page == "Find your Neighborhood":
    show_page2()
