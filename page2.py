import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px # type: ignore

df = pd.read_csv('./data/downloaded_dataset.csv')

with open('./data/Neighborhood_Map_Atlas_Neighborhoods.geojson') as f:
    geojson_data = json.load(f)

def show_svg(svg_file):
    # Define a function to display SVG content with alignment adjustments
    with open(svg_file, "r", encoding="utf-8") as file:
        svg_content = file.read()
        left_aligned_svg = f"""
        <div style="text-align: left;">{svg_content}</div>
        """
        st.markdown(left_aligned_svg, unsafe_allow_html=True)

def show():
    
    st.markdown("# Seattle Real Estate Insights")  # General title, more prominent

    st.markdown("## Map based on Price Range")
    min_value = 0
    max_price = 1000 # after analysing the data in the dataset

    min_price, max_price = st.slider('What is the price range you are looking for (per day)?', 0, max_price, (0, max_price))    

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
    # Property type selector
    #property_type_options = df.columns[df.columns.str.startswith('property_type_')]
    property_type_selected = st.selectbox(
        "Select a Property Type:",
        property_types
    )

    print("Property type selected:"+property_type_selected)
     # Number of bedrooms selector
    if 'Private' in property_type_selected:
        print("In here")
        bedrooms_selected = 1
        st.write("Number of Bedrooms: 1 (Fixed for private types)")
    else:
        max_bedrooms = int(df['bedrooms'].max())
        bedroom_options = range(0, max_bedrooms + 1)  # Creating a range up to max_bedrooms
        bedrooms_selected = st.selectbox(
            "Number of Bedrooms:",
            bedroom_options
        )

    # Filtering the dataset based on the selected inputs
    filtered_data = df[
        (df['price'] >= min_price) &
        (df['price'] <= max_price) &
        (df['bedrooms'] == bedrooms_selected) &
        (df[f'property_type_{property_type_selected}'] == 1)
    ]

    # min_price, max_price = st.slider(
    #     'What is the price range you are looking for (per day)?',
    #     min_value=0,
    #     max_value=max_price,
    #     value=[min_value, max_price])

    # # Filtering the dataset based on the price range
    # filtered_data = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

    # Plotting the map with neighborhood boundaries
    map_layer = pdk.Layer(
        "GeoJsonLayer",
        geojson_data,
        stroked=True,  # Ensure that the boundary lines are drawn
        filled=True,  # Fill the neighborhoods for visibility
        get_fill_color=[0, 0, 0, 20],  # Use a semi-transparent fill
        get_line_color=[255, 165, 0],  # Set the boundary lines to white for visibility
        get_line_width=2,  # Set the line width to make the boundaries more noticeable
        line_width_min_pixels=1,  # Minimum line width in pixels
    )

    point_layer = pdk.Layer(
    'ScatterplotLayer',
    data=filtered_data,
    get_position='[longitude, latitude]',
    get_color='[0, 128, 0, 160]',  # Dark green color with some opacity
    get_radius=100,
    )


    st.pydeck_chart(pdk.Deck(
        map_style='mapbox://styles/mapbox/light-v9',
        initial_view_state=pdk.ViewState(
            latitude=47.6062,  # Correct latitude for Seattle
            longitude=-122.3321,  # Correct longitude for Seattle
            zoom=11,
            pitch=50,
        ),
        layers=[point_layer, map_layer]
    ))

    neighborhood_columns = [col for col in filtered_data.columns if 'neighbourhood_cleansed_' in col]
    neighborhood_counts = filtered_data[neighborhood_columns].sum().sort_values(ascending=False).head(10)

    # Step 2: Calculate percentage
    total_listings = filtered_data.shape[0]  # Total number of listings
    neighborhood_percentages = (neighborhood_counts / total_listings) * 100

    # Step 3: Prepare data for visualization
    neighborhood_count_df = neighborhood_percentages.reset_index()
    neighborhood_count_df.columns = ['Neighborhood', 'Percentage']

    # Removing prefix from neighborhood names for better readability
    neighborhood_count_df['Neighborhood'] = neighborhood_count_df['Neighborhood'].str.replace('neighbourhood_cleansed_', '')

    # Step 4: Create a pie chart
    fig = px.pie(neighborhood_count_df, values='Percentage', names='Neighborhood', title='Top 10 Neighborhood Listings as a Percentage of Total')
    fig.update_layout(width=700, height=500)  # You can adjust the values as needed
    st.plotly_chart(fig)

    st.markdown("---")  # Divider
    
    st.markdown("<h2 style='text-align: right;'>Overall Seattle Neighborhood Price Density</h2>", unsafe_allow_html=True)
    show_svg('seattle_neighborhood_prices(3).svg')