# Import python packages
import streamlit as st
from snowflake.snowpark.functions import col
from snowflake.snowpark.context import get_active_session
# Write directly to the app
st.title(":cup_with_straw: Customize your Smoothie :cup_with_straw:")
st.write(
    """ Choose the fruits you want in your custom Smoothie!
    """
)
#st.title('This is a title')
#st.title('_Streamlit_ is :blue[cool] :sunglasses:')
name_on_order = st.text_input("Name on Smoothie: ")
st.write("The Name on your Smoothie will be: ", name_on_order)

cnx=st.connection("snowflake")
session1=cnx.session()

my_dataframe = session1.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True);

ingredients_list = st.multiselect(
    'Choose upto 5 ingredients: ', 
    my_dataframe,
    max_selections=5
)

if ingredients_list:
    ingredients_string=''
    for fruit_chosen in ingredients_list:
        ingredients_string+=fruit_chosen
        my_insert_stmt = """ insert into smoothies.public.orders(ingredients,name_on_order) values ('""" + ingredients_string + """','""" + name_on_order + """')"""
        time_to_insert = st.button("Submit Order")
    if time_to_insert:
        session1.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '!', icon="✅")
