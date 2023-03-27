import streamlit as st
import requests
from datetime import datetime, timedelta


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

st.title('Moon Phases')
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

col3, col4  = st.columns(2)
col3.text_input('latitude', '59.3293N')
col4.text_input('longitude', '18.0686E')

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


st.markdown('''
## Are Moon phases the same everywhere on Earth?
Yes, everyone sees the same phases of the Moon. People north and south of the equator do see the Moon’s current phase from different angles, though. If you traveled to the other hemisphere, the Moon would be in the same phase as it is at home, but it would appear upside down compared to what you're used to! 

Moon phases occur at the same time all around the world, but the appearance of the moon and the direction it appears to move across the sky can vary depending on the observer's location on Earth. This is because the Earth's rotation causes different parts of the planet to face the Moon at different times, resulting in different perspectives of the Moon's phases. Additionally, the angle of the Moon's orbit around the Earth can cause it to appear differently depending on the observer's location. However, the timing and sequence of the Moon's phases, such as full moon, new moon, and quarter moon, are the same for all observers regardless of their location on Earth.

For example, on March 8, 2021, the Moon was in a waning crescent phase. Seen from the Northern Hemisphere, the waning crescent appeared on the left side of the Moon. Seen from the Southern Hemisphere, the crescent appeared on the right.
''')