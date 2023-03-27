import streamlit as st
import requests
from datetime import datetime, timedelta
import library.lunar_phase_library as lunar

st.set_page_config(
    page_title="Moon Phases",
    page_icon="🌒",
)

@st.cache_data()
def fetch_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()  # assuming response contains JSON data
    else:
        st.error(f"Error: {response.status_code}")
        return None

st.title('Moon Phase')
st.write('Explore the ever-changing phases of the moon! With just a few clicks')

col1, col2 = st.columns([3,1])

if 'selected_date' not in st.session_state:
    st.session_state.selected_date = datetime.today().date()
date = col1.date_input('Select Date', st.session_state.selected_date, key="date_input")
increment_button = st.button("Increase +1 day", use_container_width=True)
decrement_button = st.button("Decrease -1 day", use_container_width=True)


if increment_button:
    st.session_state.selected_date = date + timedelta(days=1)

if decrement_button:
    st.session_state.selected_date = date - timedelta(days=1)
    
formated_date = datetime.strftime(date, "%Y-%m-%d")

t = col2.time_input('Set time', datetime.now())

st.write(t.strftime("%H:%M"))

url = 'https://svs.gsfc.nasa.gov/api/dialamoon/'+ formated_date +'T'+t.strftime("%H:%M")+''

get_moon_data = fetch_url(url)
# st.write(get_moon_data)
if get_moon_data is not None:
    moon_image = get_moon_data.get('image', {}).get('url')
    if moon_image:
        st.image(moon_image)
    else:
        st.error("No moon image found for the selected date.")
else:
    st.error("Failed to retrieve moon phase data. Please try again later.")



