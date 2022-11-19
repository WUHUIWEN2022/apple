import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.header('Breakfast Menu')
streamlit.text('Omega 3 & Blueberry Oatmeal')
streamlit.text('Kale, Spinach & Rocket Smoothie')
streamlit.text('Hard-Boiled Free-Range Egg')
streamlit.text('🥣 🥗 🐔 🥑🍞') 


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')

# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])

fruits_to_show = my_fruit_list.loc[fruits_selected]

# Display the table on the page.
streamlit.dataframe(fruits_to_show)




# cretate the repeatable code block
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+ fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

# New Section to dispaly API
streamlit.header('Fruit advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    strealit.error( "please select a fruit ..")
  else:
      back_from_function = get_fruityvice_data(fruit_choice)
      streamlit.dataframe(back_from_function)
   
except URLError as e:
   streamlit.error()
   
streamlit.header("Hello from fruit_load_list:")
# SnowFlake functions
def get_fruit_loadList():
        with my_cnx_cursor() as my_cur:
             my_cur.execute("SELECT * from fruit_load_list")
             return my_cur.fetchall()
        
# Add a button to load the fruit        
if streamlit.button('Get fruit Load List'):
        my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
        my_data_rows = my_cur.fetchall()
        streamlit.dataframe(my_data_rows)

 
add_my_fruit = streamlit.text_input('Which one ? from fruit_load_listt?','jackfruit')
streamlit.write ('thanks ..', add_my_fruit)

#...
# my_cur.execute( "insert into fruit_load_list  values ('from streamlit')")
