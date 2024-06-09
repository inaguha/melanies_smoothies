from snowflake.snowpark.functions import col
import streamlit as st
import pandas as pd
import numpy as np
cnx=st.connection("snowflake")
session=cnx.session()
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(""" Choose the fruits you want in your custom Smoothie!""")
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The Name on your Smoothie will be: ", name_on_order)
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
ingredients_list = st.multiselect('Choose upto 5 ingredients: ', my_dataframe, max_selections=5)
if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
import requests
fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
#st.text(fruityvice_response)
fv_df=st.dataframe(data=fruityvice_response.json(), use_container_width=True)
