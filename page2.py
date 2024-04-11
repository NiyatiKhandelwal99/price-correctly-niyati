import streamlit as st
import pandas as pd
import pydeck as pdk
import json
import plotly.express as px # type: ignore

df = pd.read_csv('./filtered_listings_detailed.csv')

def clean_price(price):
    return float(price.replace('$', '').replace(',', ''))

df['price'] = df['price'].apply(clean_price)

with open('./data/Neighborhood_Map_Atlas_Neighborhoods.geojson') as f:
    geojson_data = json.load(f)

def show_svg(svg_file):
    """Utility function to read SVG content and display it"""
    with open(svg_file, "r", encoding="utf-8") as file:
        svg_content = file.read()
        st.markdown(svg_content, unsafe_allow_html=True)

def show():
    
    st.markdown("# Seattle Real Estate Insights")  # General title, more prominent

    st.markdown("## Map based on Price Range")
    min_value = 0
    max_price = 1000 # after analysing the data in the dataset

    min_price, max_price = st.slider(
        'What is the price range you are looking for (per day)?',
        min_value=0,
        max_value=max_price,
        value=[min_value, max_price])

    # Filtering the dataset based on the price range
    filtered_data = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

    # neighborhood_count = filtered_data['neighbourhood_cleansed'].value_counts().head(10)
    # top_neighborhoods = neighborhood_count.index.tolist()

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

    # st.markdown("## Top 10 Neighborhood Listings as a Percentage of Total")  # Another subtitle
    # Display the top 10 neighborhoods with the most listings within the price range
    # st.subheader("Top 10 Neighborhoods with Most Listings within Price Range")
    neighborhood_count = filtered_data['neighbourhood_cleansed'].value_counts(normalize=True).head(10) * 100

    # Convert the series to a DataFrame, which is required for Plotly
    neighborhood_count_df = neighborhood_count.reset_index()
    neighborhood_count_df.columns = ['Neighborhood', 'Percentage']

    # Create a pie chart
    fig = px.pie(neighborhood_count_df, values='Percentage', names='Neighborhood', title='Top 10 Neighborhood Listings as a Percentage of Total')
    fig.update_layout(width=700, height=500)  # You can adjust the values as needed
    st.plotly_chart(fig)

    st.markdown("---")  # Divider
    
    st.markdown("## Overall Seattle Neighborhood Price Density")  # Another subtitle for the new section
    # st.markdown('Overall Seattle Neighborhood Price Density')
    show_svg('seattle_map_price_density_neighborhood.svg')