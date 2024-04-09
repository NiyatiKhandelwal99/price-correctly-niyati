import streamlit as st
import pandas as pd
import requests

def get_coordinates(address, api_key):
    base_url = "https://api.geoapify.com/v1/geocode/search"
    params = {
        "text": address,
        "apiKey": api_key
    }
    response = requests.get(base_url, params=params)
    if response.status_code == 200:
        results = response.json()['features']
        if results:
            #print(results)
            first_result = results[0]['geometry']['coordinates']
            return first_result[1], first_result[0]
    return None, None

def show():
    # st.set_page_config(page_title='Price Right Explorer', page_icon='📊')
    st.title('📊 Price Right Explorer')
    
    st.subheader('To provide a rough estimate for the place ($)')

    # Load data
    df = pd.read_csv('./filtered_listings_detailed.csv')

    locations = df.neighbourhood_group_cleansed
    # Input widgets
    location = st.text_input("(*) Enter Street:")
    zip_code = st.text_input("(*) Enter Zip Code:")
    
    latitude, longitude = get_coordinates(location+",Seattle, WA "+zip_code, "0964937f262f41b5a5372ceddfd602ed")
    print(latitude, longitude)

    # Initial list of property types
    property_types = [
    "Entire guesthouse", "Private room in rental unit", "Entire home", "Entire guest suite",
    "Entire rental unit", "Private room in home", "Entire bungalow", "Private room in cottage",
    "Entire condo", "Private room in loft", "Private room in guesthouse",
    "Private room in bungalow", "Entire townhouse", "Private room in condo", "Entire cabin",
    "Entire loft", "Boat", "Shared room in townhouse", "Entire vacation home",
    "Private room in treehouse", "Entire villa", "Private room in townhouse", "Camper/RV", 
    "Tiny home", "Houseboat", "Entire place", "Room in boutique hotel", "Private room in resort",
    "Casa particular", "Room in hotel", "Shared room in rental unit", "Farm stay", 
    "Room in aparthotel", "Shared room in bed and breakfast", "Private room in bed and breakfast",
    "Private room in hostel", "Bus", "Room in hostel"
    ]

    # Deduplicating the list
    unique_property_types = list(set(property_types))

    unique_property_types.sort()  # Sort the list for better readability

    print(unique_property_types)
    unique_property_types = ["Select a Property Type"] + unique_property_types

    # property_type = df.property_type.unique()
    property_type_selection = st.selectbox('(*) Property Type', unique_property_types)

    # if "private" and "Select a Property Type" not in property_type_selection.lower():
    if "private" not in property_type_selection.lower() and "select" not in property_type_selection.lower():
        df.bedrooms = df.bedrooms.fillna(0).astype(int)
        bedroom = df.bedrooms.unique()
        bedroom.sort()
        bedroom_selection = st.selectbox('Bedrooms', bedroom)

    df.accommodates = df.accommodates.astype('int')
    accomodates = df.accommodates.unique()
    accomodates.sort()
    accomodates_selection = st.selectbox('Max number of people it can accomodate', accomodates)



    amenities = ['Smoke alarm', 'Essentials', 'Carbon monoxide alarm', 'Hangers', 'Kitchen', 'Hair dryer', 'Hot water', 'Dishes and silverware', 'Microwave', 'Shampoo']

    amenities_list = list(amenities)
    amenities_select = st.multiselect('Select amenities available', amenities_list);


    #Display price
    st.markdown("# The average price for your property would be $1500", unsafe_allow_html=True)