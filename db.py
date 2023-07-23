import sqlite3
import os
import discord
from discord.ext import commands


def run_db():
    try:
        # Connect to the database (or create a new one if it doesn't exist)
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()

        # Create the character table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                character_id INTEGER PRIMARY KEY,
                character_name TEXT,
                player_name TEXT,
                server_id TEXT,
                thumbnail TEXT,
                class TEXT,
                race TEXT,
                level INTEGER,
                xp INTEGER,
                alignment TEXT,
                backstory TEXT,
                armor_class INTEGER,
                initiative INTEGER,
                speed INTEGER,
                inspiration INTEGER,
                max_hp INTEGER,
                current_hp INTEGER,
                death_saves TEXT,
                strength INTEGER,
                dexterity INTEGER,
                constitution INTEGER,
                intelligence INTEGER,
                wisdom INTEGER,
                charisma INTEGER,
                strength_mod INTEGER,
                dexterity_mod INTEGER,
                constitution_mod INTEGER,
                intelligence_mod INTEGER,
                wisdom_mod INTEGER,
                charisma_mod INTEGER,
                copper INTEGER,
                silver INTEGER,
                electrum INTEGER,
                gold INTEGER,
                platinum INTEGER,
                temp_hp INTEGER,
                hit_dice TEXT,
                prof_bonus INTEGER  
                    
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Connect to or create the database file
        conn = sqlite3.connect('spells_database.db')
        cursor = conn.cursor()

        # Create a table to store spells
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS spells (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                level INTEGER NOT NULL,
                casting_time TEXT,
                range TEXT,
                duration TEXT,
                description TEXT,
                c_class LIST
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()

        # Connect to or create the database file
        conn = sqlite3.connect('equipment_database.db')
        cursor = conn.cursor()

        # Create a table to store equipment items
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS equipment (
                id INTEGER PRIMARY KEY,
                character_name TEXT NOT NULL,
                name TEXT NOT NULL,
                type TEXT,
                rarity TEXT,
                description TEXT,
                
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f'Error connecting to the database: {e}')

def new_character(name, player, server):
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        # Insert the new character into the database
        cursor.execute('''
            INSERT INTO characters (
                character_name,
                player_name,
                server_id,
                thumbnail,
                class,
                race,
                level,
                xp,
                alignment,
                backstory,
                armor_class,
                initiative,
                speed,
                inspiration,
                max_hp,
                current_hp,
                death_saves,
                strength,
                dexterity,
                constitution,
                intelligence,
                wisdom,
                charisma,
                strength_mod,
                dexterity_mod,
                constitution_mod,
                intelligence_mod,
                wisdom_mod,
                charisma_mod,
                copper,
                silver,
                electrum,
                gold,
                platinum,
                temp_hp,
                hit_dice

            )
            VALUES (?,?,?, '', '', '', 0, 0, '', '', 0, 0, 0, 0, 0, 0, '', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,0,0,0,0,0,0, 0)
        ''', (str(name), str(player), str(server), ))

        # Get the ID of the newly inserted character
        character_id = cursor.lastrowid

        # Commit the changes
        conn.commit()
        print(f"New character table created for {name}.  `({character_id})`")
        return f"New character table created for {name}.  `({character_id})`"
    except sqlite3.Error as e:
        print(f'Error creating a new character: {e}')
        return f'Error creating a new character: {e}'

def delete_character(character_id):
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM characters WHERE character_id = ?', (character_id,))
        conn.commit()
        conn.close()
        return f"Character table deleted for {character_id}."
    except sqlite3.Error as e:
        print(f'Error deleting character: {e}')

def list_characters():
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT character_id, character_name FROM characters')
        character_list = cursor.fetchall()
        conn.close()
        return character_list
    except sqlite3.Error as e:
        print(f'Error listing characters: {e}')

def set_character(character_name, data_list):
    # Connect to the database
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        character_id = character_name.lower()
        temp_name = character_name.lower()
        # Parse the data_list into a dictionary
        data_dict = {}
        try:
            data_pairs = data_list.split(',')
            for pair in data_pairs:
                name, value = pair.strip().split('=')
                data_dict[name.strip()] = value.strip()
        except Exception as e:
            return f"Invalid data format: {e}"
            

        # Update character information in the database
        update_query = 'UPDATE characters SET '
        update_params = []
        for name, value in data_dict.items():
            update_query += f"{name} = ?, "
            update_params.append(value)

        #check if id is in the database
        cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
        character_data = cursor.fetchone()
        if character_data:
            update_query = update_query[:-2] + f" WHERE character_id = ?"
            update_params.append(character_id)
            cursor.execute(update_query, update_params)
            conn.commit()
            conn.close()
            return f"Character ID {character_id} updated successfully."
        else:
            cursor.execute('SELECT * FROM characters WHERE character_name = ?', (temp_name,))
            character_data = cursor.fetchone()
            if character_data:
                update_query = update_query[:-2] + f" WHERE character_name = ?"
                update_params.append(temp_name)
                cursor.execute(update_query, update_params)
                conn.commit()
                conn.close()
                return f"Character ID {character_id} updated successfully."
            else:
                conn.close()
                return f"Unable to set Character."
        
    except sqlite3.Error as e:
        print(f'Error setting character: {e}')
        return f'Error setting character: {e}'
    
def get_character(character:str):
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE player_name = ?', (character,))
        character_data = cursor.fetchone()
        conn.close()
        cursor.execute('SELECT * FROM characters WHERE character_name = ?', (character,))
        character_data2 = cursor.fetchone()
        conn.close()
        if character_data:
            return character_data
        elif character_data2:
            return character_data2
    except sqlite3.Error as e:
        return f'Error getting character: {e}'
    
def get_character_id(player:str):
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT character_id FROM characters WHERE player_name = ?', (player,))
        character_id = cursor.fetchone()
        conn.close()
        if character_id:
            return character_id[0]
        else:
            return f"Character not found."
    except sqlite3.Error as e:
        return f'Error getting character: {e}'
    
def search_character(character_id):
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM characters WHERE character_id = ?', (character_id,))
        character_data = cursor.fetchone()
        conn.close()
        if character_data:
            return character_data
        else:
            return f"Character not found."
    except sqlite3.Error as e:
        return f'Error getting character: {e}'
    
def delete_all_characters():
    try:
        conn = sqlite3.connect('character_database.db')
        cursor = conn.cursor()
        cursor.execute('DELETE FROM characters')
        conn.commit()
        conn.close()
        return f"Character table deleted."
    except sqlite3.Error as e:
        print(f'Error deleting character: {e}')








# new spell
def new_spell(name:str, level, casting_time, range, duration, description, c_class):
    try:
        conn = sqlite3.connect('spells_database.db')
        cursor = conn.cursor()
        # Insert the new spell into the database
        cursor.execute('''
            INSERT INTO spells (
                name,
                level,
                casting_time,
                range,
                duration,
                description,
                c_class
            )
            VALUES (?,?,?,?,?,?,?)
        ''', (name.lower, level, casting_time, range, duration, description, c_class,))

        # Get the ID of the newly inserted spell
        spell_id = cursor.lastrowid

        # Commit the changes
        conn.commit()
        conn.close()
        return f"New spell table created for {name}.  `({spell_id})`"
    except sqlite3.Error as e:
        print(f'Error creating a new spell: {e}')

# new equipment
def new_equipment(character_name:str, name, type, rarity, description, c_class):
    try:
        conn = sqlite3.connect('equipment_database.db')
        cursor = conn.cursor()
        # Insert the new equipment into the database
        cursor.execute('''
               INSERT INTO equipment (
                   character_name,
                   name,
                   type,
                   rarity,
                   description,
                   c_class
               )    
                ''', (character_name.lower, name, type, rarity, description, c_class,))        
        # Get the ID of the newly inserted equipment
        equipment_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return f"New equipment table created for {name}.  `({equipment_id})`"
    except sqlite3.Error as e:
        print(f'Error creating a new equipment: {e}')
                    
                       




def add_spell(spell_data):
    try:
        conn = sqlite3.connect('spells_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO spells (name, level, casting_time, range, duration, description) VALUES (?, ?, ?, ?, ?, ?)', spell_data)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f'Error adding spell to the database: {e}')