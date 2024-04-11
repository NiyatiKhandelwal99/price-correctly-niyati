import streamlit as st
import pandas as pd
import requests
from joblib import dump, load
import sklearn

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
    print(sklearn.__version__)
    # st.set_page_config(page_title='Price Right Explorer', page_icon='📊')
    st.title('📊 Price Right Explorer')
    
    st.subheader('To provide a rough estimate for the place ($)')

    # Load data
    df = pd.read_csv('./filtered_listings_detailed.csv')

    # Input widgets
    location = st.text_input("(*) Enter Street:")
    zip_code = st.text_input("(*) Enter Zip Code:")
    
    print("Location: ",location)
    print("Zip code: ",zip_code)
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
    "Tiny home", "Houseboat", "Entire place", "Private room in resort", "Shared room in rental unit", "Shared room in bed and breakfast", "Private room in bed and breakfast",
    "Private room in hostel", "Entire cottage", "Entire serviced apartment", "Private Room in aparthotel", 
    "Private Room in boutique hotel", "Private Room in hotel", "Private room in boat", "Private room in casa particular", 
    "Private room in earthen home", "Private room in guest suite", "Private room in serviced apartment", "Private room in tiny home",
    "Private room in villa", "Shared room in home", "Shared room in hostel", "Tent"
    ]
    neighbourhood_cleansed = ['neighbourhood_cleansed_Adams', 'neighbourhood_cleansed_Alki', 'neighbourhood_cleansed_Arbor Heights', 
                              'neighbourhood_cleansed_Atlantic', 'neighbourhood_cleansed_Belltown', 'neighbourhood_cleansed_Bitter Lake', 
                              'neighbourhood_cleansed_Briarcliff', 'neighbourhood_cleansed_Brighton', 'neighbourhood_cleansed_Broadview', 
                              'neighbourhood_cleansed_Broadway', 'neighbourhood_cleansed_Bryant', 'neighbourhood_cleansed_Cedar Park', 
                              'neighbourhood_cleansed_Central Business District', 'neighbourhood_cleansed_Columbia City', 
                              'neighbourhood_cleansed_Crown Hill', 'neighbourhood_cleansed_Dunlap', 'neighbourhood_cleansed_East Queen Anne', 
                              'neighbourhood_cleansed_Eastlake', 'neighbourhood_cleansed_Fairmount Park', 'neighbourhood_cleansed_Fauntleroy', 
                              'neighbourhood_cleansed_First Hill', 'neighbourhood_cleansed_Fremont', 'neighbourhood_cleansed_Gatewood', 
                              'neighbourhood_cleansed_Genesee', 'neighbourhood_cleansed_Georgetown', 'neighbourhood_cleansed_Green Lake', 
                              'neighbourhood_cleansed_Greenwood', 'neighbourhood_cleansed_Haller Lake', 'neighbourhood_cleansed_Harrison/Denny-Blaine',
                            'neighbourhood_cleansed_High Point', 'neighbourhood_cleansed_Highland Park', 'neighbourhood_cleansed_Holly Park', 
                            'neighbourhood_cleansed_Industrial District', 'neighbourhood_cleansed_Interbay', 'neighbourhood_cleansed_International District', 
                            'neighbourhood_cleansed_Laurelhurst', 'neighbourhood_cleansed_Lawton Park', 'neighbourhood_cleansed_Leschi', 
                            'neighbourhood_cleansed_Lower Queen Anne', 'neighbourhood_cleansed_Loyal Heights', 'neighbourhood_cleansed_Madison Park', 
                            'neighbourhood_cleansed_Madrona', 'neighbourhood_cleansed_Mann', 'neighbourhood_cleansed_Maple Leaf', 
                            'neighbourhood_cleansed_Matthews Beach', 'neighbourhood_cleansed_Meadowbrook', 'neighbourhood_cleansed_Mid-Beacon Hill', 
                            'neighbourhood_cleansed_Minor', 'neighbourhood_cleansed_Montlake', 'neighbourhood_cleansed_Mount Baker', 
                            'neighbourhood_cleansed_North Admiral', 'neighbourhood_cleansed_North Beach/Blue Ridge', 'neighbourhood_cleansed_North Beacon Hill', 
                            'neighbourhood_cleansed_North College Park', 'neighbourhood_cleansed_North Delridge', 'neighbourhood_cleansed_North Queen Anne', 
                            'neighbourhood_cleansed_Olympic Hills', 'neighbourhood_cleansed_Phinney Ridge', 'neighbourhood_cleansed_Pike-Market', 
                            'neighbourhood_cleansed_Pinehurst', 'neighbourhood_cleansed_Pioneer Square', 'neighbourhood_cleansed_Portage Bay', 
                            'neighbourhood_cleansed_Rainier Beach', 'neighbourhood_cleansed_Rainier View', 'neighbourhood_cleansed_Ravenna', 
                            'neighbourhood_cleansed_Riverview', 'neighbourhood_cleansed_Roosevelt', 'neighbourhood_cleansed_Roxhill', 
                            'neighbourhood_cleansed_Seaview', 'neighbourhood_cleansed_Seward Park', 'neighbourhood_cleansed_South Beacon Hill', 
                            'neighbourhood_cleansed_South Delridge', 'neighbourhood_cleansed_South Lake Union', 'neighbourhood_cleansed_South Park', 
                            'neighbourhood_cleansed_Southeast Magnolia', 'neighbourhood_cleansed_Stevens', 'neighbourhood_cleansed_Sunset Hill', 
                            'neighbourhood_cleansed_University District', 'neighbourhood_cleansed_Victory Heights', 'neighbourhood_cleansed_View Ridge', 
                            'neighbourhood_cleansed_Wallingford', 'neighbourhood_cleansed_Wedgwood', 'neighbourhood_cleansed_West Queen Anne', 
                            'neighbourhood_cleansed_West Woodland', 'neighbourhood_cleansed_Westlake', 'neighbourhood_cleansed_Whittier Heights', 
                            'neighbourhood_cleansed_Windermere', 'neighbourhood_cleansed_Yesler Terrace']


    # Deduplicating the list
    unique_property_types = list(set(property_types))

    unique_property_types.sort()  # Sort the list for better readability

    # print(unique_property_types)
    unique_property_types = ["Select a Property Type"] + unique_property_types

    # property_type = df.property_type.unique()
    property_type_selection = st.selectbox('(*) Property Type', unique_property_types)

    bedroom_selection = 1
    # if "private" and "Select a Property Type" not in property_type_selection.lower():
    if "private" not in property_type_selection.lower() and "select" not in property_type_selection.lower():
        bedroom_options = list(range(1, 13))
        print(bedroom_options)
        bedroom_selection = st.selectbox('Bedrooms', bedroom_options)
        
    bathroom_options = [0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6]
    bathroom_selection = st.selectbox('Bathrooms', bathroom_options)

    df.accommodates = df.accommodates.astype('int')
    accomodates = df.accommodates.unique()
    accomodates.sort()
    accomodates_selection = st.selectbox('Max number of people it can accomodate', accomodates)



    amenities = ['Smoke alarm', 'Essentials', 'Carbon monoxide alarm', 'Hangers', 'Kitchen', 'Hair dryer', 'Hot water', 'Dishes and silverware', 'Microwave', 'Shampoo']

    amenities_list = list(amenities)
    amenities_select = st.multiselect('Select amenities available', amenities_list, help="Tip: Statistics show that listing amenities like 'Hot Water', 'Carbon Monoxide Alarm', 'Smoke Alarm' are liked by customers.")
    
    # Space before the info box
    for _ in range(1):  # Adjust the range to increase/decrease space
        st.write("")

    # Info box with a message
    st.info('If all details look good, press the "Calculate" button below to see the average price for your property.')

    # Calculate button with more attractive result display
    if st.button('Calculate'):

        data = {
        'latitude': latitude,
        'longitude': longitude,
        'accommodates' : accomodates_selection,
        'bathroom_selection' : [2],
        'property_type_'+property_type_selection: 1
        }
        df = pd.DataFrame(data)
        for amenity in amenities:
            if amenity in amenities_select:
                df[amenity] = 1
            else:
                df[amenity] = 0

        #commented out - Niyati
        for property in property_types:
            if (property != property_type_selection):
                df['property_type_'+property] = 0
        if "Select a Property Type" in df.columns:
            df.drop(columns=["Select a Property Type"], inplace=True)
        for neighbour in neighbourhood_cleansed:
            df[neighbour] = 0
            
        if bedroom_selection is not None:
            df['bedrooms'] = bedroom_selection
        else:
            df['bedrooms'] = 1

        if bathroom_selection is not None:
            df['bathrooms_numeric'] = bathroom_selection
        else:
            df['bathrooms_numeric'] = 1
    
        model = load('ada-dt-model.joblib')
        model_columns = ['latitude', 'longitude', 'accommodates', 'bedrooms', 'bathrooms_numeric', 'Smoke alarm', 'Essentials', 'Carbon monoxide alarm', 'Hangers', 'Kitchen', 'Hair dryer', 'Hot water', 'Dishes and silverware', 'Microwave', 'Shampoo', 'neighbourhood_cleansed_Adams', 'neighbourhood_cleansed_Alki', 'neighbourhood_cleansed_Arbor Heights', 'neighbourhood_cleansed_Atlantic', 'neighbourhood_cleansed_Belltown', 'neighbourhood_cleansed_Bitter Lake', 'neighbourhood_cleansed_Briarcliff', 'neighbourhood_cleansed_Brighton', 'neighbourhood_cleansed_Broadview', 'neighbourhood_cleansed_Broadway', 'neighbourhood_cleansed_Bryant', 'neighbourhood_cleansed_Cedar Park', 'neighbourhood_cleansed_Central Business District', 'neighbourhood_cleansed_Columbia City', 'neighbourhood_cleansed_Crown Hill', 'neighbourhood_cleansed_Dunlap', 'neighbourhood_cleansed_East Queen Anne', 'neighbourhood_cleansed_Eastlake', 'neighbourhood_cleansed_Fairmount Park', 'neighbourhood_cleansed_Fauntleroy', 'neighbourhood_cleansed_First Hill', 'neighbourhood_cleansed_Fremont', 'neighbourhood_cleansed_Gatewood', 'neighbourhood_cleansed_Genesee', 'neighbourhood_cleansed_Georgetown', 'neighbourhood_cleansed_Green Lake', 'neighbourhood_cleansed_Greenwood', 'neighbourhood_cleansed_Haller Lake', 'neighbourhood_cleansed_Harrison/Denny-Blaine', 'neighbourhood_cleansed_High Point', 'neighbourhood_cleansed_Highland Park', 'neighbourhood_cleansed_Holly Park', 'neighbourhood_cleansed_Industrial District', 'neighbourhood_cleansed_Interbay', 'neighbourhood_cleansed_International District', 'neighbourhood_cleansed_Laurelhurst', 'neighbourhood_cleansed_Lawton Park', 'neighbourhood_cleansed_Leschi', 'neighbourhood_cleansed_Lower Queen Anne', 'neighbourhood_cleansed_Loyal Heights', 'neighbourhood_cleansed_Madison Park', 'neighbourhood_cleansed_Madrona', 'neighbourhood_cleansed_Mann', 'neighbourhood_cleansed_Maple Leaf', 'neighbourhood_cleansed_Matthews Beach', 'neighbourhood_cleansed_Meadowbrook', 'neighbourhood_cleansed_Mid-Beacon Hill', 'neighbourhood_cleansed_Minor', 'neighbourhood_cleansed_Montlake', 'neighbourhood_cleansed_Mount Baker', 'neighbourhood_cleansed_North Admiral', 'neighbourhood_cleansed_North Beach/Blue Ridge', 'neighbourhood_cleansed_North Beacon Hill', 'neighbourhood_cleansed_North College Park', 'neighbourhood_cleansed_North Delridge', 'neighbourhood_cleansed_North Queen Anne', 'neighbourhood_cleansed_Olympic Hills', 'neighbourhood_cleansed_Phinney Ridge', 'neighbourhood_cleansed_Pike-Market', 'neighbourhood_cleansed_Pinehurst', 'neighbourhood_cleansed_Pioneer Square', 'neighbourhood_cleansed_Portage Bay', 'neighbourhood_cleansed_Rainier Beach', 'neighbourhood_cleansed_Rainier View', 'neighbourhood_cleansed_Ravenna', 'neighbourhood_cleansed_Riverview', 'neighbourhood_cleansed_Roosevelt', 'neighbourhood_cleansed_Roxhill', 'neighbourhood_cleansed_Seaview', 'neighbourhood_cleansed_Seward Park', 'neighbourhood_cleansed_South Beacon Hill', 'neighbourhood_cleansed_South Delridge', 'neighbourhood_cleansed_South Lake Union', 'neighbourhood_cleansed_South Park', 'neighbourhood_cleansed_Southeast Magnolia', 'neighbourhood_cleansed_Stevens', 'neighbourhood_cleansed_Sunset Hill', 'neighbourhood_cleansed_University District', 'neighbourhood_cleansed_Victory Heights', 'neighbourhood_cleansed_View Ridge', 'neighbourhood_cleansed_Wallingford', 'neighbourhood_cleansed_Wedgwood', 'neighbourhood_cleansed_West Queen Anne', 'neighbourhood_cleansed_West Woodland', 'neighbourhood_cleansed_Westlake', 'neighbourhood_cleansed_Whittier Heights', 'neighbourhood_cleansed_Windermere', 'neighbourhood_cleansed_Yesler Terrace', 'property_type_Boat', 'property_type_Camper/RV', 'property_type_Entire bungalow', 'property_type_Entire cabin', 'property_type_Entire condo', 'property_type_Entire cottage', 'property_type_Entire guest suite', 'property_type_Entire guesthouse', 'property_type_Entire home', 'property_type_Entire loft', 'property_type_Entire place', 'property_type_Entire rental unit', 'property_type_Entire serviced apartment', 'property_type_Entire townhouse', 'property_type_Entire vacation home', 'property_type_Entire villa', 'property_type_Houseboat', 'property_type_Private Room in aparthotel', 'property_type_Private Room in boutique hotel', 'property_type_Private Room in hotel', 'property_type_Private room in bed and breakfast', 'property_type_Private room in boat', 'property_type_Private room in bungalow', 'property_type_Private room in casa particular', 'property_type_Private room in condo', 'property_type_Private room in cottage', 'property_type_Private room in earthen home', 'property_type_Private room in guest suite', 'property_type_Private room in guesthouse', 'property_type_Private room in home', 'property_type_Private room in hostel', 'property_type_Private room in loft', 'property_type_Private room in rental unit', 'property_type_Private room in resort', 'property_type_Private room in serviced apartment', 'property_type_Private room in tiny home', 'property_type_Private room in townhouse', 'property_type_Private room in treehouse', 'property_type_Private room in villa', 'property_type_Shared room in bed and breakfast', 'property_type_Shared room in home', 'property_type_Shared room in hostel', 'property_type_Shared room in rental unit', 'property_type_Shared room in townhouse', 'property_type_Tent', 'property_type_Tiny home']

        df = df[model_columns]
        y_output = model.predict(df)
        st.success(f"### You should list your property for: ${round(y_output[0], 2)} per night! :moneybag:")