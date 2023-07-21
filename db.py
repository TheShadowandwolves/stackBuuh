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
                thumbnail TEXT,
                class TEXT,
                race TEXT,
                level INTEGER,
                xp INTEGER,
                player_name TEXT,
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
                description TEXT
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
                name TEXT NOT NULL,
                type TEXT,
                rarity TEXT,
                description TEXT
            )
        ''')

        # Commit the changes and close the connection
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f'Error connecting to the database: {e}')

def add_spell(spell_data):
    try:
        conn = sqlite3.connect('spells_database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO spells (name, level, casting_time, range, duration, description) VALUES (?, ?, ?, ?, ?, ?)', spell_data)
        conn.commit()
        conn.close()
    except sqlite3.Error as e:
        print(f'Error adding spell to the database: {e}')