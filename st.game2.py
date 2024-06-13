import openai, json, re
import streamlit as st
import time
from config import OPENAI_API_KEY 
import sqlalchemy
#import random


st.set_page_config(layout="wide")

conn = st.connection('pets_db', type='sql')

companion_coef = 1
weapon_coef = 1
weapon1 = ""
weapon2 = ""
environment = ""

col4, col1, col3, col2, col5 = st.columns([3,10,2,10,3])
col1.header('Player one')
warrior1 = col1.text_input('What is your name?', key = 'warrior1')
col1.write("  ")
col2.header('Player two')
warrior2 = col2.text_input('What is your name?', key = 'warrior2')
col2.write("")

if not warrior1 == "" and not warrior2 == "":
    col1.subheader(warrior2.upper() + ' how would you describe ' + warrior1.upper() + '? Write one thing about each their: ')
    trait11 = col1.text_input('1 - Physique', key = 'trait11')
    trait12 = col1.text_input('2 - Personality', key = 'trait12')
    trait13 = col1.text_input('3 - Talents', key = 'trait13')
    trait14 = col1.text_input('4 - Hobbies', key = 'trait14')
    trait15 = col1.text_input('5 - Anything weird', key = 'trait15')
    if not trait15 == "" and not trait14 == "":
        col2.subheader(warrior1.upper() + ' how would you describe ' + warrior2.upper() + '? Write one thing about each their: ')
        trait21 = col2.text_input('1 - Physique', key = 'trait21')
        trait22 = col2.text_input('2 - Personality', key = 'trait22')
        trait23 = col2.text_input('3 - Talents', key = 'trait23')
        trait24 = col2.text_input('4 - Hobbies', key = 'trait24')
        trait25 = col2.text_input('5 - Anything weird', key = 'trait25')
        
        if not trait25 == "" and not trait24 == "":
            companion1 = col1.text_input('What is their soul animal?', key = 'companion1')
            companion2 = col2.text_input('What is their soul animal?', key = 'companion2')
            if not companion2 == "" and not companion1 == "":
                weapon1 = col1.text_input('Finally, in a world of insane savagery, what would be their weapon?', key = 'weapon1')
                weapon2 = col2.text_input('Finally, in a world of insane savagery, what would be their weapon?', key = 'weapon2')

if not weapon1 == "" and not weapon2 == "":
    status = 'Initializing ...'
    st.write(status)
    time.sleep(3)
    environments = ("high school cafeteria", "volcano", "colloseum", "war torn leningrad", "abandoned church", "chocolate factory", "tropical island", "pirate ship", "space station", "fairytale meadow", "castle")
    #environment = random.choice(environments)
    environment = "island"
    
    status = 'Prepare for battle!'
    st.subheader(status + '  \n  \n')
    
    
    _ = """
    """
    
    
    #Set up prompt
    prompt = "The battle will take place in the environment of: {}\n\
    \n\
    First character's name: {}\n\
    Pet companion: {}\n\
    Weapon: {}\n\
    Attributes: \n\
    - {}\n\
    - {}\n\
    - {}\n\
    - {}\n\
    - {}\n\
    \n\
    Second character's name: {}\n\
    Pet companion: {}\n\
    Weapon: {}\n\
    Attributes: \n\
    - {}\n\
    - {}\n\
    - {}\n\
    - {}\n\
    - {}\n".format(environment, warrior1, companion1, weapon1, trait11, trait12, trait13, trait14, trait15, warrior2, companion2, weapon2, trait21, trait22, trait23, trait24, trait25)
    
    
    openai.api_key = st.secrets['auth_token']
    
    #FIGHT!!!
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", 
             "content": "You are a successful fiction novel writer. I will give you information on two characters. Your task is to describe an epic battle between the two characters. \
                Be playful and funny, the fight should by dynamic with possible twists. One of the characters must win the battle in the end, but the choice should be random. \
                Each character has a weapon and pet companion that should play a role in the battle. Also, each character has a set of five attributes, \
                Use 2 or 3 of the attributes provided in the prompt for each of the characters, but do not repeat them word for word. The output will be three paragraphs long with a maximum of 200 words.",
             },
            {"role": "user", 
             "content": "{}".format(prompt),
             }
            ],
        frequency_penalty=1,
        max_tokens=1000,
        temperature = 1)
    
    battle = response.choices[0].message.content
    st.write("\n\n\n\n", battle)
