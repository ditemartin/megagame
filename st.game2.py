import openai, json, re
import streamlit as st
import time
import OPENAI_API_KEY from config

st.write('OPENAI_API_KEY')
st.set_page_config(layout="wide")
conn = sqlite3.connect('game.sqlite')
cur = conn.cursor()



companion_coef = 1
weapon_coef = 1
weapon1 = ""
weapon2 = ""

col4, col1, col3, col2, col5 = st.columns([3,10,2,10,3])
col1.header('Player one')
warrior1 = col1.text_input('What is your name?', key = 'warrior1')
col1.write("", key = 'spacerr')
col2.header('Player two')
warrior2 = col2.text_input('What is your name?', key = 'warrior2')
col2.write("", key = 'spacer')

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
    #Set up database structure
    cur.execute('DROP TABLE IF EXISTS weapons')
    cur.execute('DROP TABLE IF EXISTS companions')
    cur.execute('DROP TABLE IF EXISTS environments')
    cur.execute('DROP TABLE IF EXISTS traits')
    cur.execute('DROP TABLE IF EXISTS character')
    cur.execute('DROP TABLE IF EXISTS warriors')

    cur.execute('CREATE TABLE IF NOT EXISTS weapons (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TINYTEXT NOT NULL UNIQUE, coef FLOAT NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS companions (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TINYTEXT NOT NULL UNIQUE, coef FLOAT NOT NULL)')
    cur.execute('CREATE TABLE IF NOT EXISTS environments (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TINYTEXT NOT NULL UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS traits (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TINYTEXT NOT NULL UNIQUE)')
    cur.execute('CREATE TABLE IF NOT EXISTS character (trait_id INTEGER NOT NULL, warrior_id INTEGER NOT NULL, PRIMARY KEY (trait_id, warrior_id))')
    cur.execute('CREATE TABLE IF NOT EXISTS warriors (id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE, name TINYTEXT NOT NULL, weapon_id INTEGER NOT NULL, companion_id INTEGER NOT NULL)')

    cur.execute('INSERT OR IGNORE INTO environments (name) VALUES ("high school cafeteria"), \
                ("volcano"), ("colloseum"), ("war torn leningrad"), ("abandoned church"), ("chocolate factory"), \
                ("tropical island"), ("pirate ship"), ("space station"), ("fairytale meadow"), ("castle");')
    
    status = 'Inputs ready ...'
    st.write(status)
    
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait11,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait11,))
    trait11_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait21,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait21,))
    trait21_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait12,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait12,))
    trait12_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait22,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait22,))
    trait22_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait13,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait13,))
    trait13_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait23,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait23,))
    trait23_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait14,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait14,))
    trait14_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait24,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait24,))
    trait24_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait15,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait15,))
    trait15_id = cur.fetchone()[0]
    cur.execute('INSERT OR IGNORE INTO traits (name) VALUES (?)', (trait25,))
    cur.execute('SELECT id FROM traits WHERE name = (?)', (trait25,))
    trait25_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO companions (name, coef) VALUES (?,?)', (companion1,companion_coef))
    cur.execute('INSERT OR IGNORE INTO companions (name, coef) VALUES (?,?)', (companion2,companion_coef))
    cur.execute('INSERT OR IGNORE INTO weapons (name, coef) VALUES (?,?)', (weapon1, weapon_coef))
    cur.execute('INSERT OR IGNORE INTO weapons (name, coef) VALUES (?,?)', (weapon2, weapon_coef))
    cur.execute('SELECT id FROM weapons WHERE name = (?)', (weapon1,))
    weapon1_id = cur.fetchone()[0]
    cur.execute('SELECT id FROM weapons WHERE name = (?)', (weapon2,))
    weapon2_id = cur.fetchone()[0]
    cur.execute('SELECT id FROM companions WHERE name = (?)', (companion1,))
    companion1_id = cur.fetchone()[0]
    cur.execute('SELECT id FROM companions WHERE name = (?)', (companion2,))
    companion2_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO warriors (name, weapon_id, companion_id) VALUES (?,?,?)', (warrior1, weapon1_id, companion1_id))
    cur.execute('INSERT OR IGNORE INTO warriors (name, weapon_id, companion_id) VALUES (?,?,?)', (warrior2, weapon2_id, companion2_id))
    cur.execute('SELECT id FROM warriors WHERE name = ?', (warrior1,))
    warrior1_id = cur.fetchone()[0]
    cur.execute('SELECT id FROM warriors WHERE name = ?', (warrior2,))
    warrior2_id = cur.fetchone()[0]

    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait11_id, warrior1_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait12_id, warrior1_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait13_id, warrior1_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait14_id, warrior1_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait15_id, warrior1_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait21_id, warrior2_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait22_id, warrior2_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait23_id, warrior2_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait24_id, warrior2_id))
    cur.execute('INSERT OR IGNORE INTO character (trait_id, warrior_id) VALUES (?,?)', (trait25_id, warrior2_id))
    conn.commit()
    
    cur.execute('SELECT name FROM environments ORDER BY random()')
    environment = cur.fetchone()[0]
    print(environment)
    
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


openai.api_key = OPENAI_API_KEY

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
