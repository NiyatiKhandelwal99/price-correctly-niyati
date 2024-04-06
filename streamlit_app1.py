import streamlit as st
import pandas as pd
import pydeck as pdk
import json

print("Hello1")
# Load your dataset here
df = pd.read_csv('./filtered_listings_detailed.csv')

def clean_price(price):
    return float(price.replace('$', '').replace(',', ''))

df['price'] = df['price'].apply(clean_price)

with open('./data/Neighborhood_Map_Atlas_Neighborhoods.geojson') as f:
    geojson_data = json.load(f)

print("Hello")

# Streamlit application starts
st.title('Seattle Map based on Price Range')

# # Taking price range input from user
# min_price = st.number_input('Minimum Price', min_value=0)
# max_price = st.number_input('Maximum Price', min_value=0)

min_value = 0

max_price = int(df['price'].max())
print("The maximum price in the dataset is:", max_price)

min_price, max_price = st.slider(
    'What is the price range you are looking for (per day)?',
    min_value=0,
    max_value=max_price,
    value=[min_value, max_price])

# Filtering the dataset based on the price range
filtered_data = df[(df['price'] >= min_price) & (df['price'] <= max_price)]

neighborhood_count = filtered_data['neighbourhood_cleansed'].value_counts().head(10)
top_neighborhoods = neighborhood_count.index.tolist()

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
    get_color='[200, 30, 0, 160]',
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

# Display the top 10 neighborhoods with the most listings within the price range
st.subheader("Top 10 Neighborhoods with Most Listings within Price Range")
st.table(neighborhood_count)

# Show the filtered data in a table
st.write(filtered_data)

# Run the Streamlit app by pasting this code into a .py file and execute it with `streamlit run your_app.py`